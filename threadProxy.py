from PyQt5.QtCore import QThread, pyqtSignal, QThreadPool, QRunnable, QObject, QMutex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtWidgets import QTableWidgetItem
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
        self.loadMutex = QMutex()

    def load_data(self, **kwargs):
        self.gen_worker(load_dat, emit=self.in_loading, mutex=self.loadMutex, **kwargs)
        self.in_loading(1)

    def setup_data(self, **kwargs):
        self.gen_worker(setup_dat, **kwargs)

    def gen_worker(self, func, emit=None, mutex=None, **kwargs):
        worker = func(emit=emit, mutex=mutex, **kwargs)
        self.pool.start(worker)

    def in_loading(self, i):
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

    def run(self):
        start = time()
        db = {}
        modInfoStr = f'{self.modInfo[0]}_{self.modInfo[1]}'
        if os.path.isdir(self.dirPath):
            for root, dirs, files in os.walk(self.dirPath):
                for file in files:
                    if os.path.basename(file).endswith('.xml'):
                        xmlIter = etree.iterparse(os.path.join(root, file), events=('end',), encoding='UTF-8')

                        filePath = (
                            os.path.join(root, file).replace(self.projectPath, '').replace('\\', '/'))  # data/或Mods/...
                        tempDB = data_iter(xmlIter, self.modInfo, filePath)

                        for i in tempDB.keys():
                            if i in db.keys():
                                db[i] = np.vstack((db[i], tempDB[i]))
                            else:
                                db[i] = np.array(tempDB[i], dtype=str)
        self.mutex.lock()
        self.gameData[modInfoStr] = db
        for i in db.keys():
            root = self.dataTree.get_top_item(modInfoStr)
            self.dataTree.add_node(i, root)
        self.mutex.unlock()
        self.emit(-1)
        print(f'{self.modInfo[1]} loaded in {time() - start} seconds')


class setup_dat(QRunnable):

    def __init__(self, emit, mutex, **kwargs):
        super(setup_dat, self).__init__()
        self.table = kwargs['table']
        self.data:np.ndarray = kwargs['data']
        self.emit = emit
        self.mutex = mutex

    def run(self):
        start = time()
        m, n = self.data.shape
        for i in range(m):
            for j in range(n):
                item = QTableWidgetItem(self.data[i, j])
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        print(f'data setup in {time() - start} seconds')
