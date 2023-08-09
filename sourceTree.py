import os

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem,QTreeWidgetItemIterator


class sourceTree:
    def __init__(self, treeWidget):
        self.treeWidget:QTreeWidget = treeWidget

    def loadFolder(self, dirPath):
        if os.path.isdir(dirPath):
            root = QTreeWidgetItem()
            root.setText(0, os.path.basename(dirPath))
            self.treeWidget.addTopLevelItem(root)

            def loadFile(dirPath,parent:QTreeWidgetItem):
                for file in os.listdir(dirPath):
                    child = QTreeWidgetItem()
                    child.setText(0, file)
                    parent.addChild(child)
                    if os.path.isdir(os.path.join(dirPath,file)):
                        loadFile(os.path.join(dirPath,file),child)
            loadFile(dirPath,root)
        else:
            root = QTreeWidgetItem()
            root.setText(0, os.path.basename(dirPath))
            self.treeWidget.addTopLevelItem(root)

    def getFilePath(self,idx:QModelIndex):
        #获取对应位置item
        item = self.treeWidget.itemFromIndex(idx)
        path = item.text(0)
        while item.parent() is not None:
            print(path)
            item = item.parent()
            path = os.path.join(item.text(0), path)
        return path

    def filterFile(self,name):
        #遍历所有item
        it = QTreeWidgetItemIterator(self.treeWidget.topLevelItem(0))
        while it.value():
            it.value().setHidden(True)
            it += 1
        it = QTreeWidgetItemIterator(self.treeWidget.topLevelItem(0))
        while it.value():
            item = it.value()
            if item.text(0).find(name) != -1:
                item.setHidden(False)
                while item.parent() is not None:
                    item.parent().setHidden(False)
                    item = item.parent()
                print(item.text(0))
            it += 1
