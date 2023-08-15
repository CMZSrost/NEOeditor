from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTreeWidget


class tabEditor(QTabWidget):
    def __init__(self, parent=None):
        super(tabEditor, self).__init__(parent)

    def item_change(self, item, column):
        idx = self.currentIndex()
        if self.tabText(idx).find('*') == -1:
            self.setTabText(idx, self.tabText(idx) + '*')

    def cell_change(self, i, j):
        idx = self.currentIndex()
        if self.tabText(idx).find('*') == -1:
            self.setTabText(idx, self.tabText(idx) + '*')

    def get_child(self):
        tab = self.currentWidget()
        if tab:
            objName = tab.objectName()
            tree = tab.findChild(QTreeWidget, objName)
            table = tab.findChild(QTableWidget, objName)
            if tree:
                return tree
            elif table:
                return table
