# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataset_make_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.comboBoxFramework = QComboBox(Dialog)
        self.comboBoxFramework.addItem("")
        self.comboBoxFramework.setObjectName(u"comboBoxFramework")

        self.gridLayout.addWidget(self.comboBoxFramework, 0, 1, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.comboBoxDataSplit = QComboBox(Dialog)
        self.comboBoxDataSplit.addItem("")
        self.comboBoxDataSplit.setObjectName(u"comboBoxDataSplit")

        self.gridLayout.addWidget(self.comboBoxDataSplit, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonMake = QPushButton(Dialog)
        self.pushButtonMake.setObjectName(u"pushButtonMake")

        self.horizontalLayout.addWidget(self.pushButtonMake)

        self.pushButtonCancel = QPushButton(Dialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Dataset setup", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Framework", None))
        self.comboBoxFramework.setItemText(0, QCoreApplication.translate("Dialog", u"YOLOv8", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Data split", None))
        self.comboBoxDataSplit.setItemText(0, QCoreApplication.translate("Dialog", u"Train:Valid:Test = 7:2:1", None))

        self.pushButtonMake.setText(QCoreApplication.translate("Dialog", u"Make", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

