from PyQt5.QtWidgets import QTabWidget, QTableWidget


class tabEditor(QTabWidget):
    def __init__(self, parent=None):
        super(tabEditor, self).__init__(parent)

    def item_change(self, i, j):
        """
        :param i:
        :param j:
        :return:
        """
        def target_name(x): return x + '_' + self.sender().objectName().split('_')[-1]
        if self.sender().objectName().split('_')[0] == 'total':
            targetInfo = target_name(self.sender().item(i, 0).data(0))
        else:
            targetInfo = target_name('total')

        tablist = [self.tabText(i).replace('*', '') for i in range(self.count())]  # 获取所有tab的名称: "modID_modname_type"
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
