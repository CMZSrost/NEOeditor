from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItemIterator
from PyQt5.QtCore import Qt

class dataTree(QTreeWidget):
    def __init__(self, parent=None):
        super(dataTree, self).__init__(parent)

    def filter_file(self, name):
        it = QTreeWidgetItemIterator(self.topLevelItem(0))
        while it.value():
            it.value().setHidden(True)
            it += 1
        it = QTreeWidgetItemIterator(self.topLevelItem(0))
        while it.value():
            item = it.value()
            if any([item.text(i).find(name) != -1 for i in range(item.columnCount())]):
                item.setHidden(False)
                while item.parent() is not None:
                    item.parent().setHidden(False)
                    item = item.parent()
            it += 1
