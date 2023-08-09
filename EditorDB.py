import os
import re

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem

from sourceTree import sourceTree
import xml.etree.ElementTree as ET
import lxml.etree as etree
from xmlIter import fast_iter, get_info


class EditorDB:
    def __init__(self,lang="Chinese",**kwargs):
        self.language = lang
        self.projectPath = ""
        self.fileTree = sourceTree(kwargs["fileTreeWidget"])

    def loadPath(self, path):
        self.projectPath = path
        self.getModsPath = path + "/getmods.php"
        self.getimagesPath = path + "/getimages.php"
        self.dataPath = path + "/data"
        self.imgPath = path + "/img"
        self.modsPath = path + "/Mods"

    def loadProject(self, path):
        self.loadPath(path)
        self.getMods = []
        with open(self.getModsPath, "r", encoding="utf-8") as f:
            f.readline()
            for line in f.readlines():
                item = [i.split('=')[1].replace('\n', '') for i in line.split("&")[1:]]
                self.getMods.append(tuple(item))
        self.fileTree.loadFolder(self.dataPath)
        self.fileTree.loadFolder(self.imgPath)
        self.fileTree.loadFolder(self.modsPath)
        self.fileTree.loadFolder(self.getModsPath)
        self.fileTree.loadFolder(self.getimagesPath)

    def loadFile(self, filepath, treeView:QTreeWidget):
        if os.path.isfile(filepath):
            if filepath.endswith(".xml"):
                xmliter = etree.iterparse(filepath, events=('start','end'), encoding='UTF-8')
                treeView.addTopLevelItem(fast_iter(xmliter))
            if filepath.endswith(".xml") and os.path.split(filepath)[0].endswith('data'):
                xmliter = etree.iterparse(filepath, events=('start','end'), encoding='UTF-8')
                treeView.addTopLevelItem(get_info(xmliter))

    def loadPhp(self,filepath,tableView:QTableWidget):
        if os.path.isfile(filepath):
            offset = 0
            if os.path.basename(filepath) == 'getmods.php':
                tableView.setColumnCount(3)
                tableView.setHorizontalHeaderLabels(['modId','strModName','strModURL'])
                offset = 1
            elif os.path.basename(filepath) == 'getimages.php':
                tableView.setColumnCount(2)
                tableView.setHorizontalHeaderLabels(['imageId','strImageURL'])
                offset = 2
            with open(filepath,'r',encoding='utf-8') as f:
                text = ''.join(f.readlines()).replace('\n', '').split("&")[offset:]
                item = [i.split('=')[1] for i in text]
                if tableView.columnCount() == 3:
                    item = list(zip(item[::2],item[1::2]))
                tableView.setRowCount(len(item))
                for cnt, value in enumerate(item):
                    print(cnt,value)
                    tableView.setItem(cnt, 0, QTableWidgetItem(str(cnt)))
                    if tableView.columnCount() == 3:
                        tableView.setItem(cnt, 1, QTableWidgetItem(value[0]))
                        tableView.setItem(cnt, 2, QTableWidgetItem(value[1]))
                    else:
                        tableView.setItem(cnt, 1, QTableWidgetItem(value))


