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
        if self.sender().objectName().split('_')[0] == 'total':
            targetInfo = self.sender().item(i, 0).data(0)+'_'+self.sender().objectName().split('_')[-1]
        else:
            targetInfo = 'total' + '_' + self.sender().objectName().split('_')[-1]
        tablist = [self.tabText(i) for i in range(self.count())]  # 获取所有tab的名称: "modid_modname_type"
        if targetInfo in tablist:
            targetTable = self.widget(tablist.index(targetInfo)).findChild(QTableWidget, targetInfo)
            targetTable.item(i, j).setData(0, self.sender().item(i, j).data(0))
