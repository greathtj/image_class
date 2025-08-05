# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_project_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_CreateProjectDialog(object):
    def setupUi(self, CreateProjectDialog):
        if not CreateProjectDialog.objectName():
            CreateProjectDialog.setObjectName(u"CreateProjectDialog")
        CreateProjectDialog.resize(520, 208)
        self.verticalLayout = QVBoxLayout(CreateProjectDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelProjectName = QLabel(CreateProjectDialog)
        self.labelProjectName.setObjectName(u"labelProjectName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelProjectName)

        self.lineEditProjectName = QLineEdit(CreateProjectDialog)
        self.lineEditProjectName.setObjectName(u"lineEditProjectName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEditProjectName)

        self.labelProjectDir = QLabel(CreateProjectDialog)
        self.labelProjectDir.setObjectName(u"labelProjectDir")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelProjectDir)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditProjectDir = QLineEdit(CreateProjectDialog)
        self.lineEditProjectDir.setObjectName(u"lineEditProjectDir")

        self.horizontalLayout.addWidget(self.lineEditProjectDir)

        self.pushButtonBrowse = QPushButton(CreateProjectDialog)
        self.pushButtonBrowse.setObjectName(u"pushButtonBrowse")

        self.horizontalLayout.addWidget(self.pushButtonBrowse)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.label = QLabel(CreateProjectDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)

        self.comboBoxProjectType = QComboBox(CreateProjectDialog)
        self.comboBoxProjectType.addItem("")
        self.comboBoxProjectType.addItem("")
        self.comboBoxProjectType.setObjectName(u"comboBoxProjectType")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxProjectType.sizePolicy().hasHeightForWidth())
        self.comboBoxProjectType.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboBoxProjectType)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(CreateProjectDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CreateProjectDialog)
        self.buttonBox.accepted.connect(CreateProjectDialog.accept)
        self.buttonBox.rejected.connect(CreateProjectDialog.reject)

        QMetaObject.connectSlotsByName(CreateProjectDialog)
    # setupUi

    def retranslateUi(self, CreateProjectDialog):
        CreateProjectDialog.setWindowTitle(QCoreApplication.translate("CreateProjectDialog", u"Create New Project", None))
        self.labelProjectName.setText(QCoreApplication.translate("CreateProjectDialog", u"Project Name:", None))
        self.labelProjectDir.setText(QCoreApplication.translate("CreateProjectDialog", u"Project Directory:", None))
        self.pushButtonBrowse.setText(QCoreApplication.translate("CreateProjectDialog", u"Browse...", None))
        self.label.setText(QCoreApplication.translate("CreateProjectDialog", u"Project Type:", None))
        self.comboBoxProjectType.setItemText(0, QCoreApplication.translate("CreateProjectDialog", u"Object Detection", None))
        self.comboBoxProjectType.setItemText(1, QCoreApplication.translate("CreateProjectDialog", u"Image Classification", None))

    # retranslateUi

