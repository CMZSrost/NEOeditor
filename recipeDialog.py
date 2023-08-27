import numpy as np
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from Editor_UI import UI_recipesAnalysis
from xmlIter import get_column


class recipeDialog(QDialog, UI_recipesAnalysis.Ui_recipes):
    def __init__(self, parent=None):
        super(recipeDialog, self).__init__(parent)
        self.setupUi(self)
        self.recipesLabel = ['modinfo', 'nID', 'strName']
        self.toolLabel = ['type', 'modinfo', 'nID', 'strPropertyName', 'num']
        self.itemLabel = ['modinfo', 'id', 'nGroupID', 'nSubGroupID', 'strName']
        self.gameData = None
        self.recipes = None
        self.itempropsName = {}
        self.itemprops = {}
        self.modinfoMap = {}
        self.setWindowFlags(Qt.Window)
        # self.item

    def setup(self, gameData):
        Data = {}
        keys = gameData[list(gameData.keys())[0]].keys()
        for typ in keys:
            Data[typ] = np.vstack([gameData[i][typ] for i in gameData.keys() if
                                   typ in gameData[i].keys()])
        self.gameData = Data
        self.load_recipes()
        self.analysis()

    def load_recipes(self):
        self.tableWidget_recipes.clear()
        self.recipes = self.gameData['recipes']
        self.tableWidget_recipes.load_data(self.recipes[:, :3], self.recipesLabel)

    def analysis(self):
        column = get_column('itemprops')
        ptr = column.index('nID')
        namePtr = column.index('strPropertyName')
        self.itempropsName = {}
        self.itemprops = {}
        for j in self.gameData['itemprops']:
            self.modinfoMap[j[0].split("_")[-1]] = j[0]
            self.itempropsName[f'{j[0].split("_")[-1]}:{j[ptr]}'] = j[namePtr]
            self.itemprops[f'{j[0].split("_")[-1]}:{j[ptr]}'] = []
        column = get_column('itemtypes')
        ptr = column.index('vProperties')
        for i, j in enumerate(self.gameData['itemtypes']):
            vProperty = j[ptr].split(',')
            for k in vProperty:
                if k.find(':') == -1:
                    k = f'{j[0].split("_")[-1]}:{k}'
                if k in self.itemprops.keys():
                    self.itemprops[k].append(i)

    def show_recipe(self, i, j):
        print(i, j)
        toolPtr = get_column('recipes').index('strTools')
        consumedPtr = get_column('recipes').index('strConsumed')
        if self.recipes[i][toolPtr] != '':
            tools = self.recipes[i][toolPtr].split('+')
        else:
            tools = []
        if self.recipes[i][consumedPtr] != '':
            consumed = self.recipes[i][consumedPtr].split('+')
        else:
            consumed = []

        ary = np.full((len(tools) + len(consumed), 5), '', dtype=object)
        for k, v in enumerate([*tools, *consumed]):
            try:
                num, nID = v.split('x')
            except ValueError:
                print(f'ValueError:{v}')
                num, nID = 1, v
            if nID.find(':') == -1:
                nID = f'{self.recipes[i][0].split("_")[-1]}:{nID}'
            modinfo, nID = nID.split(':')
            ary[k, :] = ['', self.modinfoMap[modinfo], nID, self.itempropsName.get(f'{modinfo}:{nID}', 'None'), num]
        ary[:len(tools), 0] = ['tool' for _ in range(len(tools))]
        ary[len(tools):, 0] = ['consumed' for _ in range(len(consumed))]
        self.tableWidget_tools.load_data(ary, self.toolLabel)
        self.clear(self.tableWidget_items)
        self.label_modinfo.setText(self.recipes[i][0])
        self.label_nID.setText(self.recipes[i][1])
        self.label_strName.setText(self.recipes[i][2])
        self.label_strSecretName.setText(self.recipes[i][3])

    def clear(self, tableWidget):
        tableWidget.clear()
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(0)

    def show_item(self, i, j):
        print(i, j)
        modName = self.tableWidget_tools.item(i, 1).text().split('_')[-1]
        nID = self.tableWidget_tools.item(i, 2).text()
        Property = f'{modName}:{nID}'
        ptr = len(self.itemLabel)

        item = self.gameData['itemtypes'][self.itemprops[Property], :ptr]
        self.tableWidget_items.load_data(item, self.itemLabel)
