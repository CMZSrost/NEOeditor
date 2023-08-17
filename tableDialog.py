from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QTableWidgetItem

from Editor_UI import UI_tableDialog
from xmlIter import get_column


class tableDialog(QDialog, UI_tableDialog.Ui_Dialog):
    def __init__(self, item, parent=None):
        super(tableDialog, self).__init__(parent)
        self.setupUi(self)
        self.item: QTreeWidgetItem = item
        self.update_table(self.comboBox_type.currentText())

    def set_init(self, item):
        typ = item.text(2)
        dataMap = {item.child(i).text(2): item.child(i).text(1) for i in range(item.childCount())}
        self.comboBox_type.setCurrentText(typ)
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.item(i, 1).setText(dataMap[self.tableWidget.item(i, 0).text()])

    def accept_table(self):
        sourceLine = self.item.child(self.item.childCount() - 1).data(3, 0) + 1
        table = QTreeWidgetItem()
        table.setText(0, 'table')
        table.setText(2, self.comboBox_type.currentText())
        table.setData(3, 0, sourceLine)
        children = []
        for i in range(self.tableWidget.rowCount()):
            sourceLine += 1
            child = QTreeWidgetItem()
            child.setText(0, 'column')
            child.setText(1, self.tableWidget.item(i, 1).text())
            child.setText(2, self.tableWidget.item(i, 0).text())
            child.setData(3, 0, sourceLine)
            child.setFlags(Qt.ItemFlag(63))
            children.append(child)
        table.addChildren(children)
        self.item.addChild(table)

    def update_table(self, typ):
        self.tableWidget.clearContents()
        typeList = get_column(typ)[1:-1]
        self.tableWidget.setRowCount(len(typeList))
        for i in range(len(typeList)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(typeList[i]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(''))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
