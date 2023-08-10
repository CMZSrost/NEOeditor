import numpy as np
from PyQt5.Qt import QTableWidget, QTabWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QTableWidgetItem


class NewTable(QTableWidget):
    def __init__(self, parent: QTabWidget = None, QString=None):
        super(NewTable, self).__init__(parent)
        self.parent = parent
        self.verticalScrollBar().valueChanged['int'].connect(self.update)
        self.loaded = 0
        self.ptr = 0

    def showinfo(self, i, j):
        print(f'{i},{j}:\t{self.sender().item(i, j).data(0)}')
        # pass

    def setup(self, DB, modinfo: str):
        if self.columnCount() != 0:
            return
        self.setHorizontalHeaderLabels(DB.column)
        self.data = DB.data
        self.setRowCount(self.data.shape[0])
        self.setColumnCount(self.data.shape[1])
        self.setHorizontalHeaderLabels(DB.column)
        self.setObjectName(modinfo+'_'+DB.type)
        self.modinfo = modinfo
        self.horizontalHeader().stretchLastSection()
        self.verticalScrollBar().valueChanged['int'].connect(self.load)

        for i in range(self.data.shape[0]):
            self.hideRow(i)

        self.loadData(35)


    def loadline(self,i):
        for j in range(self.data.shape[1]):
            self.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))

    def load(self, value):
        if value-self.loaded>=10:
            self.loadData(value)

    def loadData(self,ind):
        while self.loaded < ind and self.ptr < self.data.shape[0]:
            if self.data[self.ptr, 0] == self.modinfo or self.modinfo == 'total':
                self.loadline(self.ptr)
                self.showRow(self.ptr)
                self.loaded += 1
            else:
                self.hideRow(self.ptr)
            self.ptr += 1
        self.resizeColumnsToContents()
        self.resizeRowsToContents()


    def filterData(self, modinfo:str, reverse=True):
        if modinfo == 'total':
            ind = np.full(self.data.shape[0],True)
        else:
            ind = self.data[:, self.column.index('modinfo')] == modinfo
        if reverse:
            ind = ~ind
        ind = np.where(ind)[0]
        return ind

    def fresh(self,item):
        self.resizeColumnToContents(item.column())
        self.resizeRowToContents(item.row())

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