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
        self.gameData = None
        self.recipes = None
        self.modinfoMap = {}
        # self.item

    def setup(self, gameData):
        self.gameData = gameData
        self.load_recipes()
        self.analysis()

    def load_recipes(self):
        self.tableWidget_recipes.clear()
        recipes = np.array([])
        for i in self.gameData:
            if 'recipes' in self.gameData[i]:
                recipes = np.vstack((recipes, self.gameData[i]['recipes'])) if recipes.size else self.gameData[i][
                    'recipes']
        self.recipes = recipes
        self.tableWidget_recipes.load_data(recipes[:, :3], self.recipesLabel)

    def analysis(self):
        column = get_column('itemprops')
        ptr = column.index('nID')
        namePtr = column.index('strPropertyName')
        self.itemprops = {}
        for i in self.gameData:
            if 'itemprops' in self.gameData[i]:
                for j in self.gameData[i]['itemprops']:
                    self.modinfoMap[j[0].split("_")[-1]] = j[0]
                    self.itemprops[f'{j[0].split("_")[-1]}:{j[ptr]}'] = j[namePtr]
        print(self.itemprops)
        print(self.modinfoMap)

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
                nID = f'0:{nID}'
            modinfo, nID = nID.split(':')
            ary[k, :] = ['', self.modinfoMap[modinfo], nID, self.itemprops.get(f'{modinfo}:{nID}', 'None'), num]
        ary[:len(tools), 0] = ['tool' for _ in range(len(tools))]
        ary[len(tools):, 0] = ['consumed' for _ in range(len(consumed))]
        self.tableWidget_tools.load_data(ary, self.toolLabel)
        self.label_modinfo.setText(self.recipes[i][0])
        self.label_nID.setText(self.recipes[i][1])
        self.label_strName.setText(self.recipes[i][2])
        self.label_strSecretName.setText(self.recipes[i][3])
