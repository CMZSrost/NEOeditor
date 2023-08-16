import json
import os
from time import time

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTableWidget, QTableWidgetItem, QStatusBar, QTreeWidgetItem, \
    QTreeWidgetItemIterator

import lxml.etree as etree

from sourceTree import sourceTree
from xmlIter import fast_iter, get_column,gen_xml_table


class EditorDB:
    def __init__(self, **kwargs):
        with open("config.json", 'r') as f:
            config = json.load(f)
            self.language = config["language"]
            self.projectPath = config["projectPath"]
        self.fileTree: sourceTree = kwargs["fileTreeWidget"]
        self.dataTree: sourceTree = kwargs["dataTreeWidget"]
        self.proxy = kwargs["proxy"]
        self.statusBar: QStatusBar = kwargs["statusBar"]
        self.statusBar.showMessage('waiting for project', 0)
        self.Path, self.getMods, self.gameData = {}, {}, {}

    def clear(self):
        self.fileTree.clear()
        self.dataTree.clear()
        self.gameData.clear()

    def load_path(self, path: str):
        self.Path['project'] = path
        self.Path['data'] = path + "/data"
        self.Path['mods'] = path + "/Mods"
        self.Path['img'] = path + "/img"
        self.Path['getMods'] = path + "/getmods.php"
        self.Path['getimages'] = path + "/getimages.php"

    def load_project(self, path):
        start = time()
        self.clear()
        self.load_path(path)
        modsList: list[str] = self.load_php(self.Path['getMods'])
        self.getMods = list(zip(modsList[::2], modsList[1::2]))

        for i in list(self.Path.values())[1:]:
            print(f'loading {i}')
            self.fileTree.load_folder(i)
        self.dataTree.load_data('total', [os.path.splitext(i)[-2] for i in os.listdir(self.Path['data'])])

        print(f'Initial in {np.round(time() - start, 3)} seconds')
        self.load_mods()
        self.statusBar.showMessage(f'Project loaded in {np.round(time() - start, 3)} seconds')

    def load_mods(self):
        kwargs = {'gameData': self.gameData,
                  'dataTree': self.dataTree,
                  'projectPath': self.Path['project'],
                  'dirPath': self.Path['data'],
                  'modInfo': ['-', 'data']}
        self.gameData['-_data'] = {}
        self.dataTree.add_node('-_data')
        self.proxy.load_data(**kwargs)
        for modID, modStr in enumerate(self.getMods):
            self.gameData[f'{modID}_{modStr[0]}'] = {}
            kwargs['dirPath'] = os.path.join(self.Path['project'], modStr[1])
            kwargs['modInfo'] = [modID, modStr[0]]
            self.dataTree.add_node(f'{modID}_{modStr[0]}')
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
            xmlIter = etree.iterparse(filepath, events=('start', 'end'), encoding='UTF-8',)
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

            saveFile = self.Path['project']+filePath
            savePath = os.path.dirname(saveFile)
            fileName = os.path.basename(filePath)
            os.makedirs(savePath, exist_ok=True)
            tree.write(os.path.join(savePath, fileName), pretty_print=True, xml_declaration=True,
                       encoding='utf-8')

    def write_file_from_tree(self, tree: QTreeWidget, gameData, modInfo):
        dirName, fileName = tree.objectName().split(':')
        filePath = '/'+os.path.join(dirName, fileName).replace('\\', '/')
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

    @staticmethod
    def load_php(filepath, tableView: QTableWidget = None):
        if os.path.isfile(filepath):
            offsetMap = {'getmods.php': (1, ['modId', 'strModName', 'strModURL']),
                         'getimages.php': (2, ['imageId', 'strImageURL'])}
            (offset, column) = offsetMap[os.path.basename(filepath)]

            with open(filepath, 'r', encoding='utf-8') as f:
                text = ''.join(f.readlines()).replace('\n', '').split("&")[offset:]
                item = [i.split('=')[1] for i in text]
            if tableView:
                tableView.setColumnCount(len(column))
                tableView.setHorizontalHeaderLabels(column)
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
