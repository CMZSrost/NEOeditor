# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QTreeWidgetItem
from collections import deque


def fast_iter(context):
    """
    读取xml数据，并释放空间
    :params context: etree.iterparse生成的迭代器
    :params func:处理xml数据的func
    """
    # 事件、元素
    stack = deque()
    for event, elem in context:
        if event == 'start':
            # 将元素压入栈
            item = QTreeWidgetItem()
            stack.append(item)
        if event == 'end':
            # 处理xml数据
            item = stack.pop()
            item.setText(0, elem.tag)
            if elem.text is not None:
                item.setText(1, elem.text)
            if elem.attrib is not None:
                item.setText(2, str(elem.attrib))
            if len(stack) == 0:
                root = item
            else:stack[-1].addChild(item)
            # 重置元素，清空元素内部数据
            elem.clear()
    return root