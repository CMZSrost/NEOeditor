from PyQt5.Qt import QTableWidget, QTabWidget
from PyQt5.QtCore import pyqtSignal


class NewTable(QTableWidget):
    def __init__(self, parent: QTabWidget = None, QString=None):
        super(NewTable, self).__init__(parent)
        self.parent = parent

    def showinfo(self, i, j):
        print(f'{i},{j}:\t{self.sender().item(i, j).data(0)}')

    def findText(self, text):
        for i in range(self.rowCount()):
            flag = False
            for j in range(self.columnCount()):
                if self.item(i, j) is None:
                    break
                if text == '' or self.item(i, j).data(0).find(text) != -1:
                    flag = True
                    break
            if flag:
                self.showRow(i)
            else:
                self.hideRow(i)
