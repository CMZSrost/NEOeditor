import os.path
from os import listdir
from os.path import join, isdir, basename

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QToolTip, QAction, QMenu


class sourceTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.path = ''
        self.tooltips = {}

    def setup_actions(self):
        self.loadProjectAction = self.actions()[0]
        self.openFolderAction = QAction('打开文件(夹)', self)
        self.openFolderAction.setObjectName('openFolderAction')
        self.openFolderAction.triggered.connect(self.open_folder)

    def open_folder(self):
        path = self.get_file_path(self.currentIndex()).replace('/', '\\')
        path = os.path.join(self.path, path)

        if os.path.exists(path):
            #打开文件
            os.startfile(path)
        else:
            print('not a file')
            print(path)

    def open_menu(self, pos):
        menu = QMenu()
        item = self.itemAt(pos)
        if item:
            menu.addAction(self.openFolderAction)
        else:
            menu.addAction(self.loadProjectAction)

        if len(menu.actions()) > 0:
            menu.exec_(self.mapToGlobal(pos))

    def setup_tooltips(self,tooltips:dict):
        tips = [i.get('#') for i in tooltips.values()]
        self.tooltips = dict(zip(tooltips.keys(), tips))

    def show_tooltips(self, item:QTreeWidgetItem):
        if item.text(0) in self.tooltips:
            QToolTip.showText(QCursor.pos(), self.tooltips[item.text(0)])


    def get_top_item(self, name):
        namelist = [self.topLevelItem(i).text(0) for i in range(self.topLevelItemCount())]
        return self.topLevelItem(namelist.index(name))

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
        if not idx.isValid():
            return ''
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

