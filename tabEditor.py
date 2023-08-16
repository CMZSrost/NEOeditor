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
            tree = tab.findChild(QTreeWidget)
            table = tab.findChild(QTableWidget)
            if tree:
                return tree
            elif table:
                return table
