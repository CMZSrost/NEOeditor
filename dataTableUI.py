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
        self.setObjectName(modInfo + '_' + typ)
        print(data.shape)

        self.setRowCount(self.data.shape[0])
        self.setColumnCount(self.data.shape[1])

        self.setHorizontalHeaderLabels(self.column)
        self.horizontalHeader().stretchLastSection()
        # self.verticalScrollBar().valueChanged['int'].connect(self.load)

        proxyFunc(data=self.data, table=self)

    def load_line(self, i):
        for j in range(self.data.shape[1]):
            self.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))

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
