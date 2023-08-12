import json
import os
from time import time

import numpy as np
from PyQt5.QtWidgets import QTreeWidget, QTableWidget, QTableWidgetItem, QStatusBar

import lxml.etree as etree

from sourceTree import sourceTree
from xmlIter import fast_iter


class EditorDB:
    def __init__(self, **kwargs):
        with open("config.json", 'r') as f:
            config = json.load(f)
            self.language = config["language"]
            self.projectPath = config["projectPath"]
        self.fileTree:sourceTree = kwargs["fileTreeWidget"]
        self.dataTree:sourceTree = kwargs["dataTreeWidget"]
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
    def load_file(filepath, treeView: QTreeWidget):
        if os.path.isfile(filepath):
            if filepath.endswith(".xml"):
                xmlIter = etree.iterparse(filepath, events=('start', 'end'), encoding='UTF-8')
                treeView.addTopLevelItem(fast_iter(xmlIter))
            for i in [1, 2, 3]:
                treeView.resizeColumnToContents(i)

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
