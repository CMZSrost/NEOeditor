from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QTableWidgetItem

from Editor_UI import UI_help


class helpDialog(QDialog, UI_help.Ui_help):
    def __init__(self, helps, parent=None):
        super(helpDialog, self).__init__(parent)
        self.setupUi(self)
        self.helps = helps
        model = QStringListModel()
        model.setStringList(list(self.helps.keys()))
        self.listView_key.setModel(model)
        self.setWindowFlags(Qt.Window)

    def show_value(self, index):
        self.textBrowser.clear()
        self.textBrowser.setText(self.helps[self.listView_key.model().stringList()[index.row()]])





