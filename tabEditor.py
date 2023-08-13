from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QTabWidget, QTableWidget


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
