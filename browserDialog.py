import numpy as np
from PyQt5.QtCore import QStringListModel, QModelIndex, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from Editor_UI import UI_browser
from xmlIter import get_keys, get_column


class BrowserDialog(QDialog, UI_browser.Ui_browser):
    def __init__(self, gameData, parent=None):
        super(BrowserDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.gameData = gameData
        self.setWindowFlags(Qt.Window)
        model = QStringListModel()
        model.setStringList(get_keys())
        self.listView_type.setModel(model)
        self.check = {}


    def get_stack(self):
        data = {}
        for i in self.gameData:
            for j in self.gameData[i]:
                data[j] = np.vstack([data[j], self.gameData[i][j]]) if j in data else self.gameData[i][j]
        return data

    def double_click(self, index:QModelIndex):
        self.comboBox.clear()
        self.check.clear()
        self.checkBox.setChecked(True)
        self.tableWidget_data.clear()

        column = get_column(str(index.data()))
        self.check.update({i: True for i in column})
        self.comboBox.addItems(column)
        self.comboBox.setCurrentIndex(0)

        data = self.get_stack().get(str(index.data()), np.array([]))
        if data.size != 0:
            self.tableWidget_data.setRowCount(data.shape[0])
            self.tableWidget_data.setColumnCount(data.shape[1])
            self.tableWidget_data.setHorizontalHeaderLabels(column)
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    self.tableWidget_data.setItem(i, j, QTableWidgetItem(data[i][j]))
            self.tableWidget_data.resizeColumnsToContents()
            self.tableWidget_data.resizeRowsToContents()
        else:
            self.tableWidget_data.setRowCount(0)
            self.tableWidget_data.setColumnCount(0)
            self.tableWidget_data.setHorizontalHeaderLabels([])

    def checkbox_change(self, state):
        if self.comboBox.currentText() in self.check:
            self.check[self.comboBox.currentText()] = state
            self.tableWidget_data.setColumnHidden(self.comboBox.currentIndex(), not state)
        else:
            print('combox error')

    def combox_change(self, text):
        if text in self.check:
            self.checkBox.setChecked(self.check[text])
        else:
            print('check error')
