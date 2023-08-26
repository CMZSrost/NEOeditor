import json
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from numpy import vstack

from EditorDB import EditorDB
from Editor_UI import UI_main
from dataTable import dataTable
from dataTree import dataTree
from loggerMsg import logInit
from sourceTree import sourceTree
from tabEditor import tabEditor
from templateTab import templateTab
from helpDialog import helpDialog
from threadProxy import threadProxy


# nuitka --show-memory --show-progress --plugin-enable=pyqt5 --follow-import-to=Editor_UI --onefile --output-dir=out main.py

class mainUI(QMainWindow, UI_main.Ui_main):
    def __init__(self):
        super(mainUI, self).__init__()
        self.comments, self.config = None, None
        self.setupUi(self)

        self.load_json()
        self.trans = QTranslator(self)
        self.proxy = threadProxy()
        self.templateTab = templateTab()
        self.db = EditorDB(MainWindow=self, proxy=self.proxy, config=self.config)
        self.setup_connection()

    def load_json(self):
        with open(os.path.join(os.getcwd(), 'config.json'), 'r', encoding='UTF-8') as f:
            self.config = json.load(f)
        with open(os.path.join(os.getcwd(), 'jsonData', 'NEOcomments.json'), 'r', encoding='UTF-8') as f:
            self.comments = json.load(f)
        with open(os.path.join(os.getcwd(), 'jsonData', 'NEOhelps.json'), 'r', encoding='UTF-8') as f:
            self.helps = json.load(f)

    def recipe_analysis(self):
        self.db.recipes_analysis()

    def recipe_show(self):
        if self.db.recipes is None:
            QMessageBox.information(self, '提示', '请先加载数据')
            return
        self.db.recipes.show()

    def setup_connection(self):
        self.languageAction.setChecked(True if self.config['language'] == 'zh_CN' else False)
        self.addAction(self.saveFileAction)
        self.treeWidget_file.addAction(self.loadProjectAction)
        self.proxy.loadingStatusSign.connect(self.loaded)
        self.treeWidget_data.setup_tooltips(self.comments)

    def change_language(self, toggle):
        transPath = os.path.join(os.getcwd(), 'jsonData')
        if toggle:
            self.trans.load("zh_CN", transPath)
        else:
            self.trans.load("en", transPath)
        app = QApplication.instance()
        app.installTranslator(self.trans)
        self.retranslateUi(self)

    def load_project(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", self.db.Path['project'])
        if os.path.isdir(path):
            self.db.load_project(path)
            self.treeWidget_file.setEnabled(True)
            self.lineEdit_file.setEnabled(True)

    def loaded(self, flag):
        if flag == 0:
            self.treeWidget_data.setEnabled(True)
            self.lineEdit_data.setEnabled(True)
            self.treeWidget_data.setRootIsDecorated(True)
            self.recipesAnalysisAction.setEnabled(True)
        else:
            self.treeWidget_data.setEnabled(False)
            self.lineEdit_data.setEnabled(False)

    @staticmethod
    def expand_node(tree, idx):
        tree.setExpanded(idx, not tree.isExpanded(idx))

    @staticmethod
    def get_chlid(tab, path, **kwargs):
        if tab:
            classType = kwargs['classType']
            func = kwargs['func']
            child = tab.findChild(classType)
            child.setObjectName(tab.objectName())
            func(path, child)
            return child

    def help(self):
        # QMessageBox.about(self, '帮助', '请联系作者')
        helpD = helpDialog(self.helps, self)
        helpD.show()

    def double_click(self, idx):
        if isinstance(self.sender(), sourceTree):
            pathList = os.path.split(self.sender().get_file_path(idx))
            path = os.path.join(self.db.Path['project'], *pathList)
            print(path)
            if os.path.isfile(path):
                tempMap = {'xml': {'tabName': 'filetab', 'classType': dataTree, 'func': self.db.load_file},
                           'php': {'tabName': 'datatab', 'classType': dataTable, 'func': self.db.load_php}}
                extend = pathList[-1].split('.')[-1]
                if extend not in tempMap:
                    return
                kwargs = tempMap[extend]
                tab = self.tab_factory(pathList, self.fileEditor, kwargs['tabName'])
                child = self.get_chlid(tab, path, **kwargs)
                if child:
                    if extend == 'xml':
                        child.itemChanged['QTreeWidgetItem*', 'int'].connect(self.fileEditor.item_change)
                    elif extend == 'php':
                        child.cellChanged['int', 'int'].connect(self.fileEditor.cell_change)

            elif os.path.isdir(path) or len(pathList) == 1 or pathList[0] == '':
                self.expand_node(self.sender(), idx)

            else:
                [modInfo, typ] = pathList
                try:
                    table = self.tab_factory(pathList, self.elemEditor, 'datatab').findChild(dataTable)
                except AttributeError:
                    print('AttributeError')
                    table = None
                if table:
                    if modInfo == 'total':
                        gameData = vstack([self.db.gameData[i][typ] for i in self.db.gameData.keys() if
                                           typ in self.db.gameData[i].keys()])
                    else:
                        gameData = self.db.gameData[modInfo][typ]
                    table.setup(gameData, modInfo, typ, self.proxy.setup_data)
                    table.setup_tooltips(self.comments[typ])
                    table.cellChanged['int', 'int'].connect(self.elemEditor.item_change)

    def tab_factory(self, pathList, tabParent: tabEditor, typ):
        templateTab = QTabWidget()
        objName = f'{os.path.join(*pathList[:-1])}:{pathList[-1]}'
        print(objName)
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

    @staticmethod
    def check_object_name(objName, objList):
        if objName in objList:
            return objList.index(objName)
        if objName.startswith('total'):
            for i in objList:
                if ~i.startswith('total') and i.endswith(objName.split(':')[1]):
                    return objList.index(i)
        else:
            for i in objList:
                if i.startswith('total') and i.endswith(objName.split(':')[1]):
                    return objList.index(i)
        return -1

    def reload(self):
        tree = self.fileEditor.get_current_child()
        if tree:
            fileName = tree.objectName().split(':')[-1]
            tmp = tree.objectName()
            if tmp.startswith(':'):
                tmp = tmp[1:]
            filePath = os.path.join(self.db.Path['project'], tmp.replace(':', os.sep))
            if fileName.endswith('xml'):
                self.db.load_file(filePath, tree)
                self.fileEditor.setTabText(self.fileEditor.currentIndex(), tree.objectName())
            elif fileName.endswith('php'):
                print(filePath)
                self.db.load_php(filePath, tree)
                self.fileEditor.setTabText(self.fileEditor.currentIndex(), tree.objectName())
        table = self.elemEditor.get_current_child()
        if table:
            modInfo, typ = table.objectName().split(':')
            table.setup(table.data, modInfo, typ, self.proxy.setup_data)
            self.elemEditor.setTabText(self.elemEditor.currentIndex(), table.objectName())

    def save_project(self):
        print('save project')
        for i in range(self.fileEditor.count()):
            if self.fileEditor.tabText(i).endswith('*'):
                self.save_file_tab(i)
        for i in range(self.elemEditor.count()):
            if self.elemEditor.tabText(i).endswith('*'):
                self.save_data_tab(i)

    def save_file(self):
        print('save file')
        if self.treeWidget_data.isEnabled():
            objName = self.focusWidget().objectName()
            objListFile = [self.fileEditor.widget(i).objectName() for i in range(self.fileEditor.count())]
            objListData = [self.elemEditor.widget(i).objectName() for i in range(self.elemEditor.count())]
            if objName in objListFile:
                self.save_file_tab()
            elif objName in objListData:
                self.save_data_tab()

    def save_file_tab(self, idx=None):
        if idx is not None:
            print('idx is not None')
            currentTab = self.fileEditor.widget(idx)
        else:
            print('idx is None')
            currentTab = self.fileEditor.currentWidget()
        print('save file tab')
        if currentTab:
            objName = currentTab.objectName()
            fileName = objName.split(':')[-1]
            if fileName.endswith('.xml'):
                print('save xml')
                tree = currentTab.findChild(dataTree)
                mods = dict(self.db.getMods)
                modsKey = [f'{k}_{i}' for k, i in enumerate(mods.keys())]
                modsKey = ['-_0', *modsKey]
                modsValue = list(mods.values())
                modsValue = ['data', *modsValue]
                modInfo = modsKey[modsValue.index(objName.split(':')[0])]
                self.db.write_file_from_tree(tree, self.db.gameData[modInfo], modInfo)
                self.fileEditor.setTabText(self.fileEditor.currentIndex(), tree.objectName())
            elif fileName.endswith('.php'):
                print('save php')
                table = currentTab.findChild(dataTable)
                self.db.write_php_from_data(table)
                self.fileEditor.setTabText(self.fileEditor.currentIndex(), table.objectName())

    def save_data_tab(self, idx=None):
        if idx:
            currentTab = self.elemEditor.widget(idx)
        else:
            currentTab = self.elemEditor.currentWidget()
        if currentTab:
            table = currentTab.findChild(dataTable)
            table.sortByColumn(0, Qt.AscendingOrder)
            table.update_data(self.db.gameData)
            self.db.write_file_from_data(table.data, table.objectName().split(':')[1])
            self.elemEditor.setTabText(self.elemEditor.currentIndex(), table.objectName())

    def remove_file_tab(self, idx):
        if self.fileEditor.tabText(idx).find('*') != -1:
            reply = QMessageBox.question(self, '数据未保存', '你想保存数据吗',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.save_file_tab(idx)
            elif reply == QMessageBox.Cancel:
                return
        self.fileEditor.removeTab(idx)

    def remove_data_tab(self, idx):
        if self.elemEditor.tabText(idx).find('*') != -1:
            reply = QMessageBox.question(self, '数据未保存', '你想保存数据吗',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.save_data_tab(idx)
            elif reply == QMessageBox.Cancel:
                return
        self.elemEditor.removeTab(idx)


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(BASE_DIR, 'client'))
    app = QApplication(sys.argv)
    Form = mainUI()
    Form.show()
    logInit(os.getcwd())
    sys.exit(app.exec_())
