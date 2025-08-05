from PySide6.QtWidgets import QDialog, QFileDialog
from widgets.create_project_dialog_ui import Ui_CreateProjectDialog

class CreateProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_CreateProjectDialog()
        self.ui.setupUi(self)

        self.ui.pushButtonBrowse.clicked.connect(self.browse_directory)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.ui.lineEditProjectDir.setText(directory)

    def get_project_data(self):
        return {
            "name": self.ui.lineEditProjectName.text(),
            "type": self.ui.comboBoxProjectType.currentText(),
            "directory": self.ui.lineEditProjectDir.text()
        }