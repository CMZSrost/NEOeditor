import numpy as np
from PyQt5.Qt import QTableWidget, QTabWidget
from PyQt5.QtWidgets import QTableWidgetItem
from xmlIter import get_column


class dataTable(QTableWidget):
    def __init__(self, parent: QTabWidget = None):
        super(dataTable, self).__init__(parent)
        self.parent = parent
        self.data = np.array([])
        self.column = []
        self.loaded = self.ptr = 0

    def show_info(self, i, j):
        item = self.item(i, j)
        if item:
            data = item.data(0)
            print(f'{i},{j}:\t{data}')
        else:
            print(f'{i},{j}:\tit is None')
        # pass

    def setup(self, data, modInfo: str, typ: str, proxyFunc):
        if self.columnCount() != 0:
            return
        self.column, self.data = get_column(typ), data
        self.setObjectName(modInfo + ':' + typ)
        print(data.shape)

        self.setRowCount(self.data.shape[0])
        self.setColumnCount(self.data.shape[1])

        self.setHorizontalHeaderLabels(self.column)
        self.horizontalHeader().stretchLastSection()

        proxyFunc(data=self.data, table=self)

    def update_data(self, gameData):
        temp = []
        modInfo, typ = self.objectName().split(':')
        for i in range(self.rowCount()):
            temp.append([self.item(i, j).data(0) for j in range(self.columnCount())])
        self.data = np.array(temp, dtype=str)
        if modInfo == 'total':
            for modName, modData in gameData.items():
                data = self.data[np.where(self.data[:, 0] == modName)]
                modData[typ] = data
        else:
            gameData[modInfo][typ] = self.data


    def fresh(self, item):
        self.resizeColumnToContents(item.column())
        self.resizeRowToContents(item.row())

    def find_text(self, text):
        for i in range(self.rowCount()):
            flag = False
            for j in range(self.columnCount()):
                if self.item(i, j) and text == '' or self.item(i, j).data(0).find(text) != -1:
                    flag = True
                    break
            self.showRow(i) if flag else self.hideRow(i)
