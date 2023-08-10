import numpy as np
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class gameDB:
    def __init__(self, type, column: list, data: np.array):
        self.type = type
        self.column = column
        self.data = data



    def __setitem__(self, key, value):
        if isinstance(key, tuple) and isinstance(key[0], int) and len(key) == 2:
            column = key[1]
            if isinstance(column, str):
                column = self.column.index(column)
            if column == -1 or key[0] < 0:
                return None
            if key[0] >= self.data.shape[0]:
                self.data = np.append(self.data, np.zeros((1, len(self.column))), axis=0)
                self.table.setRowCount(self.data.shape[0])
            self.data[key[0]][column] = value
            self.table.setItem(key[0], column, QTableWidgetItem(str(value)))
        elif isinstance(key, int) and isinstance(value, list) and len(value) == len(self.column):
            if key < 0:
                return None
            if key >= self.data.shape[0]:
                self.data = np.append(self.data, np.zeros((1, len(self.column))), axis=0)
                self.table.setRowCount(self.data.shape[0])
            self.data[key] = value
            for i in range(len(value)):
                self.table.setItem(key, i, QTableWidgetItem(str(value[i])))

    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 2:
            column = key[1]
            if isinstance(column, str):
                column = self.column.index(column)
            if column != -1 and 0 <= key[0] <= self.data.shape[0]:
                return self.data[key[0]][column]
        elif isinstance(key, int):
            if 0 <= key <= self.data.shape[0]:
                return self.data[key]
        return None


    def __len__(self):
        return self.data.shape[0]

    def shape(self):
        return self.data.shape
