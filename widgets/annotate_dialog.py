import os
import json
from pathlib import Path
from enum import Enum

from PySide6.QtWidgets import QDialog, QListWidget, QListWidgetItem
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QRect

from widgets.annotate_dialog_ui import Ui_DialogAnnotate
from widgets.annotation_manager import AnnotationWidget

class detection(Enum):
    OBJECT_DETECTION = 0
    CLASSIFICATION = 1
    OTHER = 2


class AnnotateDialog(QDialog):
    def __init__(
            self, 
            project_data:dict,
            detection_type = "CL",
            annotation_type=AnnotationWidget.DRAW_CENTER_SQUARE,
            parent=None
        ):
        super().__init__(parent)
        self.ui = Ui_DialogAnnotate()
        self.ui.setupUi(self)

        self.project_data = project_data
        self.detection_type = detection_type
        self.annotation_type = annotation_type

        self._init_annotation_widget()
        
        self.ui.listWidgetFiles.currentItemChanged.connect(self.on_current_item_changed)
        self.ui.pushButtonAddClass.clicked.connect(self.add_class)
        self.ui.pushButtonDeleteClass.clicked.connect(self.delete_class)

        self.ui.pushButtonApplyAndNext.clicked.connect(self.apply_and_move_next)
        self.ui.pushButtonClearAllAnnotation.clicked.connect(self.clear_all_annotation)

        self.ui.pushButtonDeleteAnnotated.clicked.connect(self.delete_annotated)

        self.my_annotator.annotation_added.connect(self.annotation_added)

        self.update_file_list()
        self.update_classes()

    def annotation_added(self):
        print("annotation added.")
<<<<<<< HEAD
        # get the class name
        selected_class_item = self.ui.listWidgetClasses.currentItem()

        # Get the name of the file without its extension (the "stem")
        image_file_name = Path(self.ui.listWidgetFiles.currentItem().text())
        if image_file_name:
            image_name = image_file_name.stem
        else:
            print("No file is selected.")
            del self.my_annotator.annotations[-1]
            return

        # Create the new path for the annotation file
        annotation_path = f"{self.project_data.get('directory')}/data/{image_name}.txt"

        if selected_class_item:
            # Assign the class for the last annotation
            this_class = selected_class_item.text()
            self.my_annotator.annotations[-1]['class'] = this_class
            # print(self.my_annotator.annotations)

            # save the annotation as a text file
            image_size = self.my_annotator.current_pixmap.size()
            annotation_str = ""
            print(self.my_annotator.annotations)
            for annotation in self.my_annotator.annotations:
                rect:QRect = annotation["rect"]
                nx = rect.x() / image_size.width()
                ny = rect.y() / image_size.height()
                nw = rect.width() / image_size.width()
                nh = rect.height() / image_size.height()
                cls = annotation['class']
                annotation_str += f"{cls} {nx} {ny} {nw} {nh}\n"
            
            with open(annotation_path, 'w') as f:
                f.write(annotation_str.strip())

        else:
            print("No class is selected.")
            del self.my_annotator.annotations[-1]
    
=======
        print(self.my_annotator.annotations)

