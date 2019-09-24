import sys
import json
from PySide2.QtWidgets import QMainWindow, QApplication, QDialog, QWidget
from PySide2.QtCore import QCoreApplication, QStringListModel,  Qt, QModelIndex, QElapsedTimer, QTimer
from PySide2.QtGui import QStandardItemModel, QIcon, QStandardItem, QPixmap
from .views import Ui_Query
from .models import queryModel


class Query(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Query()
        # TODO 增加其他试卷data
        self.paper = 'D:/Desktop/gov/data/行测/国家/json/2007.json'
        self.query_model = queryModel(self.paper)
        self.index = QModelIndex()
        self.index.column = 0
        self.setQuery()
        self.initSignals()
        self.operation = {}
        self.datetime = {}
        self.loadData()

    def setQuery(self):
        bg, q, model, has_image = self.query_model.data(
            self.index, Qt.DisplayRole)
        self.ui.setBackgroud(bg)
        self.ui.setQuestion(q)
        self.ui.setAnswers(model, has_image)

    def initSignals(self):
        self.ui.about_close.connect(self.quitAction)
        self.ui.question.ui.pushButtonPrevious.clicked.connect(
            self.previousQuestion)
        self.ui.question.ui.pushButtonNext.clicked.connect(
            self.nextQuestion)
        self.ui.question.ui.pushButtonPause.clicked.connect(
            self.togglePauseQuestion)
        self.ui.question.ui.pushButtonCommit.clicked.connect(
            self.commitQuery)

    def loadData(self):
        # 没有操作记录，也就不会有时间
        if not self.operation:
            # 生成所有题目的空列表
            # self.operation = dict.fromkeys(
            #     range(1, self.query_model.max_index+1), []) 这种方法有坑
            self.operation = {k: []
                              for k in range(1, self.query_model.max_index+1)}
            self.datetime = {k: []
                             for k in range(1, self.query_model.max_index+1)}

    def add_operation_time(self, name):
        self.operation[self.index.column+1].append(name)
        self.datetime[self.index.column+1].append(self.ui.getDateTime())

    def previousQuestion(self):
        self.add_operation_time('previous question')
        self.index.column -= 1
        if self.index.column < 0:
            self.index.column = self.query_model.max_index-1
        self.add_operation_time('passive start')
        self.setQuery()
        # print(self.elapsed_time.elapsed())

    def togglePauseQuestion(self):
        if self.ui.paused:
            self.add_operation_time('pause question')
        else:
            self.add_operation_time('continue question')

    def nextQuestion(self):
        self.add_operation_time('next question')
        self.index.column += 1
        if self.index.column is self.query_model.max_index:
            self.index.column = 0
        self.add_operation_time('passive start')
        self.setQuery()
        # print(self.elapsed_time.elapsed())

    def commitQuery(self):
        # ! TODO 这个提交一定要终止答题，不然会出BUG
        self.add_operation_time('commit query')

    def quitAction(self):
        self.add_operation_time('quit query')
        print('saveing Data...')
        # self.paper = 'D:/Desktop/gov/data/行测/国家/json/2007.json'
        operation_path = self.paper.replace(
            'data', 'user_data').replace('json', 'operation', 1)
        datetime_path = self.paper.replace(
            'data', 'user_data').replace('json', 'datetime', 1)
        # TODO 根据试卷名，把总时间保存到user_data中的json中
        with open(operation_path, 'w', encoding='utf-8') as f, open(datetime_path, 'w', encoding='utf-8') as g:
            json.dump(self.operation, f, ensure_ascii=False)
            json.dump(self.datetime, g, ensure_ascii=False)


if __name__ == "__main__":
    app = QApplication()
    w = Query()
    sys.exit(app.exec_())
