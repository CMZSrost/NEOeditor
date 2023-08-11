from os.path import join, isdir, basename
from os import listdir

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator


class sourceTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.self = parent

    def add_node(self, data, parent=None):
        node = QTreeWidgetItem()
        node.setText(0, data)
        if parent:
            parent.addChild(node)
        else:
            self.addTopLevelItem(node)
        return node

    def load_folder(self, dirPath):
        def load_file(fPath, parent: QTreeWidgetItem):
            for file in listdir(fPath):
                child = self.add_node(file, parent)
                if isdir(join(fPath, file)):
                    load_file(join(fPath, file), child)

        root = self.add_node(basename(dirPath))
        if isdir(dirPath):
            load_file(dirPath, root)

    def load_data(self, top, lst):
        topItem = self.add_node(top)
        for i in lst:
            self.add_node(i, topItem)

    def get_file_path(self, idx: QModelIndex):
        item = self.itemFromIndex(idx)
        path = item.text(0)
        while item.parent() is not None:
            item = item.parent()
            path = join(item.text(0), path)
        return path.replace('\\', '/')

    def filter_file(self, name):
        it = QTreeWidgetItemIterator(self.topLevelItem(0))
        while it.value():
            it.value().setHidden(True)
            it += 1
        it = QTreeWidgetItemIterator(self.topLevelItem(0))
        while it.value():
            item = it.value()
            if item.text(0).find(name) != -1:
                item.setHidden(False)
                while item.parent() is not None:
                    item.parent().setHidden(False)
                    item = item.parent()
            it += 1
