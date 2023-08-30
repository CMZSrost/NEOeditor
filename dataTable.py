from PyQt5.Qt import QTableWidget, QTabWidget
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QDropEvent, QCursor
from PyQt5.QtWidgets import QTableWidgetItem, QToolTip, QAction, QMenu
from numpy import array, where

from xmlIter import get_column


class dataTable(QTableWidget):
    findRecipeSignal = pyqtSignal(str, str)
    findIngredientSignal = pyqtSignal(str, str)

    def __init__(self, parent: QTabWidget = None):
        super(dataTable, self).__init__(parent)
        self.parent = parent
        self.data = array([])
        self.column = []
        self.loaded = self.ptr = 0
        self.toolTips = {}
        self.setup_action()
        self.findRecipeSignal.connect(lambda x: print(x))

    def setup_tooltips(self, tooltips: dict):
        self.toolTips = tooltips

    def show_info(self, i, j):
        item = self.item(i, j)
        if item:
            data = item.data(0)
            print(f'{i},{j}:\t{data}')
        else:
            print(f'{i},{j}:\tit is None')
        # pass

    def show_info_idx(self, idx):
        i, j = idx.row(), idx.column()
        self.show_info(i, j)

    def show_tooltips(self, i, j):
        toolTip = self.toolTips.get(self.column[j])
        if toolTip:
            QToolTip.showText(QCursor.pos(), toolTip)

    def setup_action(self):
        self.findRecipeAction = QAction('查看合成表', self)
        self.findIngredientAction = QAction('查看材料表', self)
        self.findRecipeAction.setObjectName('findRecipeAction')
        self.findIngredientAction.setObjectName('findIngredientAction')
        self.findRecipeAction.triggered.connect(self.emit_findRecipe)
        self.findIngredientAction.triggered.connect(self.emit_findIngredient)

    def emit_findRecipe(self):
        item = self.currentItem()
        if item:
            i, j = item.row(), item.column()
            self.findRecipeSignal.emit(self.data[i, 0], self.data[i, 1])

    def emit_findIngredient(self):
        item = self.currentItem()
        if item:
            i, j = item.row(), item.column()
            self.findIngredientSignal.emit(self.data[i, 0], self.data[i, 1])

    def open_menu(self, pos):
        menu = QMenu()
        item = self.currentItem()
        if item:
            typ = self.objectName().split(':')[-1]
            if typ == 'recipes':
                menu.addAction(self.findRecipeAction)
            elif typ == 'ingredients':
                menu.addAction(self.findIngredientAction)

        if len(menu.actions()) > 0:
            menu.exec_(self.mapToGlobal(pos))

    def setup(self, data, modInfo: str, typ: str, proxyFunc=None):
        self.clear()
        self.column, self.data = get_column(typ), data
        self.setObjectName(modInfo + ':' + typ)
        print(data.shape)

        self.setColumnCount(self.data.shape[1])
        self.setHorizontalHeaderLabels(self.column)

        self.load_data(data)

        # proxyFunc(data=self.data, table=self)

    def load_data(self, data, column=None):
        if column:
            self.setColumnCount(len(column))
            self.setHorizontalHeaderLabels(column)
        self.setRowCount(data.shape[0])
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = QTableWidgetItem(data[i, j])
                self.setItem(i, j, item)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def update_data(self, gameData):
        temp = []
        modInfo, typ = self.objectName().split(':')
        for i in range(self.rowCount()):
            temp.append([self.item(i, j).data(0) for j in range(self.columnCount())])
        self.data = array(temp, dtype=str)
        if modInfo == 'total':
            for modName, modData in gameData.items():
                data = self.data[where(self.data[:, 0] == modName)]
                modData[typ] = data
        else:
            gameData[modInfo][typ] = self.data

    def fresh(self, item):
        self.resizeColumnToContents(item.column())
        self.resizeRowToContents(item.row())

    def find_text(self, text):
        self.setSortingEnabled(False)
        for i in range(self.rowCount()):
            flag = False
            for j in range(self.columnCount()):
                if self.item(i, j) and text == '' or self.item(i, j).data(0).find(text) != -1:
                    flag = True
                    break
            self.showRow(i) if flag else self.hideRow(i)
        self.setSortingEnabled(True)

    def add_line(self):
        idx = self.currentRow()
        if idx >= 0:
            self.setSortingEnabled(False)
            data = [self.item(idx, i).text() if self.item(idx, i) else '' for i in range(self.columnCount())]
            self.insertRow(idx + 1)
            for i in range(1, self.columnCount() - 1):
                self.setItem(idx + 1, i, QTableWidgetItem(''))
            self.setItem(idx + 1, 0, QTableWidgetItem(data[0]))
            if self.column[self.columnCount() - 1] == 'filepath':
                self.setItem(idx + 1, self.columnCount() - 1, QTableWidgetItem(data[-1]))
            else:
                self.setItem(idx + 1, self.columnCount() - 1, QTableWidgetItem(''))
            self.setCurrentCell(idx + 1, 0)
            self.setSortingEnabled(True)

    def delete_line(self):
        idx = self.currentRow()
        print(idx)
        if idx >= 0:
            self.setSortingEnabled(False)
            self.removeRow(idx)
            self.cellChanged.emit(idx, 0)
            self.setCurrentCell(idx - 1, 0)
            self.setSortingEnabled(True)

    def copy_line(self):
        idx = self.currentRow()
        print(idx)
        if idx >= 0:
            self.setSortingEnabled(False)
            data = [self.item(idx, i).text() if self.item(idx, i) else '' for i in range(self.columnCount())]
            print(data)
            self.insertRow(idx + 1)
            for i in range(self.columnCount()):
                self.setItem(idx + 1, i, QTableWidgetItem(data[i]))
            self.setCurrentCell(idx + 1, 0)
            self.setSortingEnabled(True)

    def dropEvent(self, event: QDropEvent) -> None:
        src = self.currentRow()
        if src >= 0:
            select = self.itemAt(event.pos())
            if select:
                dst = select.row()
                if src > dst:
                    src += 1
                elif src < dst:
                    dst += 1
            else:
                dst = self.rowCount()
            self.insertRow(dst)
            for i in range(self.columnCount()):
                item = self.item(src, i)
                if item:
                    self.setItem(dst, i, QTableWidgetItem(item.text()))
                else:
                    self.setItem(dst, i, QTableWidgetItem(''))
            self.removeRow(src)
