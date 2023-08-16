from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItemIterator, QMenu, QTreeWidgetItem, QAction

from tableDialog import tableDialog


class dataTree(QTreeWidget):
    def __init__(self, parent=None):
        super(dataTree, self).__init__(parent)
        self.customContextMenuRequested.connect(self.open_menu)
        self.addTableAction = QAction('新增table', self)
        self.copyTableAction = QAction('拷贝table', self)
        self.delTableAction = QAction('删除table', self)
        self.addTableAction.setObjectName('addTableAction')
        self.copyTableAction.setObjectName('copyTableAction')
        self.delTableAction.setObjectName('delTableAction')
        self.addTableAction.triggered.connect(self.add_table)
        self.copyTableAction.triggered.connect(self.copy_table)
        self.delTableAction.triggered.connect(self.del_table)

    def open_menu(self, pos):
        menu = QMenu()
        item = self.currentItem()
        if item:
            if self.currentItem().text(0) == 'database':
                menu.addAction(self.addTableAction)
            elif self.currentItem().text(0) == 'table':
                menu.addAction(self.delTableAction)
                menu.addAction(self.copyTableAction)
            menu.exec_(self.mapToGlobal(pos))

    def add_table(self):
        item: QTreeWidgetItem = self.currentItem()
        dialog = tableDialog(item)
        dialog.exec_()


    def copy_table(self):
        item: QTreeWidgetItem = self.currentItem()
        dialog = tableDialog(item.parent())
        dialog.set_init(item)
        dialog.exec_()

    def del_table(self):
        item: QTreeWidgetItem = self.currentItem()
        print(item.text(0))
        children = [item.child(i) for i in range(item.childCount())]
        for i in children:
            item.removeChild(i)
        item.parent().removeChild(item)
        self.itemChanged.emit(item, 0)

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
