# -*- coding:utf-8 -*-
import json
import os

from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt
from collections import deque


def fast_iter(context):
    stack = deque()
    for event, elem in context:
        if event == 'start':
            # 将元素压入栈
            item = QTreeWidgetItem()
            stack.append(item)
        if event == 'end':
            item = stack.pop()
            item.setText(0, elem.tag)
            if elem.text is not None:
                item.setFlags(Qt.ItemFlag(63))
                item.setText(1, elem.text)
            if elem.attrib is not None:
                item.setText(2, '\n'.join(f'{k}="{v}"' for k, v in elem.attrib.items()))
            if len(stack) == 0:
                root = item
            else:
                stack[-1].addChild(item)
            # 重置元素，清空元素内部数据
            elem.clear()
    return root


def get_info(context):
    stack = deque()
    res = []
    maxlen = 0
    for event, elem in context:
        if event == 'start':
            stack.append(elem.attrib.values())
            maxlen = max(maxlen, len(stack))
        if event == 'end':
            # 处理xml数据
            if len(stack) == maxlen and elem.tag == "column":
                if stack[-1][0] not in res:
                    res.extend(stack[-1])
            stack.pop()
            elem.clear()
    res = "'" + "','".join(res) + "'"
    print(f'[{res}]')


def data_iter(context, modinfo):
    DBdict = {}
    pos = -1
    table = {}
    for event, elem in context:
        if event == 'start':
            if elem.tag == "table":
                pos = elem.attrib.values()[0]
                if DBdict.get(pos) is None:
                    DBdict[pos] = []
                typelist = getColumn(pos)
                table = {}
                for i in typelist:
                    table[i] = ''
                table['modinfo'] = f'{modinfo[0]}_{modinfo[1]}'
                table["filepath"] = modinfo[2]
        elif event == 'end':
            if elem.tag == "column":
                name = elem.attrib.values()[0]
                if name in table.keys():
                    table[name] = elem.text
            elif elem.tag == "table":
                DBdict[pos].append(list(table.values()))
                table.clear()
            elem.clear()
    return DBdict

def getColumn(type):
    with open(os.path.join(os.getcwd(), 'templateFile', 'typelistTemplate.json'), 'r', encoding='utf-8') as f:
        column = ['modinfo']
        column.extend(json.load(f)[type])
        column.append('filepath')
        return column