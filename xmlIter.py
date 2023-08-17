import json
import os
from collections import deque

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem
from lxml.etree import iterparse, Element


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
            item.setData(3, 0, elem.sourceline)
            stack.append(item)
            while len(comment) > 0 and elem.sourceline >= comment[0].sourceline and len(stack) > 0:
                com = QTreeWidgetItem()
                com.setText(0, '<!---->')
                com.setText(1, comment[0].text)
                com.setFlags(Qt.ItemFlag(63))
                com.setData(3, 0, comment[0].sourceline)
                comment.pop(0)
                stack[-1].addChild(com)
        elif event == 'end':
            item = stack.pop()
            item.setText(0, elem.tag)
            if elem.text is not None and elem.tag == 'column':
                item.setFlags(Qt.ItemFlag(63))
                item.setText(1, elem.text)
            if elem.attrib is not None:
                item.setText(2, ''.join(list(elem.attrib.values())))
            if len(stack) == 0:
                root = item
            else:
                stack[-1].addChild(item)

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
    with open(os.path.join(os.getcwd(), 'jsonData', 'typelistTemplate.json'), 'r', encoding='utf-8') as f:
        column = ['modinfo']
        column.extend(json.load(f)[type])
        column.append('filepath')
        return column


def gen_xml_table(typ, column, data):
    if len(column) != len(data):
        print('column and data must have same length')
        print(column)
        print(data)

    tableAttrib = {'name': typ}
    table = Element('table', attrib=tableAttrib)
    childs = []
    for k, v in zip(column, data):
        attrib = {'name': k}
        child = Element('column', attrib=attrib)
        child.text = v
        childs.append(child)
    table.extend(childs)
    return table