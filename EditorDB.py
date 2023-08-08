import os
import re

from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem

from sourceTree import sourceTree
import xml.etree.ElementTree as ET
import lxml.etree as etree
from xmlIter import fast_iter




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

    def loadFile(self, filepath, treeView:QTreeWidget):
        print(filepath)
        if os.path.isfile(filepath):
            if filepath.endswith(".xml"):
                xmliter = etree.iterparse(filepath, events=('start','end'), encoding='UTF-8')
                treeView.addTopLevelItem(fast_iter(xmliter))
