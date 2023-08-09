import json
import os

import numpy as np
from PyQt5.QtWidgets import QTreeWidget, QTableWidget, QTableWidgetItem

from sourceTree import sourceTree
from gameDB import gameDB
import lxml.etree as etree
from xmlIter import fast_iter, get_info, data_iter, getColumn


class EditorDB:
    def __init__(self, **kwargs):
        with open("config.json", 'r') as f:
            config = json.load(f)
            self.language = config["language"]
            self.projectPath = config["projectPath"]
        self.fileTree = sourceTree(kwargs["fileTreeWidget"])
        self.dataTree = sourceTree(kwargs["dataTreeWidget"])
        self.gameDB = {}

    def loadPath(self, path: str):
        self.projectPath: str = path
        self.getModsPath = path + "/getmods.php"
        self.getimagesPath = path + "/getimages.php"
        self.dataPath = path + "/data"
        self.imgPath = path + "/img"
        self.modsPath = path + "/Mods"

    def loadProject(self, path):
        self.loadPath(path)
        self.gameData = dict()
        modslist: list[str] = self.loadPhp(self.getModsPath)
        self.getMods = list(zip(modslist[::2], modslist[1::2]))
        if self.fileTree.treeWidget.topLevelItemCount() > 0:
            self.fileTree.treeWidget.clear()
        if self.dataTree.treeWidget.topLevelItemCount() > 0:
            self.dataTree.treeWidget.clear()
        for i in [self.dataPath, self.imgPath, self.modsPath, self.getModsPath, self.getimagesPath]:
            self.fileTree.loadFolder(i)
        typelist = [os.path.splitext(i)[-2] for i in os.listdir(self.dataPath)]
        self.dataTree.loadData('total', typelist)
        self.loadData(self.dataPath, ['-', 'game', ''])
        self.loadMods()
        for i in self.gameData.keys():
            self.gameDB[i] = gameDB(i, getColumn(i), self.gameData[i])

    def loadMods(self):
        for modid, modstr in enumerate(self.getMods):
            self.loadData(os.path.join(self.projectPath, modstr[1]), [modid, modstr[0], ''])

    def loadData(self, dirpath, modinfo):
        DBdict = {}
        if os.path.isdir(dirpath):
            for root, dirs, files in os.walk(dirpath):
                for file in files:
                    if os.path.basename(file).endswith('.xml'):
                        xmliter = etree.iterparse(os.path.join(root, file), events=('start', 'end'), encoding='UTF-8')
                        modinfo[2] = (os.path.join(root, file).replace(self.projectPath,'').replace('\\','/'))
                        tempDB = data_iter(xmliter, modinfo)
                        for i in tempDB.keys():
                            if i in DBdict.keys():
                                DBdict[i] = np.vstack((DBdict[i], tempDB[i]))
                            else:
                                DBdict[i] = np.array(tempDB[i], dtype=str)
        self.dataTree.loadData(f'{modinfo[0]}_{modinfo[1]}', list(DBdict.keys()))
        for i in DBdict.keys():
            if i in self.gameData.keys():
                self.gameData[i] = np.vstack((self.gameData[i], DBdict[i]))
            else:
                self.gameData[i] = np.array(DBdict[i], dtype=str)

    def loadFile(self, filepath, treeView: QTreeWidget):
        if os.path.isfile(filepath):
            if filepath.endswith(".xml"):
                xmliter = etree.iterparse(filepath, events=('start', 'end'), encoding='UTF-8')
                treeView.addTopLevelItem(fast_iter(xmliter))
            if filepath.endswith(".xml") and os.path.split(filepath)[0].endswith('data'):
                xmliter = etree.iterparse(filepath, events=('start', 'end'), encoding='UTF-8')
                treeView.addTopLevelItem(get_info(xmliter))

    def loadPhp(self, filepath, tableView: QTableWidget = None):
        if os.path.isfile(filepath):
            offset = 0
            column = []
            if os.path.basename(filepath) == 'getmods.php':
                column = ['modId', 'strModName', 'strModURL']
                offset = 1
            elif os.path.basename(filepath) == 'getimages.php':
                column = ['imageId', 'strImageURL']
                offset = 2
            if tableView is not None:
                tableView.setColumnCount(len(column))
                tableView.setHorizontalHeaderLabels(column)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = ''.join(f.readlines()).replace('\n', '').split("&")[offset:]
                item = [i.split('=')[1] for i in text]
                if tableView is not None:
                    if tableView.columnCount() == 3:
                        item = list(zip(item[::2], item[1::2]))
                    tableView.setRowCount(len(item))
                    for cnt, value in enumerate(item):
                        print(cnt, value)
                        tableView.setItem(cnt, 0, QTableWidgetItem(str(cnt)))
                        if tableView.columnCount() == 3:
                            tableView.setItem(cnt, 1, QTableWidgetItem(value[0]))
                            tableView.setItem(cnt, 2, QTableWidgetItem(value[1]))
                        else:
                            tableView.setItem(cnt, 1, QTableWidgetItem(value))
            return item
