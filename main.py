import sys
import os

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *

import sourceTree
from Editor_UI import UI_main, UI_fileTab
from EditorDB import EditorDB
from dataTable import dataTable
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
        if flag == 0:
            self.treeWidget_data.setEnabled(True)
            self.lineEdit_data.setEnabled(True)
            self.treeWidget_data.setRootIsDecorated(True)
        else:
            self.treeWidget_data.setEnabled(False)
            self.lineEdit_data.setEnabled(False)

    @staticmethod
    def expand_node(tree, idx):
        tree.setExpanded(idx, not tree.isExpanded(idx))

    def get_chlid(self, tab, path, **kwargs):
        if tab:
            classType = kwargs['classType']
            className = kwargs['className']
            func = kwargs['func']
            child = tab.findChild(classType, className)
            func(path, child)

    def double_click(self, idx):
        if isinstance(self.sender(), sourceTree.sourceTree):
            pathList = os.path.split(self.sender().get_file_path(idx))
            path = os.path.join(self.db.projectPath, *pathList)
            if os.path.isfile(path):
                tempMap = {'xml': {'tabName': 'filetab', 'classType': QTreeWidget,
                                   'className': 'treeWidget', 'func': self.db.load_file},
                           'php': {'tabName': 'datatab', 'classType': QTableWidget,
                                   'className': 'tableWidget', 'func': self.db.load_php}}
                kwargs = tempMap[pathList[-1].split('.')[-1]]
                self.get_chlid(self.tab_factory(pathList, self.fileEditor, kwargs['tabName']), path, **kwargs)

            elif os.path.isdir(path) or len(pathList) == 1 or pathList[0] == '':
                self.expand_node(self.sender(), idx)

            else:
                [modInfo, typ] = pathList
                tab = self.tab_factory(pathList, self.elemEditor, 'datatab')
                if tab:
                    table = tab.findChild(dataTable, 'tableWidget')
                    if modInfo == 'total':
                        gameData = np.vstack([self.db.gameData[i][typ] for i in self.db.gameData.keys() if
                                              typ in self.db.gameData[i].keys()])
                    else:
                        gameData = self.db.gameData[modInfo][typ]
                    table.setup(gameData, modInfo, typ, self.proxy.setup_data)
                    table.cellChanged['int', 'int'].connect(self.elemEditor.item_change)

    def tab_factory(self, pathList, tabParent: QTabWidget, typ):
        templateTab = QTabWidget()
        objName = f'{os.path.join(*pathList[:-1])}:{pathList[-1]}'
        objList = [tabParent.tabText(i) for i in range(tabParent.count())]
        check = self.check_object_name(objName, objList)
        if check != -1:
            tabParent.setCurrentIndex(check)
            return
        self.templateTab.setupUi(templateTab)
        pos = templateTab.findChild(QWidget, typ)
        pos.setObjectName(objName)
        tabParent.addTab(pos, objName)
        templateTab.clear()
        return pos

    def check_object_name(self, objName, objList):
        if objName in objList:
            return objList.index(objName)
        if objName.startswith('total'):
            for i in objList:
                if ~i.startswith('total') and i.endswith(objName.split(':')[1]):
                    return objList.index(i)
        return -1

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
