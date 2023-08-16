from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabWidget, QTableWidget
from Editor_UI import UI_fileTab
from dataTable import dataTable
from dataTree import dataTree


class templateTab(QTabWidget, UI_fileTab.Ui_templateTab):
    def __init__(self, parent=None):
        super(templateTab, self).__init__(parent)

