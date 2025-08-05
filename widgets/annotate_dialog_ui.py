# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'annotate_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_DialogAnnotate(object):
    def setupUi(self, DialogAnnotate):
        if not DialogAnnotate.objectName():
            DialogAnnotate.setObjectName(u"DialogAnnotate")
        DialogAnnotate.resize(1240, 728)
        self.horizontalLayout = QHBoxLayout(DialogAnnotate)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(DialogAnnotate)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayoutImage = QVBoxLayout()
        self.verticalLayoutImage.setObjectName(u"verticalLayoutImage")

        self.verticalLayout_2.addLayout(self.verticalLayoutImage)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(DialogAnnotate)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(350, 0))
        self.groupBox_2.setMaximumSize(QSize(350, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 9, 0, 0)
        self.stackedWidget = QStackedWidget(self.groupBox_2)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageImageClassification = QWidget()
        self.pageImageClassification.setObjectName(u"pageImageClassification")
        self.verticalLayout_4 = QVBoxLayout(self.pageImageClassification)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(self.pageImageClassification)
        self.label.setObjectName(u"label")

        self.verticalLayout_5.addWidget(self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEditClassName = QLineEdit(self.pageImageClassification)
        self.lineEditClassName.setObjectName(u"lineEditClassName")

        self.horizontalLayout_3.addWidget(self.lineEditClassName)

        self.pushButtonAddClass = QPushButton(self.pageImageClassification)
        self.pushButtonAddClass.setObjectName(u"pushButtonAddClass")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddClass.sizePolicy().hasHeightForWidth())
        self.pushButtonAddClass.setSizePolicy(sizePolicy)
        self.pushButtonAddClass.setMinimumSize(QSize(30, 0))
        self.pushButtonAddClass.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_3.addWidget(self.pushButtonAddClass)

        self.pushButtonDeleteClass = QPushButton(self.pageImageClassification)
        self.pushButtonDeleteClass.setObjectName(u"pushButtonDeleteClass")
        sizePolicy.setHeightForWidth(self.pushButtonDeleteClass.sizePolicy().hasHeightForWidth())
        self.pushButtonDeleteClass.setSizePolicy(sizePolicy)
        self.pushButtonDeleteClass.setMinimumSize(QSize(30, 0))
        self.pushButtonDeleteClass.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_3.addWidget(self.pushButtonDeleteClass)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.listWidgetClasses = QListWidget(self.pageImageClassification)
        self.listWidgetClasses.setObjectName(u"listWidgetClasses")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listWidgetClasses.sizePolicy().hasHeightForWidth())
        self.listWidgetClasses.setSizePolicy(sizePolicy1)
        self.listWidgetClasses.setMinimumSize(QSize(0, 150))
        self.listWidgetClasses.setMaximumSize(QSize(16777215, 150))

        self.verticalLayout_5.addWidget(self.listWidgetClasses)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_2 = QLabel(self.pageImageClassification)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_6.addWidget(self.label_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.pushButtonDeleteAnnotated = QPushButton(self.pageImageClassification)
        self.pushButtonDeleteAnnotated.setObjectName(u"pushButtonDeleteAnnotated")
        sizePolicy.setHeightForWidth(self.pushButtonDeleteAnnotated.sizePolicy().hasHeightForWidth())
        self.pushButtonDeleteAnnotated.setSizePolicy(sizePolicy)
        self.pushButtonDeleteAnnotated.setMinimumSize(QSize(30, 0))
        self.pushButtonDeleteAnnotated.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_4.addWidget(self.pushButtonDeleteAnnotated)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.listWidgetAnnotated = QListWidget(self.pageImageClassification)
        self.listWidgetAnnotated.setObjectName(u"listWidgetAnnotated")
        sizePolicy1.setHeightForWidth(self.listWidgetAnnotated.sizePolicy().hasHeightForWidth())
        self.listWidgetAnnotated.setSizePolicy(sizePolicy1)
        self.listWidgetAnnotated.setMinimumSize(QSize(0, 150))
        self.listWidgetAnnotated.setMaximumSize(QSize(16777215, 150))

        self.verticalLayout_6.addWidget(self.listWidgetAnnotated)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonApplyAndNext = QPushButton(self.pageImageClassification)
        self.pushButtonApplyAndNext.setObjectName(u"pushButtonApplyAndNext")

        self.horizontalLayout_5.addWidget(self.pushButtonApplyAndNext)

        self.pushButtonClearAllAnnotation = QPushButton(self.pageImageClassification)
        self.pushButtonClearAllAnnotation.setObjectName(u"pushButtonClearAllAnnotation")

        self.horizontalLayout_5.addWidget(self.pushButtonClearAllAnnotation)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.listWidgetFiles = QListWidget(self.pageImageClassification)
        self.listWidgetFiles.setObjectName(u"listWidgetFiles")

        self.verticalLayout_4.addWidget(self.listWidgetFiles)

        self.stackedWidget.addWidget(self.pageImageClassification)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.groupBox_2)


        self.retranslateUi(DialogAnnotate)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DialogAnnotate)
    # setupUi

    def retranslateUi(self, DialogAnnotate):
        DialogAnnotate.setWindowTitle(QCoreApplication.translate("DialogAnnotate", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("DialogAnnotate", u"Image", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("DialogAnnotate", u"Annotation", None))
        self.label.setText(QCoreApplication.translate("DialogAnnotate", u"Classes", None))
        self.pushButtonAddClass.setText(QCoreApplication.translate("DialogAnnotate", u"+", None))
        self.pushButtonDeleteClass.setText(QCoreApplication.translate("DialogAnnotate", u"-", None))
        self.label_2.setText(QCoreApplication.translate("DialogAnnotate", u"Annotated", None))
        self.pushButtonDeleteAnnotated.setText(QCoreApplication.translate("DialogAnnotate", u"-", None))
        self.pushButtonApplyAndNext.setText(QCoreApplication.translate("DialogAnnotate", u"Apply and Move next", None))
        self.pushButtonClearAllAnnotation.setText(QCoreApplication.translate("DialogAnnotate", u"Clear all annotation", None))
    # retranslateUi

