from PyQt5.QtCore import QThread, pyqtSignal, QThreadPool, QRunnable, QObject, QMutex
from time import time
import numpy as np
import os.path
from xmlIter import data_iter
from lxml import etree


class threadProxy(QObject):
    loadingStatusSign = pyqtSignal(int)

    def __init__(self, max_thread=8):
        super(threadProxy, self).__init__()
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(max_thread)
        self.loadingNum = 0
        self.mutex = QMutex()

    def load_data(self, **kwargs):
        worker = load_dat(emit=self.inLoading, mutex=self.mutex, **kwargs)
        self.pool.start(worker)
        self.inLoading(1)

    def inLoading(self, i):
        self.loadingNum += i
        self.loadingStatusSign['int'].emit(self.loadingNum)


class load_dat(QRunnable):

    def __init__(self, emit, mutex, **kwargs):
        super(load_dat, self).__init__()
        self.gameData = kwargs['gameData']
        self.dataTree = kwargs['dataTree']
        self.projectPath = kwargs['projectPath']
        self.dirPath = kwargs['dirPath']
        self.modInfo = kwargs['modInfo']
        self.emit = emit
        self.mutex = mutex
        print(f'loading data init {self.modInfo[1]}')

    def run(self):
        start = time()
        print(f'loading {self.modInfo[1]}')
        db_dict = set()
        if os.path.isdir(self.dirPath):
            for root, dirs, files in os.walk(self.dirPath):
                for file in files:
                    if os.path.basename(file).endswith('.xml'):
                        xmlIter = etree.iterparse(os.path.join(root, file), events=('end',), encoding='UTF-8')

                        filePath = (
                            os.path.join(root, file).replace(self.projectPath, '').replace('\\', '/'))  # data/或Mods/...
                        tempDB = data_iter(xmlIter, self.modInfo, filePath)

                        db_dict.update(tempDB.keys())
                        self.mutex.lock()
                        for i in tempDB.keys():
                            if i in self.gameData.keys():
                                self.gameData[i] = np.vstack((self.gameData[i], tempDB[i]))
                            else:
                                self.gameData[i] = np.array(tempDB[i], dtype=str)
                        self.mutex.unlock()
        self.mutex.lock()
        for i in db_dict:
            root = self.dataTree.get_top_item(f'{self.modInfo[0]}_{self.modInfo[1]}')
            self.dataTree.add_node(i, root)
        self.mutex.unlock()
        self.emit(-1)
        print(f'{self.modInfo[1]} loaded in {time() - start} seconds')
