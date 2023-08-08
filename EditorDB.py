import os
import re

from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem

from sourceTree import sourceTree
import xml.etree.ElementTree as ET




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
                with open(filepath,encoding='utf-8') as f:
                    text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", f.read())
                root = ET.fromstring(text)
                rootitem = QTreeWidgetItem()
                rootitem.setText(0, root.tag)
                treeView.addTopLevelItem(rootitem)
                def loadXML(item:QTreeWidgetItem,element:ET.Element):
                    for child in element:
                        childitem = QTreeWidgetItem()
                        print([child.tag,child.attrib])
                        childitem.setText(0, child.tag)
                        if child.text is not None:
                            childitem.setText(1, child.text)
                        if child.attrib is not None:
                            childitem.setText(2, str(child.attrib))
                        item.addChild(childitem)
                        loadXML(childitem, child)
                loadXML(rootitem,root)
