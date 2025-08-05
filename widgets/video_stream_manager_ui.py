# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'video_stream_manager.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSlider, QVBoxLayout, QWidget)

class Ui_FormCameraControl(object):
    def setupUi(self, FormCameraControl):
        if not FormCameraControl.objectName():
            FormCameraControl.setObjectName(u"FormCameraControl")
        FormCameraControl.resize(400, 300)
        self.verticalLayout = QVBoxLayout(FormCameraControl)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBoxCameras = QComboBox(FormCameraControl)
        self.comboBoxCameras.setObjectName(u"comboBoxCameras")

        self.horizontalLayout.addWidget(self.comboBoxCameras)

        self.pushButtonSwitchCamera = QPushButton(FormCameraControl)
        self.pushButtonSwitchCamera.setObjectName(u"pushButtonSwitchCamera")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSwitchCamera.sizePolicy().hasHeightForWidth())
        self.pushButtonSwitchCamera.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButtonSwitchCamera)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(FormCameraControl)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.lineEditAlpha = QLineEdit(FormCameraControl)
        self.lineEditAlpha.setObjectName(u"lineEditAlpha")
        sizePolicy.setHeightForWidth(self.lineEditAlpha.sizePolicy().hasHeightForWidth())
        self.lineEditAlpha.setSizePolicy(sizePolicy)
        self.lineEditAlpha.setMinimumSize(QSize(50, 0))
        self.lineEditAlpha.setMaximumSize(QSize(50, 16777215))
        self.lineEditAlpha.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEditAlpha, 1, 2, 1, 1)

        self.horizontalSliderBeta = QSlider(FormCameraControl)
        self.horizontalSliderBeta.setObjectName(u"horizontalSliderBeta")
        self.horizontalSliderBeta.setMinimum(-127)
        self.horizontalSliderBeta.setMaximum(127)
        self.horizontalSliderBeta.setSingleStep(10)
        self.horizontalSliderBeta.setPageStep(50)
        self.horizontalSliderBeta.setValue(0)
        self.horizontalSliderBeta.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.horizontalSliderBeta, 2, 1, 1, 1)

        self.lineEditBeta = QLineEdit(FormCameraControl)
        self.lineEditBeta.setObjectName(u"lineEditBeta")
        sizePolicy.setHeightForWidth(self.lineEditBeta.sizePolicy().hasHeightForWidth())
        self.lineEditBeta.setSizePolicy(sizePolicy)
        self.lineEditBeta.setMinimumSize(QSize(50, 0))
        self.lineEditBeta.setMaximumSize(QSize(50, 16777215))
        self.lineEditBeta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEditBeta, 2, 2, 1, 1)

        self.label_2 = QLabel(FormCameraControl)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.horizontalSliderAlpha = QSlider(FormCameraControl)
        self.horizontalSliderAlpha.setObjectName(u"horizontalSliderAlpha")
        self.horizontalSliderAlpha.setMaximum(30)
        self.horizontalSliderAlpha.setPageStep(5)
        self.horizontalSliderAlpha.setValue(10)
        self.horizontalSliderAlpha.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.horizontalSliderAlpha, 1, 1, 1, 1)

        self.label_3 = QLabel(FormCameraControl)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.comboBoxResolutions = QComboBox(FormCameraControl)
        self.comboBoxResolutions.setObjectName(u"comboBoxResolutions")

        self.gridLayout.addWidget(self.comboBoxResolutions, 0, 1, 1, 1)

        self.pushButtonApplyResolution = QPushButton(FormCameraControl)
        self.pushButtonApplyResolution.setObjectName(u"pushButtonApplyResolution")
        sizePolicy.setHeightForWidth(self.pushButtonApplyResolution.sizePolicy().hasHeightForWidth())
        self.pushButtonApplyResolution.setSizePolicy(sizePolicy)
        self.pushButtonApplyResolution.setMinimumSize(QSize(60, 0))
        self.pushButtonApplyResolution.setMaximumSize(QSize(60, 16777215))

        self.gridLayout.addWidget(self.pushButtonApplyResolution, 0, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(FormCameraControl)

        QMetaObject.connectSlotsByName(FormCameraControl)
    # setupUi

    def retranslateUi(self, FormCameraControl):
        FormCameraControl.setWindowTitle(QCoreApplication.translate("FormCameraControl", u"Form", None))
        self.pushButtonSwitchCamera.setText(QCoreApplication.translate("FormCameraControl", u"Switch", None))
        self.label.setText(QCoreApplication.translate("FormCameraControl", u"Alpha", None))
        self.label_2.setText(QCoreApplication.translate("FormCameraControl", u"Beta", None))
        self.label_3.setText(QCoreApplication.translate("FormCameraControl", u"Resolution", None))
        self.pushButtonApplyResolution.setText(QCoreApplication.translate("FormCameraControl", u"Apply", None))
    # retranslateUi

