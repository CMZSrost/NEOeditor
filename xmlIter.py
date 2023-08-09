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

def get_info(context):
    """
    读取xml数据，并释放空间
    :params context: etree.iterparse生成的迭代器
    :params func:处理xml数据的func
    """
    # 事件、元素
    stack = deque()
    res = []
    maxlen=0
    for event, elem in context:
        if event == 'start':
            # 将元素压入栈
            stack.append(elem.attrib.values())
            maxlen=max(maxlen,len(stack))
        if event == 'end':
            # 处理xml数据
            if len(stack) == maxlen and elem.tag == "column":
                # print(stack[-1])
                if stack[-1][0] not in res:
                    res.extend(stack[-1])
            stack.pop()

            # 重置元素，清空元素内部数据
            elem.clear()
    res = "'"+"','".join(res)+"'"
    print(f'[{res}]')