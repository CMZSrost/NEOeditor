import os
from time import time

import lxml.etree as etree
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTableWidget, QTableWidgetItem, QTreeWidgetItem, QTreeWidgetItemIterator

from recipeDialog import recipeDialog
from xmlIter import fast_iter, get_column, gen_xml_table


class EditorDB:
    Path, getMods, gameData = {}, {}, {}

    def __init__(self, **kwargs):
        self.MainWindow = kwargs["MainWindow"]
        self.proxy = kwargs["proxy"]
        self.config = kwargs["config"]
        self.Path['project'] = self.config["projectPath"]
        self.recipes = None

    def clear(self):
        self.MainWindow.treeWidget_file.clear()
        self.MainWindow.treeWidget_data.clear()
        self.gameData.clear()
        self.recipes = None
        self.MainWindow.recipesAnalysisAction.setEnabled(False)
        self.MainWindow.showRecipesAction.setEnabled(False)

    def load_path(self, path: str):
        self.Path['project'] = path
        paths = ['data', 'Mods', 'img']
        for i in paths:
            self.Path[i] = os.path.join(path, i)
        self.Path['getMods'] = os.path.join(path, 'getmods.php')
        self.Path['getimages'] = os.path.join(path, 'getimages.php')

    def load_project(self, path):
        start = time()
        self.clear()
        self.load_path(path)
        print(self.Path)
        modsList: list[str] = self.load_php(self.Path['getMods'])
        if modsList:
            self.getMods = list(zip(modsList[::2], modsList[1::2]))

            for i in list(self.Path.values())[1:]:
                print(f'loading {i}')
                self.MainWindow.treeWidget_file.load_folder(i)
            self.MainWindow.treeWidget_data.load_data('total',
                                                      [os.path.splitext(i)[-2] for i in os.listdir(self.Path['data'])])

            print(f'Initial in {np.round(time() - start, 3)} seconds')
            self.load_mods()
            self.MainWindow.statusbar.showMessage(f'Project loaded in {np.round(time() - start, 3)} seconds')

    def recipes_analysis(self):
        self.recipes = recipeDialog(self.MainWindow)
        self.recipes.setup(self.gameData)
        self.MainWindow.showRecipesAction.setEnabled(True)

    def load_mods(self):
        kwargs = {'gameData': self.gameData,
                  'dataTree': self.MainWindow.treeWidget_data,
                  'projectPath': self.Path['project'],
                  'dirPath': self.Path['data'],
                  'modInfo': ['-', '0']}
        self.gameData['-_0'] = {}
        self.MainWindow.treeWidget_data.add_node('-_0')
        self.proxy.load_data(**kwargs)
        for modID, modStr in enumerate(self.getMods):
            self.gameData[f'{modID}_{modStr[0]}'] = {}
            kwargs['dirPath'] = os.path.join(self.Path['project'], modStr[1])
            kwargs['modInfo'] = [modID, modStr[0]]
            self.MainWindow.treeWidget_data.add_node(f'{modID}_{modStr[0]}')
            self.proxy.load_data(**kwargs)

    @staticmethod
    def setchildtext(node: etree.Element, parent: QTreeWidgetItem):
        for elem in node.xpath('./*'):
            item = EditorDB.setNode(elem)
            parent.addChild(item)
            EditorDB.setchildtext(elem, item)

    @staticmethod
    def setNode(elem):
        item = QTreeWidgetItem()
        item.setText(0, elem.tag)
        item.setData(3, 0, elem.sourceline)
        if elem.text is not None:
            item.setFlags(Qt.ItemFlag(63))
            item.setText(1, elem.text)
        if elem.attrib is not None:
            item.setText(2, '\n'.join(f'{k}="{v}"' for k, v in elem.attrib.items()))
        return item

    def load_file(self, filepath, treeView: QTreeWidget):
        treeView.clear()
        treeView.sortByColumn(3, Qt.AscendingOrder)
        if os.path.isfile(filepath) and filepath.endswith(".xml"):
            xmlIter = etree.iterparse(filepath, events=('start', 'end'), encoding='UTF-8', )
            treeView.addTopLevelItem(fast_iter(xmlIter))

    def clear_database(self, path, typ=None):
        parser = etree.XMLParser(remove_blank_text=True)
        xml_root = etree.parse(path, parser).getroot()
        database = xml_root.xpath('//database')[0]
        xtext = './table' if typ is None else f'./table[@name="{typ}"]'
        for child in database.xpath(xtext):
            database.remove(child)
        return xml_root, database

    def write_file_from_data(self, data, typ):
        filePathSet = set(data[:, -1])
        datas = [data[data[:, -1] == i, 1:-1] for i in filePathSet]
        column = get_column(typ)[1:-1]
        for filePath, dataPiece in zip(filePathSet, datas):
            Path = self.Path['project'] + filePath
            xml_root, database = self.clear_database(Path, typ)

            tables = [gen_xml_table(typ, column, i) for i in dataPiece]
            database.extend(tables)
            tree = etree.ElementTree(xml_root)

            saveFile = self.Path['project'] + filePath
            savePath = os.path.dirname(saveFile)
            fileName = os.path.basename(filePath)
            os.makedirs(savePath, exist_ok=True)
            tree.write(os.path.join(savePath, fileName), pretty_print=True, xml_declaration=True,
                       encoding='utf-8')

    def write_file_from_tree(self, tree: QTreeWidget, gameData, modInfo):
        dirName, fileName = tree.objectName().split(':')
        filePath = '/' + os.path.join(dirName, fileName).replace('\\', '/')
        print(filePath)
        Path = os.path.join(self.Path['project'], dirName, fileName)
        xml_root, database = self.clear_database(Path)

        iter = QTreeWidgetItemIterator(tree)
        while iter.value().text(0) != 'database':
            iter += 1
        treeDB = iter.value()
        tables = []
        shapes = {i: j.shape[0] for i, j in gameData.items()}
        for i in range(treeDB.childCount()):
            treeTable = treeDB.child(i)
            if treeTable.text(0) == '<!---->':
                tables.append(etree.Comment(treeTable.text(1)))
            else:
                typ = treeTable.text(2)
                column = {treeTable.child(j).text(2): treeTable.child(j).text(1) for j in range(treeTable.childCount())
                          if treeTable.child(j).text(0) != '<!---->'}
                gameData[typ] = np.vstack([gameData[typ], [modInfo, *list(column.values()), filePath]])
                table = gen_xml_table(typ, list(column.keys()), list(column.values()))
                tables.append(table)
        for i in shapes.keys():
            ind = np.where(gameData[i][:, -1] != filePath)[0]
            gameData[i] = np.vstack([gameData[i][ind], gameData[i][shapes[i]:]])
        database.extend(tables)

        tree = etree.ElementTree(xml_root)

        savePath = os.path.join(self.Path['project'], dirName)
        saveFile = os.path.join(savePath, fileName)
        os.makedirs(savePath, exist_ok=True)
        tree.write(saveFile, pretty_print=True, xml_declaration=True,
                   encoding='utf-8')

    def write_php_from_data(self, table: QTableWidget):
        dirName, fileName = table.objectName().split(':')
        Path = os.path.join(self.Path['project'], dirName, fileName).replace('\\', '/')
        print(Path)
        print(fileName)
        with open(Path, 'w', encoding='utf-8') as f:
            table.sortByColumn(0, Qt.AscendingOrder)
            if fileName == 'getmods.php':
                f.write(f'nRows={table.rowCount()}')
                for i in range(table.rowCount()):
                    f.write(
                        f'&strModName{table.item(i, 0).text()}={table.item(i, 1).text()}&strModURL{table.item(i, 0).text()}={table.item(i, 2).text()}\n')
            elif fileName == 'getimages.php':
                f.write(f'nRows={table.rowCount()}&nCols=2')
                for i in range(table.rowCount()):
                    f.write(f'&strImageURL{table.item(i, 0).text()}={table.item(i, 1).text()}')

    @staticmethod
    def load_php(filepath, tableView: QTableWidget = None):
        if os.path.isfile(filepath):
            print(os.path.basename(filepath))
            print(filepath)
            offsetMap = {'getmods.php': (1, ['modId', 'strModName', 'strModURL']),
                         'getimages.php': (2, ['imageId', 'strImageURL'])}
            (offset, column) = offsetMap[os.path.basename(filepath)]

            with open(filepath, 'r', encoding='utf-8') as f:
                text = ''.join(f.readlines()).replace('\n', '').split("&")[offset:]
                item = [i.split('=')[1] for i in text]
            if tableView:
                tableView.setColumnCount(len(column))
                tableView.setHorizontalHeaderLabels(column)
                tableView.column = column
                if tableView.columnCount() == 3:
                    item = list(zip(item[::2], item[1::2]))
                tableView.setRowCount(len(item))
                for cnt, value in enumerate(item):
                    tableView.setItem(cnt, 0, QTableWidgetItem(str(cnt)))
                    if tableView.columnCount() == 3:
                        tableView.setItem(cnt, 1, QTableWidgetItem(value[0]))
                        tableView.setItem(cnt, 2, QTableWidgetItem(value[1]))
                    else:
                        tableView.setItem(cnt, 1, QTableWidgetItem(value))
            return item
