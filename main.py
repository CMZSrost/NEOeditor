import sys
import os

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *
from Editor_UI import UI_main, UI_fileTab
from EditorDB import EditorDB
from dataTableUI import NewTable
from threadProxy import threadProxy


class mainUI(QMainWindow, UI_main.Ui_main):
    def __init__(self):
        super(mainUI, self).__init__()
        self.setupUi(self)
        self.proxy = threadProxy()
        self.db = EditorDB(fileTreeWidget=self.treeWidget_file,
                           dataTreeWidget=self.treeWidget_data,
                           proxy=self.proxy,
                           statusBar=self.statusbar)
        self.templateTab = UI_fileTab.Ui_templateTab()
        self.proxy.loadingStatusSign.connect(self.loaded)


    def load_project(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", self.db.projectPath)
        if os.path.isdir(path):
            self.db.load_project(path)
            self.treeWidget_file.setEnabled(True)
            self.lineEdit_file.setEnabled(True)

    def loaded(self, flag):
        print(flag)
        if flag == 0:
            for i in self.db.gameData:
                self.db.gameData[i] = self.db.gameData[i][np.argsort(self.db.gameData[i][:, 0]),:]

            self.treeWidget_data.setEnabled(True)
            self.lineEdit_data.setEnabled(True)
            self.treeWidget_data.setRootIsDecorated(True)
        else:
            self.treeWidget_data.setEnabled(False)
            self.lineEdit_data.setEnabled(False)

    @staticmethod
    def expand_node(tree, idx):
        tree.setExpanded(idx, not tree.isExpanded(idx))

    def double_click(self, idx):
        if self.sender() == self.treeWidget_file:
            filePath = self.db.fileTree.get_file_path(idx)
            path = os.path.join(self.db.projectPath, filePath)
            if os.path.isfile(path):
                fileName = os.path.basename(path)
                if fileName.endswith('xml'):
                    tab = self.tab_factory(filePath, self.fileEditor, 'filetab')
                    if tab:
                        tree = tab.findChild(QTreeWidget, 'treeWidget')
                        tree.sortByColumn(3, Qt.AscendingOrder)
                        self.db.load_file(path, tree)

                elif fileName.endswith('php'):
                    tab = self.tab_factory(fileName, self.fileEditor, 'datatab')
                    if tab:
                        table = tab.findChild(QTableWidget, 'tableWidget')
                        self.db.load_php(path, table)

            elif os.path.isdir(path):
                self.treeWidget_file.setExpanded(idx, not self.treeWidget_file.isExpanded(idx))

        elif self.sender() == self.treeWidget_data:

            pathList = os.path.split(self.db.dataTree.get_file_path(idx))
            if len(pathList) == 1:
                self.treeWidget_data.setExpanded(idx, not self.treeWidget_data.isExpanded(idx))
                return
            modInfo, typ = pathList[0], pathList[1]

            if modInfo == '':
                self.treeWidget_data.setExpanded(idx, not self.treeWidget_data.isExpanded(idx))
                return
            else:
                tab = self.tab_factory('_'.join(pathList), self.elemEditor, 'datatab')
                if tab:
                    table = tab.findChild(NewTable, 'tableWidget')
                    table.setup(self.db.gameData[typ], modInfo, typ)
                    table.cellChanged['int', 'int'].connect(self.elemEditor.item_change)

    def tab_factory(self, tabName, tabParent: QTabWidget, typ):
        templateTab = QTabWidget()
        fileName = os.path.basename(tabName)
        tablist = [tabParent.tabText(i) for i in range(tabParent.count())]
        if tabName in tablist:
            tabParent.setCurrentIndex(tablist.index(tabName))
            return
        self.templateTab.setupUi(templateTab)
        pos = templateTab.findChild(QWidget, typ)
        pos.setObjectName(tabParent.objectName() + '_' + fileName)
        tabParent.addTab(pos, tabName)
        templateTab.clear()
        return pos

    def remove_file_tab(self, idx):
        self.fileEditor.removeTab(idx)

    def remove_data_tab(self, idx):
        if self.elemEditor.tabText(idx).find('*') != -1:
            print(idx)
        self.elemEditor.removeTab(idx)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Form = mainUI()
    Form.show()
    exit(app.exec_())
