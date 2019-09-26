import os
import sys
import json
from PySide2.QtCore import QStringListModel
from PySide2.QtWidgets import QMainWindow
from .views import Ui_Query


class Query(QMainWindow):
    def __init__(self):
        super().__init__()
        # TODO 增加其他试卷data，这个self.paper文件也已经不存在
        # TODO self.loadQuestions也需要修改路径生成方式
        # TODO 改变使用数据库吧，东西太多了。。
        self.paper = 'D:/Desktop/gov/data/行测/国家/json/2007.json'
        self._questions, self._options = self.loadQuestions()
        self.max_num = max(int(s) for s in self._questions.keys())
        self.option_model = QStringListModel()
        self.operation, self.datetime, self.totaltime, self.chosen, self.current_num = self.loadData()
        # 使用答题已用时间初始化UI
        self.ui = Ui_Query(self.totaltime)
        self.initSignals()
        # 更新插件内容
        self.ui.question.ui.listViewOptions.setModel(self.option_model)
        self.updateQuestion()

    def loadQuestions(self):
        '''把options.json读取到model中，题目为option_model的self.num'''
        q = self.paper.replace('.', '_questions.')
        opt = self.paper.replace('.', '_options.')
        with open(q, encoding='utf-8') as f, open(opt, encoding='utf-8') as g:
            return(json.load(f), json.load(g))

    def genPath(self, suffix):
        '''根据文件名生成需要分类保存的文件名，如operation、datetime等'''
        return self.paper.replace('data', 'user_data').replace('/json', '').replace('.json', f'_{suffix}.json')

    def updateQuestion(self):
        self.ui.question.ui.textEditQuestion.setHtml(
            self._questions[str(self.current_num)])
        self.option_model.setStringList(self._options[str(self.current_num)])

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
        self.ui.question.ui.listViewOptions.clicked.connect(self.chooseOption)

    def loadData(self):
        '''从文件中读取操作、日期时间、已用时间、已选答案'''
        operation_path = self.genPath('operation')
        datetime_path = self.genPath('datetime')
        totaltime_path = self.genPath('totaltime')
        chosen_path = self.genPath('chosen')
        current_num_path = self.genPath('current_num')
        if not os.path.exists(operation_path):
            # 生成所有题目的空列表
            operation = {k: [] for k in range(1, self.max_num+1)}
            datetime = {k: [] for k in range(1, self.max_num+1)}
            # self.operation = dict.fromkeys(
            #     range(1, self.query_model.max_index+1), []) 这种方法有坑
            totaltime = 0
            chosen = {}
        else:
            with open(operation_path, encoding='utf-8') as f1, open(datetime_path, encoding='utf-8') as f2, open(totaltime_path, encoding='utf-8') as f3, open(chosen_path, encoding='utf-8') as f4:
                operation = json.load(f1)
                datetime = json.load(f2)
                totaltime = json.load(f3)
                chosen = json.load(f4)
        # 没有操作记录，也就不会有时间
        if not os.path.exists(current_num_path):
            current_num = 1
        else:
            with open(current_num_path, encoding='utf-8')as f5:
                current_num = json.load(f5)
        return operation, datetime, totaltime, chosen, current_num

    def add_operation_time(self, name):
        self.operation[str(self.current_num)].append(name)
        self.datetime[str(self.current_num)].append(self.ui.getDateTime())

    def previousQuestion(self):
        # 改变model，以改变view
        # print(f'self.chosen = {self.chosen}')
        self.add_operation_time('previous question')
        self.current_num -= 1
        if self.current_num is 0:
            self.current_num = self.max_num
        self.add_operation_time('passive start')
        self.updateQuestion()
        # 如果这道题已经被选过答案，则阴影突出答案

    def togglePauseQuestion(self):
        if self.ui.paused:
            self.add_operation_time('pause question')
        else:
            self.add_operation_time('continue question')

    def nextQuestion(self):
        # 改变model，以改变view
        # print(f'self.chosen = {self.chosen}')
        self.add_operation_time('next question')
        self.current_num += 1
        if self.current_num > self.max_num:
            self.current_num = 1
        self.add_operation_time('passive start')
        self.updateQuestion()
        # 如果这道题已经被选过答案，则阴影突出答案

    def chooseOption(self):
        # 0, 1, 2, 3代表 A, B, C, D
        choice = self.ui.question.ui.listViewOptions.currentIndex().row()
        self.chosen[str(self.current_num)] = choice
        print(choice)
        self.nextQuestion()

    def commitQuery(self):
        # TODO 这个提交需要终止答题
        self.add_operation_time('commit query')

    def quitAction(self):
        self.add_operation_time('quit query')
        print('saveing Data...')
        # self.paper = 'D:/Desktop/gov/data/行测/国家/json/2007.json'
        if self.ui.totaltime is 0:
            self.ui.totaltime = self.ui.elapsed_time.elapsed()
        operation_path = self.genPath('operation')
        datetime_path = self.genPath('datetime')
        totaltime_path = self.genPath('totaltime')
        chosen_path = self.genPath('chosen')
        current_num_path = self.genPath('current_num')
        # TODO 根据试卷名，把总时间保存到user_data中的json中
        with open(operation_path, 'w', encoding='utf-8') as f1, open(datetime_path, 'w', encoding='utf-8') as f2, open(totaltime_path, 'w', encoding='utf-8') as f3, open(chosen_path, 'w', encoding='utf-8') as f4, open(current_num_path, 'w', encoding='utf-8') as f5:
            json.dump(self.operation, f1, ensure_ascii=False)
            json.dump(self.datetime, f2, ensure_ascii=False)
            json.dump(self.ui.totaltime, f3, ensure_ascii=False)
            json.dump(self.chosen, f4, ensure_ascii=False)
            json.dump(self.current_num, f5, ensure_ascii=False)
