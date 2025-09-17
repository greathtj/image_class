# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_manager.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_FormProjectManager(object):
    def setupUi(self, FormProjectManager):
        if not FormProjectManager.objectName():
            FormProjectManager.setObjectName(u"FormProjectManager")
        FormProjectManager.resize(671, 800)
        self.verticalLayout = QVBoxLayout(FormProjectManager)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonCreateProject = QPushButton(FormProjectManager)
        self.pushButtonCreateProject.setObjectName(u"pushButtonCreateProject")

        self.horizontalLayout.addWidget(self.pushButtonCreateProject)

        self.pushButtonOpenProject = QPushButton(FormProjectManager)
        self.pushButtonOpenProject.setObjectName(u"pushButtonOpenProject")

        self.horizontalLayout.addWidget(self.pushButtonOpenProject)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(FormProjectManager)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label)

        self.labelCurrentProject = QLabel(FormProjectManager)
        self.labelCurrentProject.setObjectName(u"labelCurrentProject")
        font = QFont()
        font.setBold(True)
        self.labelCurrentProject.setFont(font)

        self.horizontalLayout_2.addWidget(self.labelCurrentProject)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.stackedWidgetProject = QStackedWidget(FormProjectManager)
        self.stackedWidgetProject.setObjectName(u"stackedWidgetProject")
        self.page_Blank = QWidget()
        self.page_Blank.setObjectName(u"page_Blank")
        self.stackedWidgetProject.addWidget(self.page_Blank)
        self.page_OD = QWidget()
        self.page_OD.setObjectName(u"page_OD")
        self.verticalLayout_2 = QVBoxLayout(self.page_OD)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.page_OD)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.tabWidgetOD = QTabWidget(self.page_OD)
        self.tabWidgetOD.setObjectName(u"tabWidgetOD")
        self.tabDataset = QWidget()
        self.tabDataset.setObjectName(u"tabDataset")
        self.verticalLayout_6 = QVBoxLayout(self.tabDataset)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_15 = QLabel(self.tabDataset)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QSize(0, 0))
        self.label_15.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_10.addWidget(self.label_15)

        self.pushButtonTakeShotsOD = QPushButton(self.tabDataset)
        self.pushButtonTakeShotsOD.setObjectName(u"pushButtonTakeShotsOD")

        self.horizontalLayout_10.addWidget(self.pushButtonTakeShotsOD)

        self.pushButtonImpotrOD = QPushButton(self.tabDataset)
        self.pushButtonImpotrOD.setObjectName(u"pushButtonImpotrOD")

        self.horizontalLayout_10.addWidget(self.pushButtonImpotrOD)

        self.pushButtonAnnotateOD = QPushButton(self.tabDataset)
        self.pushButtonAnnotateOD.setObjectName(u"pushButtonAnnotateOD")

        self.horizontalLayout_10.addWidget(self.pushButtonAnnotateOD)

        self.pushButtonMakeDatasetOD = QPushButton(self.tabDataset)
        self.pushButtonMakeDatasetOD.setObjectName(u"pushButtonMakeDatasetOD")

        self.horizontalLayout_10.addWidget(self.pushButtonMakeDatasetOD)


        self.verticalLayout_6.addLayout(self.horizontalLayout_10)

        self.tableWidgetFilesOD = QTableWidget(self.tabDataset)
        if (self.tableWidgetFilesOD.columnCount() < 3):
            self.tableWidgetFilesOD.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidgetFilesOD.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidgetFilesOD.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidgetFilesOD.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidgetFilesOD.setObjectName(u"tableWidgetFilesOD")
        self.tableWidgetFilesOD.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_6.addWidget(self.tableWidgetFilesOD)

        self.tabWidgetOD.addTab(self.tabDataset, "")
        self.tabTrain = QWidget()
        self.tabTrain.setObjectName(u"tabTrain")
        self.tabWidgetOD.addTab(self.tabTrain, "")

        self.verticalLayout_2.addWidget(self.tabWidgetOD)

        self.stackedWidgetProject.addWidget(self.page_OD)
        self.page_IC = QWidget()
        self.page_IC.setObjectName(u"page_IC")
        self.verticalLayout_3 = QVBoxLayout(self.page_IC)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.page_IC)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.tabWidgetIC = QTabWidget(self.page_IC)
        self.tabWidgetIC.setObjectName(u"tabWidgetIC")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_4 = QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(0, 0))
        self.label_4.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_3.addWidget(self.label_4)

        self.pushButtonTakeShots = QPushButton(self.tab)
        self.pushButtonTakeShots.setObjectName(u"pushButtonTakeShots")

        self.horizontalLayout_3.addWidget(self.pushButtonTakeShots)

        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)

        self.pushButtonAnnotate = QPushButton(self.tab)
        self.pushButtonAnnotate.setObjectName(u"pushButtonAnnotate")

        self.horizontalLayout_3.addWidget(self.pushButtonAnnotate)

        self.pushButtonMakeDataset = QPushButton(self.tab)
        self.pushButtonMakeDataset.setObjectName(u"pushButtonMakeDataset")

        self.horizontalLayout_3.addWidget(self.pushButtonMakeDataset)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.tableWidgetFilesIC = QTableWidget(self.tab)
        if (self.tableWidgetFilesIC.columnCount() < 3):
            self.tableWidgetFilesIC.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidgetFilesIC.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidgetFilesIC.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidgetFilesIC.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.tableWidgetFilesIC.setObjectName(u"tableWidgetFilesIC")
        self.tableWidgetFilesIC.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_4.addWidget(self.tableWidgetFilesIC)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.pushButtonDeleteFiles = QPushButton(self.tab)
        self.pushButtonDeleteFiles.setObjectName(u"pushButtonDeleteFiles")

        self.horizontalLayout_4.addWidget(self.pushButtonDeleteFiles)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.tabWidgetIC.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_5 = QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(140, 0))
        self.label_5.setMaximumSize(QSize(140, 16777215))
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_6 = QLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(140, 0))
        self.label_6.setMaximumSize(QSize(140, 16777215))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.label_8 = QLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(140, 0))
        self.label_8.setMaximumSize(QSize(140, 16777215))
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBoxSelectedDataset = QComboBox(self.tab_2)
        self.comboBoxSelectedDataset.setObjectName(u"comboBoxSelectedDataset")

        self.horizontalLayout_5.addWidget(self.comboBoxSelectedDataset)

        self.pushButtonUpdateDatasets = QPushButton(self.tab_2)
        self.pushButtonUpdateDatasets.setObjectName(u"pushButtonUpdateDatasets")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonUpdateDatasets.sizePolicy().hasHeightForWidth())
        self.pushButtonUpdateDatasets.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.pushButtonUpdateDatasets)


        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)

        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(140, 0))
        self.label_7.setMaximumSize(QSize(140, 16777215))
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.comboBoxPreTrainedModel = QComboBox(self.tab_2)
        self.comboBoxPreTrainedModel.addItem("")
        self.comboBoxPreTrainedModel.addItem("")
        self.comboBoxPreTrainedModel.addItem("")
        self.comboBoxPreTrainedModel.addItem("")
        self.comboBoxPreTrainedModel.addItem("")
        self.comboBoxPreTrainedModel.setObjectName(u"comboBoxPreTrainedModel")

        self.gridLayout.addWidget(self.comboBoxPreTrainedModel, 2, 1, 1, 1)

        self.label_9 = QLabel(self.tab_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(140, 0))
        self.label_9.setMaximumSize(QSize(140, 16777215))
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.lineEditTrainTitle = QLineEdit(self.tab_2)
        self.lineEditTrainTitle.setObjectName(u"lineEditTrainTitle")

        self.gridLayout.addWidget(self.lineEditTrainTitle, 0, 1, 1, 1)

        self.lineEditEpochs = QLineEdit(self.tab_2)
        self.lineEditEpochs.setObjectName(u"lineEditEpochs")

        self.gridLayout.addWidget(self.lineEditEpochs, 3, 1, 1, 1)

        self.comboBoxImageSize = QComboBox(self.tab_2)
        self.comboBoxImageSize.addItem("")
        self.comboBoxImageSize.addItem("")
        self.comboBoxImageSize.addItem("")
        self.comboBoxImageSize.addItem("")
        self.comboBoxImageSize.addItem("")
        self.comboBoxImageSize.setObjectName(u"comboBoxImageSize")

        self.gridLayout.addWidget(self.comboBoxImageSize, 4, 1, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.pushButtonStartTrain = QPushButton(self.tab_2)
        self.pushButtonStartTrain.setObjectName(u"pushButtonStartTrain")

        self.horizontalLayout_6.addWidget(self.pushButtonStartTrain)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.tabWidgetIC.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_7 = QVBoxLayout(self.tab_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_10 = QLabel(self.tab_3)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_10)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.comboBoxTrainedModels = QComboBox(self.tab_3)
        self.comboBoxTrainedModels.setObjectName(u"comboBoxTrainedModels")

        self.horizontalLayout_7.addWidget(self.comboBoxTrainedModels)

        self.pushButtonRefreshTrainedModels = QPushButton(self.tab_3)
        self.pushButtonRefreshTrainedModels.setObjectName(u"pushButtonRefreshTrainedModels")
        sizePolicy1.setHeightForWidth(self.pushButtonRefreshTrainedModels.sizePolicy().hasHeightForWidth())
        self.pushButtonRefreshTrainedModels.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.pushButtonRefreshTrainedModels)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_7)

        self.label_11 = QLabel(self.tab_3)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_11)

        self.comboBoxConfidence = QComboBox(self.tab_3)
        self.comboBoxConfidence.addItem("")
        self.comboBoxConfidence.addItem("")
        self.comboBoxConfidence.addItem("")
        self.comboBoxConfidence.addItem("")
        self.comboBoxConfidence.addItem("")
        self.comboBoxConfidence.addItem("")
        self.comboBoxConfidence.setObjectName(u"comboBoxConfidence")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBoxConfidence)

        self.label_12 = QLabel(self.tab_3)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_12)

        self.comboBoxInferenceImageSize = QComboBox(self.tab_3)
        self.comboBoxInferenceImageSize.addItem("")
        self.comboBoxInferenceImageSize.addItem("")
        self.comboBoxInferenceImageSize.addItem("")
        self.comboBoxInferenceImageSize.addItem("")
        self.comboBoxInferenceImageSize.addItem("")
        self.comboBoxInferenceImageSize.addItem("")
        self.comboBoxInferenceImageSize.setObjectName(u"comboBoxInferenceImageSize")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBoxInferenceImageSize)


        self.verticalLayout_7.addLayout(self.formLayout)

        self.pushButtonToggleInference = QPushButton(self.tab_3)
        self.pushButtonToggleInference.setObjectName(u"pushButtonToggleInference")

        self.verticalLayout_7.addWidget(self.pushButtonToggleInference)

        self.plainTextEditInferenceResults = QPlainTextEdit(self.tab_3)
        self.plainTextEditInferenceResults.setObjectName(u"plainTextEditInferenceResults")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.plainTextEditInferenceResults.sizePolicy().hasHeightForWidth())
        self.plainTextEditInferenceResults.setSizePolicy(sizePolicy2)
        self.plainTextEditInferenceResults.setMinimumSize(QSize(0, 200))
        self.plainTextEditInferenceResults.setMaximumSize(QSize(16777215, 200))

        self.verticalLayout_7.addWidget(self.plainTextEditInferenceResults)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.tabWidgetIC.addTab(self.tab_3, "")

        self.verticalLayout_3.addWidget(self.tabWidgetIC)

        self.stackedWidgetProject.addWidget(self.page_IC)

        self.verticalLayout.addWidget(self.stackedWidgetProject)


        self.retranslateUi(FormProjectManager)

        self.stackedWidgetProject.setCurrentIndex(1)
        self.tabWidgetOD.setCurrentIndex(0)
        self.tabWidgetIC.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(FormProjectManager)
    # setupUi

    def retranslateUi(self, FormProjectManager):
        FormProjectManager.setWindowTitle(QCoreApplication.translate("FormProjectManager", u"Form", None))
        self.pushButtonCreateProject.setText(QCoreApplication.translate("FormProjectManager", u"Create", None))
        self.pushButtonOpenProject.setText(QCoreApplication.translate("FormProjectManager", u"Open", None))
        self.label.setText(QCoreApplication.translate("FormProjectManager", u"Current project =", None))
        self.labelCurrentProject.setText(QCoreApplication.translate("FormProjectManager", u"...", None))
        self.label_2.setText(QCoreApplication.translate("FormProjectManager", u"Object Detection", None))
        self.label_15.setText(QCoreApplication.translate("FormProjectManager", u"Files ", None))
        self.pushButtonTakeShotsOD.setText(QCoreApplication.translate("FormProjectManager", u"Take shots", None))
        self.pushButtonImpotrOD.setText(QCoreApplication.translate("FormProjectManager", u"Import", None))
        self.pushButtonAnnotateOD.setText(QCoreApplication.translate("FormProjectManager", u"Annotate", None))
        self.pushButtonMakeDatasetOD.setText(QCoreApplication.translate("FormProjectManager", u"Make", None))
        ___qtablewidgetitem = self.tableWidgetFilesOD.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("FormProjectManager", u"#", None));
        ___qtablewidgetitem1 = self.tableWidgetFilesOD.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("FormProjectManager", u"Name", None));
        ___qtablewidgetitem2 = self.tableWidgetFilesOD.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("FormProjectManager", u"Class", None));
        self.tabWidgetOD.setTabText(self.tabWidgetOD.indexOf(self.tabDataset), QCoreApplication.translate("FormProjectManager", u"Dataset", None))
        self.tabWidgetOD.setTabText(self.tabWidgetOD.indexOf(self.tabTrain), QCoreApplication.translate("FormProjectManager", u"Train", None))
        self.label_3.setText(QCoreApplication.translate("FormProjectManager", u"Image Classification", None))
        self.label_4.setText(QCoreApplication.translate("FormProjectManager", u"Files ", None))
        self.pushButtonTakeShots.setText(QCoreApplication.translate("FormProjectManager", u"Take shots", None))
        self.pushButton_2.setText(QCoreApplication.translate("FormProjectManager", u"Import", None))
        self.pushButtonAnnotate.setText(QCoreApplication.translate("FormProjectManager", u"Annotate", None))
        self.pushButtonMakeDataset.setText(QCoreApplication.translate("FormProjectManager", u"Make", None))
        ___qtablewidgetitem3 = self.tableWidgetFilesIC.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("FormProjectManager", u"#", None));
        ___qtablewidgetitem4 = self.tableWidgetFilesIC.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("FormProjectManager", u"Name", None));
        ___qtablewidgetitem5 = self.tableWidgetFilesIC.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("FormProjectManager", u"Class", None));
        self.pushButtonDeleteFiles.setText(QCoreApplication.translate("FormProjectManager", u"Delete", None))
        self.tabWidgetIC.setTabText(self.tabWidgetIC.indexOf(self.tab), QCoreApplication.translate("FormProjectManager", u"Dataset", None))
        self.label_5.setText(QCoreApplication.translate("FormProjectManager", u"Dataset", None))
        self.label_6.setText(QCoreApplication.translate("FormProjectManager", u"Pretrained Moldel", None))
        self.label_8.setText(QCoreApplication.translate("FormProjectManager", u"Image Size", None))
        self.pushButtonUpdateDatasets.setText(QCoreApplication.translate("FormProjectManager", u"Refresh", None))
        self.label_7.setText(QCoreApplication.translate("FormProjectManager", u"Epochs", None))
        self.comboBoxPreTrainedModel.setItemText(0, QCoreApplication.translate("FormProjectManager", u"yolov8n-cls.pt", None))
        self.comboBoxPreTrainedModel.setItemText(1, QCoreApplication.translate("FormProjectManager", u"yolov8s-cls.pt", None))
        self.comboBoxPreTrainedModel.setItemText(2, QCoreApplication.translate("FormProjectManager", u"yolov8m-cls.pt", None))
        self.comboBoxPreTrainedModel.setItemText(3, QCoreApplication.translate("FormProjectManager", u"yolov8l-cls.pt", None))
        self.comboBoxPreTrainedModel.setItemText(4, QCoreApplication.translate("FormProjectManager", u"yolov8x-cls.pt", None))

        self.label_9.setText(QCoreApplication.translate("FormProjectManager", u"Training Title", None))
        self.lineEditEpochs.setText(QCoreApplication.translate("FormProjectManager", u"100", None))
        self.comboBoxImageSize.setItemText(0, QCoreApplication.translate("FormProjectManager", u"160", None))
        self.comboBoxImageSize.setItemText(1, QCoreApplication.translate("FormProjectManager", u"320", None))
        self.comboBoxImageSize.setItemText(2, QCoreApplication.translate("FormProjectManager", u"640", None))
        self.comboBoxImageSize.setItemText(3, QCoreApplication.translate("FormProjectManager", u"720", None))
        self.comboBoxImageSize.setItemText(4, QCoreApplication.translate("FormProjectManager", u"1024", None))

        self.pushButtonStartTrain.setText(QCoreApplication.translate("FormProjectManager", u"Start train", None))
        self.tabWidgetIC.setTabText(self.tabWidgetIC.indexOf(self.tab_2), QCoreApplication.translate("FormProjectManager", u"Train", None))
        self.label_10.setText(QCoreApplication.translate("FormProjectManager", u"Train model", None))
        self.pushButtonRefreshTrainedModels.setText(QCoreApplication.translate("FormProjectManager", u"Refresh", None))
        self.label_11.setText(QCoreApplication.translate("FormProjectManager", u"Confidence", None))
        self.comboBoxConfidence.setItemText(0, QCoreApplication.translate("FormProjectManager", u"0.25", None))
        self.comboBoxConfidence.setItemText(1, QCoreApplication.translate("FormProjectManager", u"0.3", None))
        self.comboBoxConfidence.setItemText(2, QCoreApplication.translate("FormProjectManager", u"0.5", None))
        self.comboBoxConfidence.setItemText(3, QCoreApplication.translate("FormProjectManager", u"0.75", None))
        self.comboBoxConfidence.setItemText(4, QCoreApplication.translate("FormProjectManager", u"0.9", None))
        self.comboBoxConfidence.setItemText(5, QCoreApplication.translate("FormProjectManager", u"1", None))

        self.label_12.setText(QCoreApplication.translate("FormProjectManager", u"Image Size", None))
        self.comboBoxInferenceImageSize.setItemText(0, QCoreApplication.translate("FormProjectManager", u"160", None))
        self.comboBoxInferenceImageSize.setItemText(1, QCoreApplication.translate("FormProjectManager", u"320", None))
        self.comboBoxInferenceImageSize.setItemText(2, QCoreApplication.translate("FormProjectManager", u"640", None))
        self.comboBoxInferenceImageSize.setItemText(3, QCoreApplication.translate("FormProjectManager", u"800", None))
        self.comboBoxInferenceImageSize.setItemText(4, QCoreApplication.translate("FormProjectManager", u"1024", None))
        self.comboBoxInferenceImageSize.setItemText(5, QCoreApplication.translate("FormProjectManager", u"1280", None))

        self.pushButtonToggleInference.setText(QCoreApplication.translate("FormProjectManager", u"Toggle Inference", None))
        self.tabWidgetIC.setTabText(self.tabWidgetIC.indexOf(self.tab_3), QCoreApplication.translate("FormProjectManager", u"Operation", None))
    # retranslateUi