>>>>>>> e5da825c2d8369414ecb09333cbb18b1e3f603ee
    def clear_all_annotation(self):
        # delete the annotation_info.json file
        data_dir = f"{self.project_data.get('directory')}/data"
        annotation_info_path = f"{data_dir}/annotation_info.json"
        if os.path.exists(annotation_info_path):
            os.remove(annotation_info_path)
            print(f"File '{annotation_info_path}' deleted.")

        # update the file list
        self.update_file_list()

        # clear annotated liswidget
        self.ui.listWidgetAnnotated.clear()

    def delete_annotated(self):
        annotation_info_file = f"{self.project_data.get('directory')}/data/annotation_info.json"
        selected_item = self.ui.listWidgetAnnotated.currentItem()
        selected_key = self.ui.listWidgetFiles.currentItem().text().split(":-")[0] if self.ui.listWidgetFiles.currentItem() else None
        
        if selected_key:
            # delete the item from annotation info
            self.delete_json_item(annotation_info_file, selected_key)

            if selected_item:
                # delete from the listwidget annotated.
                self.ui.listWidgetAnnotated.takeItem(self.ui.listWidgetAnnotated.row(selected_item))

                self.update_selected_item_text(
                    self.ui.listWidgetFiles.currentItem(), 
                    self.ui.listWidgetFiles.currentItem().text().split(":-")[0]
                )

    def delete_json_item(self, file_path: str, key_to_delete: str) -> bool:
        """
        Deletes an item with a given key from a JSON file.

        Args:
            file_path (str): The path to the JSON file.
            key_to_delete (str): The key of the item to delete.

        Returns:
            bool: True if the operation was successful (key was deleted or not found but file handled),
                False if a critical error occurred (e.g., file could not be read/written).
        """
        data = {}
        found_key = False

        # 1. Read the JSON file
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"Successfully loaded JSON from '{file_path}'.")
            except json.JSONDecodeError:
                print(f"Warning: '{file_path}' contains invalid JSON. Cannot delete item from invalid file.")
                return False # Cannot proceed if JSON is invalid
            except Exception as e:
                print(f"Error reading '{file_path}': {e}. Cannot delete item.")
                return False
        else:
            print(f"File '{file_path}' does not exist. Nothing to delete.")
            return True # Considered successful as there's nothing to delete from a non-existent file

        # Ensure data is a dictionary (in case it was a JSON list or other type)
        if not isinstance(data, dict):
            print(f"Error: JSON content of '{file_path}' is not a dictionary. Cannot delete item.")
            return False

        # 2. Check and delete the item
        if key_to_delete in data:
            del data[key_to_delete]
            print(f"Key '{key_to_delete}' deleted from dictionary.")
            found_key = True
        else:
            print(f"Key '{key_to_delete}' not found in JSON file '{file_path}'. No deletion performed.")
            # Even if key not found, we still might need to write if file was read successfully.
            # But for this function's purpose, if the key wasn't there, no change is needed.
            return True # Considered successful as the desired state (key absent) is achieved

        # 3. Write the modified dictionary back to the JSON file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4) # Use indent for pretty-printing
            print(f"Successfully wrote updated JSON to '{file_path}'.")
            return True
        except Exception as e:
            print(f"Error writing to '{file_path}': {e}")
            return False

    def apply_and_move_next(self):
        selected_class_item = self.ui.listWidgetClasses.currentItem()
        if selected_class_item:
            selected_class = selected_class_item.text()
        else:
            return

        if self.project_data:
            data_dir = f"{self.project_data.get('directory')}/data"
            try:
                os.makedirs(data_dir, exist_ok=True)
                print(f"Folder '{data_dir}' ensured to exist.")
            except OSError as e:
                print(f"Error creating folder '{data_dir}': {e}")

        annotate_info = {}
        if data_dir and os.path.exists(data_dir):
            annotate_info_file = f"{data_dir}/annotation_info.json"
            if not os.path.exists(annotate_info_file):
                # File does not exist, so create it
                try:
                    with open(annotate_info_file, 'w', encoding='utf-8') as f:
                        # Writing nothing, just creating an empty file
                        pass
                    print(f"File '{annotate_info_file}' did not exist and was created.")
                except IOError as e:
                    print(f"Error creating file '{annotate_info_file}': {e}")

            # File exists, so replace the value
            try:
                file_name = self.ui.listWidgetFiles.currentItem().text().split(":-")[0]
                self.update_or_add_json_item(annotate_info_file, file_name, selected_class)
                print(f"Annotation info is updated for {file_name} with {selected_class}")

                self.update_selected_item_text(
                    self.ui.listWidgetFiles.currentItem(), 
                    f"{file_name}:-{selected_class}"
                )
            except IOError as e:
                print(f"Error reading file '{annotate_info_file}': {e}")

        # move to next item
        self.select_next_list_item(self.ui.listWidgetFiles)

    def update_selected_item_text(self, selected_item:QListWidgetItem, new_text:str):
        """
        Updates the text of the currently selected item in the QListWidget
        with the text from the input field.
        """

        if selected_item is not None:
            if new_text: # Only update if new text is not empty
                old_text = selected_item.text()
                selected_item.setText(new_text) # Set the new text
                print(f"Item '{old_text}' updated to '{new_text}'.")

    def select_next_list_item(self, this_list_widget:QListWidget):
        """
        Selects the next item in the QListWidget.
        Handles wrapping from last to first, or stopping at the end.
        """
        current_row = this_list_widget.currentRow()
        total_items = this_list_widget.count()

        if total_items == 0:
            print("List is empty. No item to select.")
            return

        # Calculate the next row index
        # Method 1: Wrap around to the beginning if at the end
        next_row = (current_row + 1) % total_items

        # Method 2: Stop at the last item (uncomment this and comment out Method 1 if desired)
        # next_row = current_row + 1
        # if next_row >= total_items:
        #     print("Already at the last item. Cannot select next.")
        #     return # Stop here, don't change selection

        # Set the new current row
        this_list_widget.setCurrentRow(next_row)
        print(f"Moved selection to next item (Index: {next_row})")

    def update_or_add_json_item(self, file_path: str, key_to_modify: str, new_value: str) -> bool:
        """
        Replaces an item's value in a JSON file or adds a new item if the key doesn't exist.

        Args:
            file_path (str): The path to the JSON file.
            key_to_modify (str): The key of the item to modify or add.
            new_value (str): The new string value to set for the item.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        data = {}

        # 1. Read the JSON file (or initialize an empty dict if it doesn't exist or is invalid)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"Successfully loaded JSON from '{file_path}'.")
            except json.JSONDecodeError:
                print(f"Warning: '{file_path}' contains invalid JSON. Starting with an empty dictionary.")
                data = {} # Treat as empty if invalid JSON
            except Exception as e:
                print(f"Error reading '{file_path}': {e}. Starting with an empty dictionary.")
                data = {} # Treat as empty on other read errors
        else:
            print(f"File '{file_path}' does not exist. A new file will be created.")

        # Ensure data is a dictionary (in case it was a JSON list or other type)
        if not isinstance(data, dict):
            print(f"Warning: JSON content of '{file_path}' is not a dictionary. Overwriting with new dictionary.")
            data = {}

        # 2. Modify/Add the item
        # This single line handles both scenarios:
        # If key_to_modify exists, its value is updated.
        # If key_to_modify does not exist, it's added as a new key-value pair.
        data[key_to_modify] = new_value
        print(f"Key '{key_to_modify}' updated/added with value: '{new_value}'.")

        # 3. Write the modified dictionary back to the JSON file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4) # Use indent for pretty-printing
            print(f"Successfully wrote updated JSON to '{file_path}'.")
            return True
        except Exception as e:
            print(f"Error writing to '{file_path}': {e}")
            return False
    
    def add_class(self):
        """
        QLineEdit의 텍스트를 QListWidget에 새로운 아이템으로 추가합니다.
        """
        item_text = self.ui.lineEditClassName.text().strip() # 입력된 텍스트 가져오기 및 공백 제거
        if item_text: # 텍스트가 비어있지 않은 경우에만 추가
            self.ui.listWidgetClasses.addItem(item_text)
            self.ui.lineEditClassName.clear() # 입력 필드 초기화
            self._save_classes_to_file() # 파일 업데이트 호출
        else:
            print("Emply class name!!")

    def delete_class(self):
        """
        QListWidget에서 선택된 아이템을 삭제합니다.
        """
        selected_item = self.ui.listWidgetClasses.currentItem()
        if selected_item:
            self.ui.listWidgetClasses.takeItem(self.ui.listWidgetClasses.row(selected_item))
            self._save_classes_to_file()

    def _save_classes_to_file(self):
        """
        QListWidget에 있는 모든 클래스 아이템을 'classes.lst' 파일에 저장합니다.
        각 아이템은 파일의 새 줄에 기록됩니다.
        """
        data_dir = f"{self.project_data.get('directory')}/data"
        file_path = f"{data_dir}/classes.lst"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for i in range(self.ui.listWidgetClasses.count()):
                    item = self.ui.listWidgetClasses.item(i)
                    f.write(item.text() + '\n')
            print(f"클래스 목록이 '{file_path}'에 저장되었습니다.")
        except IOError as e:
            print(f"클래스 목록을 파일에 저장하는 중 오류 발생: {e}")

    def on_current_item_changed(self, current_item: QListWidgetItem, previous_item: QListWidgetItem):
        self.show_file_on_annotation(current_item)

    def show_file_on_annotation(self, current_item: QListWidgetItem):
        """
        QListWidget에서 파일 선택이 변경될 때 호출되는 슬롯입니다.
        선택된 이미지 파일을 로드하고, 해당하는 어노테이션 파일을 읽어 바운딩 박스를 표시합니다.
        """

        data_dir = f"{self.project_data.get('directory')}/data"
        if not current_item: # 선택된 아이템이 없으면 (예: 선택 해제)
            self.my_annotator.clear_annotations() # 어노테이션 지우기
            self.my_annotator.update_image(QImage()) # 이미지 비우기
            return

        filename = current_item.text().split(":-")[0]

        # 1) 해당 파일을 열어서 annotation image label에 표시
        self._load_image_annotation(filename)

    def _load_image_annotation(self, filename):
        data_dir = f"{self.project_data.get('directory')}/data"
        image_filepath = os.path.join(data_dir, filename)

        if not os.path.exists(image_filepath):
            print(f"오류: 이미지 파일이 존재하지 않습니다 - {image_filepath}")
            self.my_annotator.clear_annotations()
            self.my_annotator.update_image(QImage()) # 이미지 비우기
            return

        pixmap = QPixmap(image_filepath)
        if pixmap.isNull():
            print(f"오류: 이미지 로드 실패 - {image_filepath}")
            self.my_annotator.clear_annotations()
            self.my_annotator.update_image(QImage()) # 이미지 비우기
            return
        
        self.my_annotator.update_image(pixmap.toImage(), is_still_image=True)
        print(f"이미지 로드됨: {image_filepath}")

        if self.detection_type == "CL":
            data_dir = f"{self.project_data.get('directory')}/data"
            annotated_class = self.get_value_from_json_file(
                f"{data_dir}/annotation_info.json",
                filename
            )
            
            self.ui.listWidgetAnnotated.clear()
            if annotated_class:
                self.ui.listWidgetAnnotated.addItem(annotated_class)

        elif self.detection_type == "OD":
            annotation_path = f"{self.project_data.get('directory')}/data/{Path(image_filepath).stem}.txt"
            
            lines = []
            with open(annotation_path, 'r') as f:
                lines = f.readlines()
            print(lines)
            
            image_size = self.my_annotator.current_pixmap.size()
            self.my_annotator.annotations.clear()
            for line in lines:
                info = [item.strip() for item in line.split(" ")]
                self.my_annotator.annotations.append(
                    {
                        'type':'rectangle', 
                        'rect':QRect(
                            float(info[1])*image_size.width(),
                            float(info[2])*image_size.height(),
                            float(info[3])*image_size.width(),
                            float(info[4])*image_size.height()
                        ),
                        'class':info[0]
                    }
                )
                self.my_annotator.update()

    def _init_annotation_widget(self):
        self.my_annotator = AnnotationWidget(
            # get_current_selected_class_text_func = self.my_base_line_annotator._get_current_selected_class_from_list
        )
        # self.my_annotator.annotation_added.connect(self.handle_annotation_added)
        self.ui.verticalLayoutImage.addWidget(self.my_annotator)
        self.my_annotator.set_drawing_mode(self.annotation_type) # default no drawing

    def get_value_from_json_file(self, file_path: str, key: str):
        """
        Reads a JSON file and returns the value associated with a given key.

        Args:
            file_path (str): The path to the JSON file.
            key (str): The key whose value is to be retrieved.

        Returns:
            The value associated with the key, or None if:
            - The file does not exist.
            - The file contains invalid JSON.
            - The JSON content is not a dictionary.
            - The key is not found in the JSON data.
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found at '{file_path}'")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Ensure the loaded JSON is a dictionary
            if not isinstance(data, dict):
                print(f"Error: JSON content of '{file_path}' is not a dictionary.")
                return None

            # Try to retrieve the value using the key
            if key in data:
                print(f"Successfully retrieved value for key '{key}' from '{file_path}'.")
                return data[key]
            else:
                print(f"Key '{key}' not found in JSON file '{file_path}'.")
                return None

        except json.JSONDecodeError as e:
            print(f"Error: Could not decode JSON from '{file_path}'. Invalid JSON format: {e}")
            return None
        except Exception as e: # Catch other potential file reading errors
            print(f"An unexpected error occurred while processing '{file_path}': {e}")
            return None
    
    def update_file_list(self):
        if self.project_data:
            data_dir = f"{self.project_data.get('directory')}/data"
            annotated_data = {}
            try:
                os.makedirs(data_dir, exist_ok=True)
                print(f"Folder '{data_dir}' ensured to exist.")
            except OSError as e:
                print(f"Error creating folder '{data_dir}': {e}")

            if data_dir and os.path.exists(data_dir):
                self.ui.listWidgetFiles.clear()

                annotation_info_path = f"{data_dir}/annotation_info.json"
                if os.path.exists(annotation_info_path):
                    with open(annotation_info_path, 'r', encoding='utf-8') as f:
                        annotated_data = json.load(f)

                for f in sorted(os.listdir(data_dir)):
                    if f.endswith(('.png', '.jpg', '.jpeg')):
                        if f in annotated_data:
                            f = f"{f}:-{annotated_data[f]}"
                        self.ui.listWidgetFiles.addItem(f)

    def update_classes(self):
        if self.project_data:
            data_dir = f"{self.project_data.get('directory')}/data"
            try:
                os.makedirs(data_dir, exist_ok=True)
                print(f"Folder '{data_dir}' ensured to exist.")
            except OSError as e:
                print(f"Error creating folder '{data_dir}': {e}")

            classes = []
            if data_dir and os.path.exists(data_dir):
                file_path = f"{data_dir}/classes.lst"
                if not os.path.exists(file_path):
                    # File does not exist, so create it
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            # Writing nothing, just creating an empty file
                            pass
                        print(f"File '{file_path}' did not exist and was created.")
                        classes = []
                    except IOError as e:
                        print(f"Error creating file '{file_path}': {e}")
                        classes = [] # Return empty list on error
                else:
                    # File exists, so read its contents
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = [line.strip() for line in f if line.strip()] # Read lines and strip whitespace/newlines
                            print(f"File '{file_path}' exists. Contents read.")
                            classes = lines
                    except IOError as e:
                        print(f"Error reading file '{file_path}': {e}")
                        classes = [] # Return empty list on error

            self.ui.listWidgetClasses.clear()
            self.ui.listWidgetClasses.addItems(classes)