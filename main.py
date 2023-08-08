import sys
import os
from PyQt5.QtWidgets import *
from Editor_UI import UI_main, UI_fileTab
from EditorDB import EditorDB


class mainUI(QMainWindow, UI_main.Ui_main):
    def __init__(self):
        super(mainUI, self).__init__()
        self.setupUi(self)
        self.db = EditorDB(lang="Chinese", fileTreeWidget=self.treeWidget_file)
        self.AllTemplateTab = QTabWidget()
        self.templateTab = UI_fileTab.Ui_templateTab()

    def loadProject(self):
        #打开文件夹,默认为上次打开的文件夹，否则为当前文件夹
        if self.db.projectPath == "":
            self.db.projectPath = os.getcwd()
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", self.db.projectPath)
        if os.path.isdir(path):
            self.db.loadProject(path)

    def doubleClick(self, idx):
        if self.sender() == self.treeWidget_file:
            path = os.path.join(self.db.projectPath, self.db.fileTree.getFilePath(idx))
            if os.path.isfile(path):
                self.tabFactory(path,'file')
            elif os.path.isdir(path):
                self.treeWidget_file.setExpanded(idx, not self.treeWidget_file.isExpanded(idx))

    def tabFactory(self, path, type):
        if type == 'file':
            fileName, fileExtension = os.path.splitext(os.path.basename(path))
            pos = self.fileEditor.findChild(QWidget, fileName)
            if pos is not None:
                self.fileEditor.setCurrentWidget(pos)
                return
            self.templateTab.setupUi(self.AllTemplateTab)
            pos = self.AllTemplateTab.findChild(QWidget, 'filetab')
            self.fileEditor.addTab(pos, fileName)
            self.AllTemplateTab.clear()
            self.db.loadFile(path, pos.findChild(QTreeWidget, 'treeWidget'))


    def filterFile(self, name):
        if self.sender() == self.lineEdit_file:
            self.db.fileTree.filterFile(name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Form = mainUI()
    Form.show()
    exit(app.exec_())
