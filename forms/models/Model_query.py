import json
from PySide2.QtCore import QStringListModel, QAbstractTableModel, Qt
from PySide2.QtGui import QStandardItemModel, QIcon, QStandardItem, QPixmap


class optionModel(QAbstractTableModel):
    def __init__(self, paper):
        super().__init__()
        with open(paper, encoding='utf-8') as f:
            self.dic = json.load(f)
        # 储存当前试卷
        self.current_test = paper
        # 储存当前题目
        self.current_num = 1
        self.max_index = max(int(i) for i in self.dic.keys())

    def rowCount(self, index):
        return 6

    def columnCount(self, index):
        return self.maxnum - 1

    def data(self, index, role=Qt.DisplayRole):
        # 如果index无效则返回0
        col = index.column + 1
        # if not index.isValid():
        #     return 1111111, 222, 33, 1
        # 如果以文本方式展现
        # 添加背景
        if 'backgroud' in self.dic[str(col)]:
            bg = self.dic[str(col)]['backgroud']
        else:
            bg = ''
        # 添加问题
        q = self.dic[str(col)]['question']
        # 添加答案，如果答案中有图片，则使用QIcon，否则使用stringList
        options = self.dic[str(col)]['options']
        if 'img' in options[0]:
            has_image = True
            model = QStandardItemModel()
            for i in range(4):
                img = options[i].split('"')[1]
                item = QStandardItem(QIcon(img), f'{chr(65+i)}.')
                model.appendRow(item)
        else:
            has_image = False
            model = QStringListModel()
            model.setStringList(options)
        return bg, q, model, has_image
