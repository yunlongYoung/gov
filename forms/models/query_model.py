import json
from PySide2.QtCore import QStringListModel, QAbstractTableModel, Qt
from PySide2.QtGui import QStandardItemModel, QIcon, QStandardItem, QPixmap


class queryModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        data = 'D:/Desktop/gov/data/行测/国家/json/paper/2007.json'
        with open(data, encoding='utf-8') as f:
            self.dic = json.load(f)
        # 储存当前试卷
        self.current_test = data
        # 储存当前题目
        self.current_num = 1
        self.maxnum = max(int(i) for i in self.dic.keys())

    def rowCount(self, index):
        return 6

    def columnCount(self, index):
        return self.maxnum - 1

    def data(self, index, role):
        # 如果index无效则返回0
        col = index.column + 1
        # if not index.isValid():
        #     return 1111111, 222, 33, 1
        # 如果以文本方式展现
        if role == Qt.DisplayRole:
            # 添加背景
            if 'bg' in self.dic[str(col)]:
                bg = self.dic[str(col)]['bg']
            else:
                bg = ''
            # 添加问题
            q = self.dic[str(col)]['q']
            # 添加答案，如果答案中有图片，则使用QIcon，否则使用stringList
            answers = self.dic[str(col)]['ans']
            if 'img' in answers[0]:
                has_image = True
                model = QStandardItemModel()
                for i in range(4):
                    img = answers[i].split('"')[1]
                    item = QStandardItem(QIcon(img), f'{chr(65+i)}.')
                    model.appendRow(item)
            else:
                has_image = False
                model = QStringListModel()
                model.setStringList(answers)
        return bg, q, model, has_image
