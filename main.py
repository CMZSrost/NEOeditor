import sys
import os

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *

import sourceTree
from Editor_UI import UI_main, UI_fileTab
from EditorDB import EditorDB
from dataTable import dataTable
from dataTree import dataTree
from tabEditor import tabEditor
from threadProxy import threadProxy
from templateTab import templateTab


class mainUI(QMainWindow, UI_main.Ui_main):
    def __init__(self):
        super(mainUI, self).__init__()
        self.setupUi(self)
        self.proxy = threadProxy()
        self.db = EditorDB(fileTreeWidget=self.treeWidget_file,
                           dataTreeWidget=self.treeWidget_data,
                           proxy=self.proxy,
                           statusBar=self.statusbar)
        self.templateTab = templateTab()
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
            func = kwargs['func']
            child = tab.findChild(classType)
            child.setObjectName(tab.objectName())
            func(path, child)
            return child

    def double_click(self, idx):
        if isinstance(self.sender(), sourceTree.sourceTree):
            pathList = os.path.split(self.sender().get_file_path(idx))
            path = os.path.join(self.db.projectPath, *pathList)
            if os.path.isfile(path):
                tempMap = {'xml': {'tabName': 'filetab', 'classType': dataTree, 'func': self.db.load_file},
                           'php': {'tabName': 'datatab', 'classType': dataTable, 'func': self.db.load_php}}
                extend = pathList[-1].split('.')[-1]
                kwargs = tempMap[extend]
                tab = self.tab_factory(pathList, self.fileEditor, kwargs['tabName'])
                child = self.get_chlid(tab, path, **kwargs)
                if child:
                    if extend == 'xml':
                        child.itemChanged['QTreeWidgetItem*', 'int'].connect(self.fileEditor.item_change)
                    elif extend == 'php':
                        child.cellChanged['int', 'int'].connect(self.elemEditor.cell_change)

            elif os.path.isdir(path) or len(pathList) == 1 or pathList[0] == '':
                self.expand_node(self.sender(), idx)

            else:
                [modInfo, typ] = pathList
                self.tab_factory(pathList, self.elemEditor, 'datatab')
                table = self.elemEditor.get_child()
                if table:
                    if modInfo == 'total':
                        gameData = np.vstack([self.db.gameData[i][typ] for i in self.db.gameData.keys() if
                                              typ in self.db.gameData[i].keys()])
                    else:
                        gameData = self.db.gameData[modInfo][typ]
                    table.setup(gameData, modInfo, typ, self.proxy.setup_data)
                    table.cellChanged['int', 'int'].connect(self.elemEditor.item_change)

    def tab_factory(self, pathList, tabParent: tabEditor, typ):
        templateTab = QTabWidget()
        objName = f'{os.path.join(*pathList[:-1])}:{pathList[-1]}'
        objList = [tabParent.tabText(i) for i in range(tabParent.count())]
        check = self.check_object_name(objName, objList)
        if check != -1:
            tabParent.setCurrentIndex(check)
            return
        self.templateTab.setup(templateTab)
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

    def reload(self):
        # Editor =
        tree = self.fileEditor.get_child()
        if tree:
            filePath = os.path.join(self.db.Path['project'], tree.objectName().replace(':', os.sep))
            self.db.load_file(filePath, tree)
            self.fileEditor.setTabText(self.fileEditor.currentIndex(), tree.objectName())
        table = self.elemEditor.get_child()
        if table:
            modInfo, typ = table.objectName().split(':')
            table.setup(table.data, modInfo, typ, self.proxy.setup_data)
            self.elemEditor.setTabText(self.elemEditor.currentIndex(), table.objectName())

    def remove_file_tab(self, idx):
        if self.fileEditor.tabText(idx).find('*') != -1:
            reply = QMessageBox.question(self, '数据未保存', '你想保存数据吗',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                currentTab = self.fileEditor.widget(idx)
                objName = currentTab.objectName()
                tree = currentTab.findChild(dataTree)
                mods = dict(self.db.getMods)
                modsKey = [f'{k}_{i}' for k, i in enumerate(mods.keys())]
                modsKey = ['-_data', *modsKey]
                modsValue = list(mods.values())
                modsValue = ['data', *modsValue]
                modInfo = modsKey[modsValue.index(objName.split(':')[0])]
                self.db.write_file_from_tree(tree, self.db.gameData[modInfo], modInfo)
            elif reply == QMessageBox.Cancel:
                return
        self.fileEditor.removeTab(idx)

    def remove_data_tab(self, idx):
        if self.elemEditor.tabText(idx).find('*') != -1:
            reply = QMessageBox.question(self, '数据未保存', '你想保存数据吗',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                currentTab = self.elemEditor.widget(idx)
                table = currentTab.findChild(dataTable)
                table.update_data(self.db.gameData)
                self.db.write_file_from_data(table.data, table.objectName().split(':')[1])
            elif reply == QMessageBox.Cancel:
                return
        self.elemEditor.removeTab(idx)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Form = mainUI()
    Form.show()
    exit(app.exec_())
