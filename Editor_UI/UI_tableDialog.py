# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Pytrain\NEOeditor\Editor_UI\tableDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(502, 518)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox_type = QtWidgets.QComboBox(Dialog)
        self.comboBox_type.setCurrentText("attackmodes")
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(0, "attackmodes")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(1, "barterhexes")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(2, "battlemoves")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(3, "camptypes")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(4, "chargeprofiles")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(5, "conditions")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(6, "containertypes")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(7, "creatures")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(8, "creaturesources")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(9, "datafiles")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(10, "dmcplaces")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(11, "encounters")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(12, "encountertriggers")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(13, "factions")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(14, "forbiddenhexes")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(15, "gamevars")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(16, "headlines")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(17, "ingredients")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(18, "itemprops")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(19, "itemtypes")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(20, "maps")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(21, "recipes")
        self.comboBox_type.addItem("")
        self.comboBox_type.setItemText(22, "treasuretable")
        self.verticalLayout.addWidget(self.comboBox_type)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.buttonBox_dialog = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox_dialog.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_dialog.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_dialog.setCenterButtons(True)
        self.buttonBox_dialog.setObjectName("buttonBox_dialog")
        self.verticalLayout.addWidget(self.buttonBox_dialog)

        self.retranslateUi(Dialog)
        self.buttonBox_dialog.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox_dialog.rejected.connect(Dialog.reject) # type: ignore
        self.comboBox_type.currentTextChanged['QString'].connect(Dialog.update_table) # type: ignore
        self.buttonBox_dialog.accepted.connect(Dialog.accept_table) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "add table"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "attrib"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "value"))
