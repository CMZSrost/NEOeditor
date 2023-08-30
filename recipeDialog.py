import os

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
        self.toolLabel = ['type', 'modinfo', 'nID', 'strName', 'num']
        self.itemLabel = ['modinfo', 'id', 'nGroupID', 'nSubGroupID', 'strName']
        self.gameData = None
        self.recipes = None
        self.path = None
        self.modsList = None
        self.ingredientsName = {}
        self.ingredients = {}
        # self.modinfoMap = {}
        self.setWindowFlags(Qt.Window)
        # self.item

    def setup(self, gameData, path, modsList):
        self.path = path
        self.modsList = modsList
        print(modsList)
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

    def find_recipe(self, modinfo, nID):
        print(modinfo, nID)
        idx = np.where((self.recipes[:, 0] == modinfo) & (self.recipes[:, 1] == nID))[0]
        if len(idx) == 0:
            return
        self.show_recipe(idx[0],idx[0])



    def analysis(self):
        def get_ingredients(List):
            tmp = []
            for j in List:
                if j.find(':') == -1:
                    j = f'{i[0]}:{j}'
                modInfo, nID = j.split(':')
                modInfo = self.get_mod_info(modInfo)
                j = f'{modInfo}:{nID}'
                tmp.append(j)
            return tmp

        column = get_column('ingredients')
        ptr = column.index('nID')
        namePtr = column.index('strName')
        requiredPtr = column.index('strRequiredProps')
        forbidPtr = column.index('strForbidProps')
        self.ingredientsName = {}
        self.ingredients = {}
        for i in self.gameData['ingredients']:
            # self.modinfoMap[i[0].split("_")[-1]] = i[0]
            self.ingredientsName[f'{i[0]}:{i[ptr]}'] = i[namePtr]
            required = get_ingredients(i[requiredPtr].split('&') if i[requiredPtr] != '' else [])
            forbid = get_ingredients(i[forbidPtr].split('&') if i[forbidPtr] != '' else [])
            self.ingredients[f'{i[0]}:{i[ptr]}'] = (required, forbid)

    def get_mod_info(self, modInfo):
        if modInfo == '0':
            modInfo = '-_0'
        elif modInfo.find('_') == -1:
            modInfo = f'{self.modsList.index(modInfo)}_{modInfo}'
        return modInfo

    def show_recipe(self, i, j):
        print(i, j)
        recipe = self.recipes[i]
        toolPtr = get_column('recipes').index('strTools')
        consumedPtr = get_column('recipes').index('strConsumed')
        tools = recipe[toolPtr].split('+') if recipe[toolPtr] != '' else []
        consumed = recipe[consumedPtr].split('+') if recipe[consumedPtr] != '' else []

        ary = np.full((len(tools) + len(consumed), 5), '', dtype=object)
        for k, v in enumerate([*tools, *consumed]):
            try:
                num, nID = v.split('x')
            except ValueError:
                print(f'ValueError:{v}')
                num, nID = 1, v
            if nID.find(':') == -1:
                nID = f'{self.recipes[i][0]}:{nID}'
            modinfo, nID = nID.split(':')
            modinfo = self.get_mod_info(modinfo)
            ingredientName = self.ingredientsName.get(f'{modinfo}:{nID}', '')
            if ingredientName == '' and modinfo != '-_0':
                modinfo = '-_0'
                ingredientName = self.ingredientsName.get(f'{modinfo}:{nID}', '')
            ary[k, :] = ['', modinfo, nID, ingredientName, num]
        ary[:len(tools), 0] = ['tool' for _ in range(len(tools))]
        ary[len(tools):, 0] = ['consumed' for _ in range(len(consumed))]

        self.tableWidget_tools.load_data(ary, self.toolLabel)
        self.clear(self.tableWidget_items)
        self.label_modinfo.setText(self.recipes[i][0])
        self.label_nID.setText(self.recipes[i][1])
        self.label_strName.setText(self.recipes[i][2])
        self.label_strSecretName.setText(self.recipes[i][3])

    def load_tools(self, i, toolID, tool):
        for j in toolID:
            try:
                num, nID = j.split('x')
            except ValueError:
                print(f'ValueError:{j}')
                num, nID = 1, j
            if nID.find(':') == -1:
                nID = f'{i[0]}:{nID}'
            modinfo, nID = nID.split(':')
            modinfo = self.get_mod_info(modinfo)
            tool.append(f"{self.ingredientsName.get(f'{modinfo}:{nID}')} x {num}")

    def export_recipes(self):
        filePath = os.path.join(self.path, 'recipes.txt')
        strNamePtr = get_column('recipes').index('strName')
        toolPtr = get_column('recipes').index('strTools')
        consumedPtr = get_column('recipes').index('strConsumed')
        print(filePath)
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(f'all recipes:\n\n')
            for i in self.recipes:
                recipeStr = f"{i[strNamePtr]}:"
                toolID = i[toolPtr].split('+') if i[toolPtr] != '' else []
                consumedID = i[consumedPtr].split('+') if i[consumedPtr] != '' else []
                tool, consumed = [], []
                self.load_tools(i, toolID, tool)
                self.load_tools(i, consumedID, consumed)
                recipeStr += '\ntool:\t' + ',  '.join(tool)
                recipeStr += '\nconsumed:\t' + ',  '.join(consumed)
                f.write(recipeStr + '\n\n')

    @staticmethod
    def clear(tableWidget):
        tableWidget.clear()
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(0)

    def clear_text(self):
        self.label_modinfo = ''
        self.label_nID = ''
        self.label_strName = ''
        self.label_strSecretName = ''

    def show_item(self,i, j):
        print(i, j)
        modinfo = self.tableWidget_tools.item(i, 1).text()
        nID = self.tableWidget_tools.item(i, 2).text()
        self.show_cell_item(modinfo, nID)

    def show_cell_item(self, modinfo, nID):
        ingredientName = f'{modinfo}:{nID}'
        required, forbid = self.ingredients.get(ingredientName, ([], []))
        requiredSet, forbidSet = set(required), set(forbid)

        itemtypesColumn = get_column('itemtypes')
        namePtr = itemtypesColumn.index('strName')
        ptr = itemtypesColumn.index('vProperties')

        ary = np.array([])

        for i, j in enumerate(self.gameData['itemtypes']):
            vProperty = j[ptr].split(',')
            props = set()
            for k in vProperty:
                if k.find(':') == -1:
                    k = f'{j[0]}:{k}'
                kmodinfo, knID = k.split(':')
                kmodinfo = self.get_mod_info(kmodinfo)
                k = f'{kmodinfo}:{knID}'
                props.add(k)
            if requiredSet.issubset(props) and not forbidSet.intersection(props):
                ary = np.vstack((ary, j[:namePtr+1])) if ary.size else j[:namePtr+1]

        self.tableWidget_items.load_data(ary.reshape((-1,namePtr+1)), self.itemLabel)
