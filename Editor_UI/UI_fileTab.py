# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Pytrain\NEOeditor\Editor_UI\fileTab.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_templateTab(object):
    def setupUi(self, templateTab):
        templateTab.setObjectName("templateTab")
        templateTab.resize(941, 662)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(templateTab.sizePolicy().hasHeightForWidth())
        templateTab.setSizePolicy(sizePolicy)
        templateTab.setTabsClosable(True)
        templateTab.setMovable(True)
        self.filetab = QtWidgets.QWidget()
        self.filetab.setObjectName("filetab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.filetab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.filetab)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.treeWidget = QtWidgets.QTreeWidget(self.filetab)
        self.treeWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.treeWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.treeWidget.setTabKeyNavigation(True)
        self.treeWidget.setDragEnabled(False)
        self.treeWidget.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.treeWidget.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.treeWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.treeWidget.setTextElideMode(QtCore.Qt.ElideLeft)
        self.treeWidget.setAutoExpandDelay(0)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setAllColumnsShowFocus(True)
        self.treeWidget.setExpandsOnDoubleClick(False)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setHighlightSections(False)
        self.verticalLayout.addWidget(self.treeWidget)
        templateTab.addTab(self.filetab, "")
        self.datatab = QtWidgets.QWidget()
        self.datatab.setObjectName("datatab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.datatab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.datatab)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.tableWidget = NewTable(self.datatab)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.tableWidget.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.tableWidget)
        templateTab.addTab(self.datatab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_4.addWidget(self.graphicsView)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableWidget_2.setDragEnabled(False)
        self.tableWidget_2.setDragDropOverwriteMode(False)
        self.tableWidget_2.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.tableWidget_2.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.tableWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_2.setWordWrap(False)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        self.tableWidget_2.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.tableWidget_2)
        templateTab.addTab(self.tab, "")

        self.retranslateUi(templateTab)
        templateTab.setCurrentIndex(1)
        self.tableWidget.cellClicked['int','int'].connect(self.tableWidget.showinfo) # type: ignore
        self.lineEdit.textChanged['QString'].connect(self.tableWidget.findText) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(templateTab)

    def retranslateUi(self, templateTab):
        _translate = QtCore.QCoreApplication.translate
        templateTab.setWindowTitle(_translate("templateTab", "TabWidget"))
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.headerItem().setText(0, _translate("templateTab", "属性"))
        self.treeWidget.headerItem().setText(1, _translate("templateTab", "值"))
        self.treeWidget.headerItem().setText(2, _translate("templateTab", "属性注释"))
        templateTab.setTabText(templateTab.indexOf(self.filetab), _translate("templateTab", "文件"))
        self.tableWidget.setSortingEnabled(True)
        templateTab.setTabText(templateTab.indexOf(self.datatab), _translate("templateTab", "数据"))
        self.label.setText(_translate("templateTab", "modName:"))
        self.label_4.setText(_translate("templateTab", "TextLabel"))
        self.label_2.setText(_translate("templateTab", "modID:"))
        self.label_5.setText(_translate("templateTab", "TextLabel"))
        self.label_3.setText(_translate("templateTab", "str:"))
        self.label_6.setText(_translate("templateTab", "TextLabel"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("templateTab", "属性"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("templateTab", "值"))
        templateTab.setTabText(templateTab.indexOf(self.tab), _translate("templateTab", "详情"))
from dataTableUI import NewTable
