from PyQt5.QtWidgets import QTabWidget

from Editor_UI import UI_fileTab


class templateTab(QTabWidget, UI_fileTab.Ui_templateTab):
    def __init__(self, parent=None):
        super(templateTab, self).__init__(parent)

