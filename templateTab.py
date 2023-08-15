from PyQt5.QtWidgets import QTabWidget, QTableWidget
from Editor_UI import UI_fileTab
from dataTable import dataTable
from dataTree import dataTree


class templateTab(QTabWidget, UI_fileTab.Ui_templateTab):
    def __init__(self, parent=None):
        super(templateTab, self).__init__(parent)

    def setup(self, tempTab):
        self.setupUi(tempTab)
        for i in range(tempTab.count()):
            currentWidget = tempTab.widget(i)
            tree = currentWidget.findChild(dataTree)
            table = currentWidget.findChild(dataTable)
            if tree:
                print(tree.objectName())
                print(self.actionAddTable.objectName())
                tree.addActions([self.actionAddTable])
                self.actionAddTable.triggered.connect(tree.add_table)
            elif table:
                # table.addActions([self.actionDelTable])
                pass