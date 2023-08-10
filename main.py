import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from Editor_UI import UI_main, UI_fileTab
from EditorDB import EditorDB
from dataTableUI import NewTable


class mainUI(QMainWindow, UI_main.Ui_main):
    def __init__(self):
        super(mainUI, self).__init__()
        self.setupUi(self)
        self.db = EditorDB(fileTreeWidget=self.treeWidget_file, dataTreeWidget=self.treeWidget_data,
                           statusBar=self.statusbar)
        self.AllTemplateTab = QTabWidget()
        self.templateTab = UI_fileTab.Ui_templateTab()

    def loadProject(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", self.db.projectPath)
        if os.path.isdir(path):
            self.db.loadProject(path)

    def doubleClick(self, idx):
        if self.sender() == self.treeWidget_file:
            path = os.path.join(self.db.projectPath, self.db.fileTree.getFilePath(idx))
            if os.path.isfile(path):
                fileName = os.path.basename(path)
                if fileName.endswith('xml'):
                    tab = self.tabFactory(fileName, self.fileEditor, 'filetab')
                    if tab:
                        tree = tab.findChild(QTreeWidget, 'treeWidget')
                        tree.sortByColumn(3, Qt.AscendingOrder)
                        self.db.loadFile(path, tree)
                elif fileName.endswith('php'):
                    tab = self.tabFactory(fileName, self.fileEditor, 'datatab')
                    if tab:
                        self.db.loadPhp(path, tab.findChild(QTableWidget, 'tableWidget'))
            elif os.path.isdir(path):
                self.treeWidget_file.setExpanded(idx, not self.treeWidget_file.isExpanded(idx))
        elif self.sender() == self.treeWidget_data:
            if len(os.path.split(self.db.dataTree.getFilePath(idx))) == 1:
                self.treeWidget_data.setExpanded(idx, not self.treeWidget_data.isExpanded(idx))
                return
            datapath = os.path.split(self.db.dataTree.getFilePath(idx))
            if datapath[0] == '':
                self.treeWidget_data.setExpanded(idx, not self.treeWidget_data.isExpanded(idx))
                return
            else:
                tab = self.tabFactory('_'.join(datapath), self.elemEditor, 'datatab')
                if tab:
                    table = tab.findChild(NewTable, 'tableWidget')
                    table.setup(self.db.gameDB[datapath[1]], datapath[0])
                    table.cellChanged['int', 'int'].connect(self.elemEditor.itemChange)
                    self.elemEditor.setCurrentIndex(self.elemEditor.count() - 1)
                    self.elemEditor.tabText(self.elemEditor.count() - 1).replace('*', '')

    def tabFactory(self, tabName, tabParent: QTabWidget, type):
        self.AllTemplateTab.clear()
        tablist = [tabParent.tabText(i) for i in range(tabParent.count())]
        if tabName in tablist:
            tabParent.setCurrentIndex(tablist.index(tabName))
            return
        self.templateTab.setupUi(self.AllTemplateTab)
        pos = self.AllTemplateTab.findChild(QWidget, type)
        pos.setObjectName(tabParent.objectName() + '_' + tabName)
        tabParent.addTab(pos, tabName)
        return pos

    def filterFile(self, name):
        if self.sender() == self.lineEdit_file:
            self.db.fileTree.filterFile(name)
        elif self.sender() == self.lineEdit_data:
            self.db.dataTree.filterFile(name)

    def removeFileTab(self, idx):
        self.fileEditor.removeTab(idx)

    def removeDataTab(self, idx):
        if self.elemEditor.tabText(idx).find('*') != -1:
            print(idx)
        self.elemEditor.removeTab(idx)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Form = mainUI()
    Form.show()
    exit(app.exec_())
