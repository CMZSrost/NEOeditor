from PyQt5.QtWidgets import QTabWidget, QWidget, QTableWidget


class tabEditor(QTabWidget):
    def __init__(self, parent=None):
        super(tabEditor, self).__init__(parent)


    def itemChange(self, i, j):
        '''
        :param i:
        :param j:
        :param targetInfo: "modid_modname_type"
        :return:
        '''
        targetName = lambda x: x + '_' + self.sender().objectName().split('_')[-1]
        if self.sender().objectName().split('_')[0] == 'total':
            targetInfo = targetName(self.sender().item(i, 0).data(0))
        else:
            targetInfo = targetName('total')

        tablist = [self.tabText(i).replace('*','') for i in range(self.count())]  # 获取所有tab的名称: "modid_modname_type"
        if targetInfo in tablist:
            idx = tablist.index(targetInfo)
            targetTable = self.widget(idx).findChild(QTableWidget, targetInfo)
            item = targetTable.item(i, j)
            item.setData(0, self.sender().item(i, j).data(0))
            targetTable.fresh(item)
            if self.tabText(idx).find('*') == -1:
                self.setTabText(idx, self.tabText(idx) + '*')

        idx = self.currentIndex()
        if self.tabText(idx).find('*') == -1:
            self.setTabText(idx, self.tabText(idx) + '*')
