# functionLib/annotation_manager.py

import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen, QMouseEvent, QColor, QCursor, QFont
from PySide6.QtCore import Qt, Signal, Slot, QPoint, QPointF, QRect, QSize, QLineF, QRectF

class AnnotationWidget(QLabel):
    """
    A QLabel subclass that displays an image and allows drawing
    various annotations on it with mouse interaction.
    """
    # Drawing Modes
    DRAW_NONE = 0
    DRAW_RECTANGLE = 1
    DRAW_CIRCLE = 2
    DRAW_LINE = 3
    DRAW_CENTER_SQUARE = 4 # New mode for fixed-size square centered on click

    annotation_added = Signal(object, str) # Emits dict {'type': '...', 'rect': QRect, 'class': '...'}
    annotation_cleared = Signal(str)
    annotation_selected = Signal(int, str) # 새 시그널: 어노테이션 선택 시 해당 인덱스 방출
    # annotation_removed = Signal(object) # 제거된 어노테이션 데이터를 전달할 수 있음

    def __init__(self, parent=None, get_current_selected_class_text_func=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.CrossCursor)

        self.current_pixmap = QPixmap()
        self.annotations = []

        self.drawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.drawing_mode = self.DRAW_NONE
        self.is_video_mode = True
        self.tag = ""

        self.center_square_fixed_size = 50 # 이 값은 원본 이미지 픽셀 단위로 유지됩니다.

        self._image_ratio = 1.0
        self._image_offset_x = 0
        self._image_offset_y = 0
        self._image_draw_rect = QRect() # 이전에 추가된 속성

        self.setMinimumSize(320, 240)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.get_current_selected_class_text = get_current_selected_class_text_func if get_current_selected_class_text_func else (lambda: "")

        # --- 클래스별 색상 동적 할당 ---
        self._generated_class_colors = {}
        self._color_palette = [
            QColor(255, 0, 0),      # Red
            QColor(0, 255, 0),      # Green
            QColor(0, 0, 255),      # Blue
            QColor(255, 165, 0),    # Orange
            QColor(128, 0, 128),    # Purple
            QColor(0, 255, 255),    # Cyan
            QColor(255, 255, 0),    # Yellow
            QColor(255, 192, 203),  # Pink
            QColor(0, 128, 0),      # Dark Green
            QColor(0, 0, 128),      # Dark Blue
            QColor(139, 69, 19),    # Brown
            QColor(255, 99, 71),    # Tomato
            QColor(70, 130, 180),   # SteelBlue
            QColor(218, 112, 214),  # Orchid
            QColor(100, 100, 100)   # Gray (기본/fallback 색상)
        ]
        self._color_index = 0
        # ---------------------------

        # --- 어노테이션 선택을 위한 새 속성 ---
        self.selected_annotation_index = -1 # 선택된 어노테이션의 인덱스 (없으면 -1)
        # ------------------------------------

    @Slot(QImage)
    def update_image(self, q_image:QImage=None, q_dimage:QImage=None, results:object=None, is_still_image=False):
        if self.is_video_mode or is_still_image:
            """
            Updates the QLabel with a new QImage frame.
            Stores the original QImage as QPixmap for drawing consistency.
            """
            self.current_pixmap = QPixmap.fromImage(q_image)
            self.current_d_pixmap = None

            if q_dimage:
                self.current_d_pixmap = QPixmap.fromImage(q_dimage)
                self.setPixmap(self.current_d_pixmap.scaled(
                    self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
            else:
                self.setPixmap(self.current_pixmap.scaled(
                    self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))

            self.current_results = results
            self.update_image_properties()
            self.clear_selection() # 이미지 변경 시 선택 해제
            self.update()

            self.is_video_mode = not is_still_image


    def update_image_properties(self):
        """
        Calculates the actual scaled size and offset of the displayed image
        within the QLabel. This is crucial for coordinate transformation.
        Also updates the _image_draw_rect.
        """
        if self.current_pixmap.isNull():
            self._image_ratio = 1.0
            self._image_offset_x = 0
            self._image_offset_y = 0
            self._image_draw_rect = QRect()
            return

        scaled_pixmap_size = self.pixmap().size()
        widget_size = self.size()

        width_ratio = widget_size.width() / self.current_pixmap.width()
        height_ratio = widget_size.height() / self.current_pixmap.height()

        self._image_ratio = min(width_ratio, height_ratio)

        displayed_width = int(self.current_pixmap.width() * self._image_ratio)
        displayed_height = int(self.current_pixmap.height() * self._image_ratio)

        self._image_offset_x = (widget_size.width() - displayed_width) // 2
        self._image_offset_y = (widget_size.height() - displayed_height) // 2

        self._image_draw_rect = QRect(self._image_offset_x, self._image_offset_y,
                                      displayed_width, displayed_height)

    def set_drawing_mode(self, mode: int):
        """Sets the current drawing mode."""
        self.drawing_mode = mode
        self.drawing = False
        self.clear_selection() # 드로잉 모드 변경 시 선택 해제
        self.update()
        
        self.setCursor(Qt.CursorShape.CrossCursor)

    def clear_annotations(self):
        """Clears all stored annotations."""
        self.annotations.clear()
        self.clear_selection() # 어노테이션 지울 때 선택 해제
        self.annotation_cleared.emit(self.tag)
        self.update()

    def remove_last_annotation(self):
        """
        마지막으로 추가된 어노테이션을 제거합니다.
        선택된 어노테이션이 마지막 어노테이션인 경우 선택 해제합니다.
        """
        if self.annotations:
            removed_annotation = self.annotations.pop()
            print(f"마지막 어노테이션이 제거되었습니다: {removed_annotation}")
            # 제거된 어노테이션이 선택된 어노테이션이었다면 선택 해제
            if self.selected_annotation_index == len(self.annotations):
                self.selected_annotation_index = -1
            elif self.selected_annotation_index > len(self.annotations): # 제거 후 인덱스가 범위를 벗어날 경우
                self.selected_annotation_index = -1
            self.update()
        else:
            print("제거할 어노테이션이 없습니다.")

    def clear_selection(self):
        """현재 선택된 어노테이션을 해제합니다."""
        if self.selected_annotation_index != -1:
            self.selected_annotation_index = -1
            self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self.current_pixmap.isNull():
            return

        # 클릭이 표시된 이미지 영역 내에 있는지 확인
        if not self._image_draw_rect.contains(event.pos()):
            self.drawing = False
            self.clear_selection() # 이미지 영역 밖 클릭 시 선택 해제
            return

        if event.button() == Qt.MouseButton.LeftButton:
            # 드로잉 모드가 아닐 때 (어노테이션 선택 모드일 때) 어노테이션 선택 시도
            if self.drawing_mode == self.DRAW_NONE:
                self.selected_annotation_index = -1 # 일단 선택 없음으로 초기화
                
                # 시각적으로 가장 위에 있는 어노테이션을 선택하기 위해 역순으로 반복
                for i in reversed(range(len(self.annotations))):
                    annotation = self.annotations[i]
                    
                    # 어노테이션 타입별 히트 테스트
                    if annotation['type'] in ['rectangle', 'center_square']:
                        original_rect = annotation['rect']
                        
                        # 어노테이션의 원본 좌표를 위젯 좌표로 변환하여 히트 테스트
                        widget_x = original_rect.x() * self._image_ratio + self._image_offset_x
                        widget_y = original_rect.y() * self._image_ratio + self._image_offset_y
                        widget_width = original_rect.width() * self._image_ratio
                        widget_height = original_rect.height() * self._image_ratio
                        
                        bbox_in_widget_coords = QRectF(widget_x, widget_y, widget_width, widget_height)
                        
                        if bbox_in_widget_coords.contains(event.pos()):
                            self.selected_annotation_index = i
                            self.annotation_selected.emit(self.selected_annotation_index, self.tag)
                            self.update() # 선택 하이라이트를 위해 다시 그리기 요청
                            return # 선택 완료, 루프 종료
                    # TODO: 다른 어노테이션 타입(원, 선 등)에 대한 히트 테스트 로직을 여기에 추가할 수 있음
                    # elif annotation['type'] == 'circle': ...
                    # elif annotation['type'] == 'line': ...

                # 클릭된 어노테이션이 없으면 선택 해제 상태 유지 및 업데이트
                if self.selected_annotation_index == -1:
                    self.update() # 이전 선택 하이라이트 지우기 위해 다시 그리기 요청
            
            else: # 드로잉 모드가 활성화되어 있으면, 새로운 드로잉 시작
                self.drawing = True
                self.start_point = event.pos()
                self.end_point = event.pos()
                self.clear_selection() # 새 드로잉 시작 시 선택 해제
                self.update() # 드로잉 시작을 표시하기 위해 다시 그리기 요청

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.current_pixmap.isNull():
            return

        # 이미지 영역 밖으로 마우스가 나가면 드로잉 중단 (선택에는 영향 없음)
        if not self._image_draw_rect.contains(event.pos()):
            if self.drawing:
                self.drawing = False # 드로잉 중단
                self.update() # 드로잉 흔적 지우기
            return

        if self.drawing:
            self.end_point = event.pos()
            self.update() # 실시간 드로잉 피드백을 위해 다시 그리기 요청
        elif self.drawing_mode == self.DRAW_CENTER_SQUARE:
            # DRAW_CENTER_SQUARE는 마우스 드래그가 아닌 단일 클릭 기반이지만,
            # 실시간 피드백을 위해 mouseMoveEvent에서 미리보기 제공
            self.end_point = event.pos() # 현재 마우스 위치를 사용하여 미리보기 그리기
            self.update()


    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.current_pixmap.isNull():
            return

        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            self.end_point = event.pos()

            # 위젯 좌표에서 원본 이미지 좌표로 변환
            scaled_start, scaled_end = self._get_scaled_points(self.start_point, self.end_point)

            annotation_data = None
            selected_class = self.get_current_selected_class_text() # 현재 선택된 클래스 가져오기

            if self.drawing_mode == self.DRAW_RECTANGLE:
                final_rect = QRect(scaled_start, scaled_end).normalized()
                annotation_data = {'type': 'rectangle', 'rect': final_rect}
            elif self.drawing_mode == self.DRAW_CIRCLE:
                center_x = (scaled_start.x() + scaled_end.x()) / 2
                center_y = (scaled_start.y() + scaled_end.y()) / 2
                radius = QLineF(scaled_start, scaled_end).length() / 2
                annotation_data = {'type': 'circle', 'center': QPointF(center_x, center_y), 'radius': radius}
            elif self.drawing_mode == self.DRAW_LINE:
                annotation_data = {'type': 'line', 'start': scaled_start, 'end': scaled_end}
            elif self.drawing_mode == self.DRAW_CENTER_SQUARE:
                half_size = self.center_square_fixed_size / 2
                top_left_x = scaled_start.x() - half_size
                top_left_y = scaled_start.y() - half_size
                final_rect = QRect(int(top_left_x), int(top_left_y),
                                   self.center_square_fixed_size, self.center_square_fixed_size)
                annotation_data = {'type': 'center_square', 'rect': final_rect}

            if annotation_data:
                annotation_data['class'] = selected_class # 'class' 항목 추가
                annotation_data['image'] = self.current_pixmap  # 'image' 항목 추가
                self.annotations.append(annotation_data)
                # 새로운 어노테이션 추가 시 자동 선택
                self.selected_annotation_index = len(self.annotations) - 1
                self.annotation_added.emit(self.annotations, self.tag) # 외부 로깅/저장을 위해 시그널 방출
            self.update() # 최종 다시 그리기 요청

    def _get_scaled_points(self, p1: QPoint, p2: QPoint):
        """
        위젯 좌표의 두 QPoint 객체를 원본 이미지 좌표로 변환합니다.
        """
        p1_relative_x = p1.x() - self._image_offset_x
        p1_relative_y = p1.y() - self._image_offset_y
        p2_relative_x = p2.x() - self._image_offset_x
        p2_relative_y = p2.y() - self._image_offset_y

        scaled_p1 = QPoint(int(p1_relative_x / self._image_ratio), int(p1_relative_y / self._image_ratio))
        scaled_p2 = QPoint(int(p2_relative_x / self._image_ratio), int(p2_relative_y / self._image_ratio))

        return scaled_p1, scaled_p2

    def resizeEvent(self, event):
        """리사이즈 이벤트를 처리하여 픽스맵을 다시 스케일링하고 속성을 재계산합니다."""
        super().resizeEvent(event)
        if not self.current_pixmap.isNull():
            self.setPixmap(self.current_pixmap.scaled(
                self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
            self.update_image_properties()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.current_pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        displayed_pixmap = self.pixmap()
        if displayed_pixmap is None:
            return

        # 이미지 그리기 영역 클리핑
        painter.setClipRect(self._image_draw_rect)

        # --- 저장된 어노테이션 그리기 ---
        painter.save()
        painter.translate(self._image_draw_rect.x(), self._image_draw_rect.y())
        painter.scale(self._image_draw_rect.width() / self.current_pixmap.width(),
                      self._image_draw_rect.height() / self.current_pixmap.height())

        base_pen_width = 2.0 * (self.current_pixmap.width() / self._image_draw_rect.width())
        painter.setBrush(Qt.BrushStyle.NoBrush)

        for i, annotation in enumerate(self.annotations):
            # 어노테이션의 클래스에 따라 펜 색상 설정
            annotation_class = annotation.get('class', 'default_class')

            if annotation_class not in self._generated_class_colors:
                self._generated_class_colors[annotation_class] = self._color_palette[self._color_index]
                self._color_index = (self._color_index + 1) % len(self._color_palette)

            pen_color = self._generated_class_colors[annotation_class]
            
            # --- 선택된 어노테이션 하이라이트 ---
            if i == self.selected_annotation_index:
                # 선택된 어노테이션은 다른 색상과 더 두꺼운 펜으로 표시
                pen = QPen(QColor(255, 255, 0), base_pen_width * 2) # 노란색, 두 배 두께
                pen.setStyle(Qt.PenStyle.SolidLine)
            else:
                pen = QPen(pen_color, base_pen_width) # 일반 어노테이션
                pen.setStyle(Qt.PenStyle.SolidLine) # 항상 실선으로 (파선은 라이브 드로잉용)
            # -----------------------------------

            painter.setPen(pen)

            if annotation['type'] == 'rectangle':
                painter.drawRect(annotation['rect'])
            elif annotation['type'] == 'circle':
                painter.drawEllipse(annotation['center'], annotation['radius'], annotation['radius'])
            elif annotation['type'] == 'line':
                painter.drawLine(annotation['start'], annotation['end'])
            elif annotation['type'] == 'center_square':
                painter.drawRect(annotation['rect'])
                painter.setBrush(QColor(0, 0, 255)) 
                dot_diameter_scaled = 3.0 * (self.current_pixmap.width() / self._image_draw_rect.width())
                painter.drawEllipse(QPointF(annotation['rect'].center().x(), annotation['rect'].center().y()), dot_diameter_scaled / 2, dot_diameter_scaled / 2)

                # painter.restore()
                painter.setBrush(Qt.BrushStyle.NoBrush)

                # --- 클래스 이름 그리기 ---
                if annotation_class:
                    painter.save() # 텍스트 그리기 설정 변경을 위해 상태 저장
                    painter.setPen(QPen(pen_color)) # 정해진 색
                    
                    font = QFont("Arial", 16) # 폰트 설정 (폰트 이름, 크기)
                    font.setBold(True)
                    # 폰트 크기도 이미지 스케일에 맞게 조정할 수 있지만, 일반적으로 가독성을 위해 고정 크기 사용
                    # font.setPointSize(int(8 * scale_factor)) # 폰트 크기 스케일링 예시
                    painter.setFont(font)

                    # 텍스트를 그릴 영역 (사각형의 위쪽, 약간 떨어뜨려서)
                    # 텍스트 영역을 물리적 픽셀 단위로 설정하고, 다시 painter를 위젯 좌표로 옮겨 그립니다.
                    text_height = 20 # 텍스트 영역 높이
                    text_padding = 5 # 사각형 상단에서 여백

                    painter.translate(-self._image_draw_rect.topLeft()) # Painter를 위젯 좌표계로 되돌립니다.
                    
                    text_rect_widget_coords = QRectF(
                        annotation['rect'].x() + self._image_draw_rect.x(),
                        annotation['rect'].y() + self._image_draw_rect.y() - (text_height + text_padding),
                        annotation['rect'].width(),
                        text_height
                    )

                    # 텍스트를 사각형 위 중앙에 그립니다.
                    painter.drawText(text_rect_widget_coords, Qt.AlignHCenter | Qt.AlignBottom, annotation_class)
                    painter.restore() # 저장된 painter 상태 복원

        painter.restore()

        # --- 현재 실시간 드로잉 피드백 ---
        # 이 부분은 항상 녹색 파선으로 유지
        if self.drawing_mode != self.DRAW_NONE:
            if self.drawing or (self.drawing_mode == self.DRAW_CENTER_SQUARE and self._image_draw_rect.contains(self.end_point)):
                painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.PenStyle.DashLine))
                painter.setBrush(Qt.BrushStyle.NoBrush)

                if self.drawing_mode == self.DRAW_RECTANGLE:
                    painter.drawRect(QRect(self.start_point, self.end_point).normalized())
                elif self.drawing_mode == self.DRAW_CIRCLE:
                    center_x = (self.start_point.x() + self.end_point.x()) / 2
                    center_y = (self.start_point.y() + self.end_point.y()) / 2
                    radius = QLineF(self.start_point, self.end_point).length() / 2
                    painter.drawEllipse(QPoint(int(center_x), int(center_y)), int(radius), int(radius))
                elif self.drawing_mode == self.DRAW_LINE:
                    painter.drawLine(self.start_point, self.end_point)
                elif self.drawing_mode == self.DRAW_CENTER_SQUARE:
                    # 마우스 포인터 위치에 고정 크기 사각형 미리보기
                    # 여기서 원본 이미지 픽셀 크기를 위젯 픽셀 크기로 변환합니다.
                    scaled_square_size = int(self.center_square_fixed_size * self._image_ratio)
                    scaled_half_size = scaled_square_size / 2

                    temp_rect = QRect(int(self.end_point.x() - scaled_half_size),
                                      int(self.end_point.y() - scaled_half_size),
                                      scaled_square_size, scaled_square_size)
                    painter.drawRect(temp_rect)
                    painter.setBrush(QColor(0, 255, 255))
                    painter.drawEllipse(self.end_point, 3, 3)
                    painter.setBrush(Qt.BrushStyle.NoBrush)