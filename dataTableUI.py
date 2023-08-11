from PyQt5.Qt import QTableWidget, QTabWidget
from PyQt5.QtWidgets import QTableWidgetItem
from xmlIter import get_column


class NewTable(QTableWidget):
    def __init__(self, parent: QTabWidget = None):
        super(NewTable, self).__init__(parent)
        self.parent = parent
        self.data, self.column = None, []
        self.loaded = self.ptr = 0

    def show_info(self, i, j):
        print(f'{i},{j}:\t{self.sender().item(i, j).data(0)}')
        # pass

    def setup(self, data, modInfo: str, typ: str):
        if self.columnCount() != 0:
            return
        self.column, self.data = get_column(typ), data
        self.setObjectName(modInfo + '_' + typ)
        print(data.shape)

        self.setRowCount(self.data.shape[0])
        self.setColumnCount(self.data.shape[1])

        self.setHorizontalHeaderLabels(self.column)
        self.horizontalHeader().stretchLastSection()
        self.verticalScrollBar().valueChanged['int'].connect(self.load)

        for i in range(self.data.shape[0]):
            self.hideRow(i)

        self.load_data(35)

    def load_line(self, i):
        for j in range(self.data.shape[1]):
            self.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))

    def load(self, value):
        ind = value + 35
        if ind - self.loaded >= 10:
            self.load_data(ind)

    def load_data(self, ind):
        modInfo = self.objectName().rsplit('_', 1)[0]
        print(modInfo)
        while self.loaded < ind and self.ptr < self.data.shape[0]:
            if self.data[self.ptr, 0] == modInfo or modInfo == 'total':
                self.load_line(self.ptr)
                self.showRow(self.ptr)
                self.loaded += 1
            else:
                self.hideRow(self.ptr)
            self.ptr += 1

        if self.ptr == self.data.shape[0]:
            self.setSortingEnabled(True)
            self.horizontalHeader().setSortIndicatorShown(True)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

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
