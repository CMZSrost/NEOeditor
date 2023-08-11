# -*- coding:utf-8 -*-
import json
import os

from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt
from collections import deque
from lxml.etree import iterparse

def fast_iter(context:iterparse):
    stack = deque()
    flag = True
    for event, elem in context:
        if flag:
            comment = elem.xpath('//comment()')
            flag = False
        if event == 'start':
            # 将元素压入栈
            item = QTreeWidgetItem()
            stack.append(item)
            while len(comment) > 0 and elem.sourceline >= comment[0].sourceline and len(stack) > 0:
                com = QTreeWidgetItem()
                com.setText(0, '<!---->')
                com.setText(1, comment[0].text)
                com.setData(3, 0, comment[0].sourceline)
                comment.pop(0)
                stack[-1].addChild(com)
        elif event == 'end':
            item = stack.pop()
            item.setText(0, elem.tag)
            item.setData(3, 0, elem.sourceline)
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


def data_iter(context, modInfo, filePath):
    DBdict = {}
    for event, elem in context:
        if elem.tag == "table":
            pos = elem.attrib.values()[0]
            typelist = get_column(pos)
            if DBdict.get(pos) is None:
                DBdict[pos] = []

            table = {i: '' for i in typelist}
            table['modinfo'] = f'{modInfo[0]}_{modInfo[1]}'
            table["filepath"] = filePath
            table.update({i.attrib.values()[0]: i.text for i in elem.xpath('column')})

            DBdict[pos].append([table[i] for i in typelist])
            table.clear()
    return DBdict

def get_column(type):
    with open(os.path.join(os.getcwd(), 'templateFile', 'typelistTemplate.json'), 'r', encoding='utf-8') as f:
        column = ['modinfo']
        column.extend(json.load(f)[type])
        column.append('filepath')
        return column