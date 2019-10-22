import json
from PySide2.QtCore import QStringListModel
from PySide2.QtWidgets import QMainWindow, QPushButton
from .views import Ui_Query, Ui_optionPanel
from .models import (
    dbSession,
    Paper,
    Question,
    Record,
    V_Question,
    Question_Record,
    Question_Property,
    Question_Operation,
)


class Query(QMainWindow):
    """显示试卷和练习题的容器"""

    def __init__(self, record_id):
        super().__init__()
        self.record_id = record_id
        self.session = dbSession()
        # 获取答题总时间和当前题号
        self.totaltime, self.current_v_question_id, self.max_num = self.load_data(
            record_id
        )
        # 使用答题已用时间初始化UI
        self.ui = Ui_Query(self.totaltime)
        self.option_model = QStringListModel()
        self.ui.question_panel.ui.listViewOptions.setModel(self.option_model)
        self.update_question()
        # 信号连接
        self.ui.about_close.connect(self.quitAction)
        self.ui.question_panel.ui.pushButtonPrevious.clicked.connect(
            self.previousQuestion
        )
        self.ui.question_panel.ui.pushButtonPause.clicked.connect(
            self.togglePauseQuestion
        )
        self.ui.question_panel.ui.pushButtonNext.clicked.connect(self.nextQuestion)
        self.ui.question_panel.ui.pushButtonCommit.clicked.connect(self.commitQuery)
        self.ui.question_panel.ui.listViewOptions.clicked.connect(self.chooseOption)
        # TODO 能不能改进，当前index改变时
        self.ui.note.textChanged.connect(self.saveNote)
        self.ui.question_panel.ui.pushButtonChooseQuestion.clicked.connect(
            self.openOptionPanel
        )

    def load_data(self, record_id):
        record = self.session.query(Record).filter(Record.id == record_id)[0]
        totaltime = record.totaltime
        # ! 新建的试卷，此值为None
        current_v_question_id = record.last_v_question_id
        vqs = (
            self.session.query(V_Question)
            .filter(V_Question.record_id == record_id)
            .all()
        )
        max_num = len(vqs)
        if not current_v_question_id:
            # 把此值改为record_id相同的第一个
            # 记录的第一个是不是就是第一题？
            current_v_question_id = vqs[0].id
        return totaltime, current_v_question_id, max_num

    def update_question(self):
        v_question = (
            self.session.query(V_Question)
            .filter(V_Question.id == self.current_v_question_id)
            .one_or_none()
        )
        question_id = v_question.question_id
        question = (
            self.session.query(Question).filter(Question.id == question_id).first()
        )
        q = f"{question.num}. {question.question}"
        options = []
        options.append(question.A)
        options.append(question.B)
        options.append(question.C)
        options.append(question.D)
        self.ui.question_panel.ui.textEditQuestion.setHtml(q)
        self.option_model.setStringList(options)
        # 如果这道题已经被选过答案，则阴影突出答案
        record = (
            self.session.query(Question_Record)
            .filter(Question_Record.v_question_id == v_question.id)
            .one_or_none()
        )
        if record:
            row = record.chosen
            index = self.option_model.index(row, 0)
            self.ui.question_panel.ui.listViewOptions.setCurrentIndex(index)

    def openOptionPanel(self):
        self.optionPanel = Ui_optionPanel(self.max_num)
        # 根据131_0的格式，131为题号，0是选项A
        # 找到所有已经做了的题，把答案显示出来
        for k, v in self.chosen.items():
            if v != -1:
                btn = self.optionPanel.findChild(QPushButton, f"{k}_{v}")
                btn.set_button_chosen()
        self.optionPanel.show()
        # 找到所有的数字按钮，把点击他们的信号连接到跳转题目
        for i in range(1, self.max_num + 1):
            btn = self.optionPanel.findChild(QPushButton, str(i))
            btn.clicked.connect(self.goQuestion)
            for j in range(4):
                option_btn = self.optionPanel.findChild(QPushButton, f"{i}_{j}")
                option_btn.clicked.connect(self.connect_ui_and_model)

    def connect_ui_and_model(self):
        """点击答题卡，同样model中的数据也被修改，不只是UI"""
        option_btn = self.sender()
        name = option_btn.objectName()
        num, option = name.split("_")
        if option_btn.isChosen:
            self.chosen[num] = int(option)
        # else:
        #     self.chosen[num] = -1
        self.update_question()

    def goQuestion(self):
        """self.sender()方法能知道调用槽函数的发送者是谁，就不再需要lambda了"""
        btn = self.optionPanel.findChild(QPushButton, str(self.current_num))
        btn.setFlat(True)
        btn = self.sender()
        btn.setFlat(False)
        num = int(btn.objectName())
        self.current_virtual_question_id = num
        self.update_question()

    def add_operation_time(self, name):
        self.operation[str(self.current_num)].append(name)
        self.datetime[str(self.current_num)].append(self.ui.getDateTime())

    def previousQuestion(self):
        # 改变model，以改变view
        self.add_operation_time("previous question")
        self.current_num -= 1
        if self.current_num is 0:
            self.current_num = self.max_num
        self.add_operation_time("passive start")
        self.update_question()

    def togglePauseQuestion(self):
        if self.ui.paused:
            self.add_operation_time("pause question")
        else:
            self.add_operation_time("continue question")

    def nextQuestion(self):
        # 改变model，以改变view
        # print(f"self.chosen = {self.chosen}")
        self.add_operation_time("next question")
        self.current_num += 1
        if self.current_num > self.max_num:
            self.current_virtual_question_id = 1
        self.add_operation_time("passive start")
        self.update_question()

    def chooseOption(self):
        # TODO 还有BUG，实际保留到了前一个问题名下
        # 0, 1, 2, 3代表 A, B, C, D
        choice = self.ui.question_panel.ui.listViewOptions.currentIndex().row()
        self.chosen[str(self.current_num)] = choice
        # print(choice)
        self.nextQuestion()

    def commitQuery(self):
        # TODO 这个提交需要终止答题
        self.add_operation_time("commit query")
        print(self.getQuestionTime())

    def getQuestionTime(self):
        for i in self.datetime:
            # 如果有做题时间，即做过这道题
            datetime_list = self.datetime[i]
            if datetime_list:
                # 把datetime_list变成偶数长度
                if len(datetime_list) % 2:
                    datetime_list = datetime_list[:-1]
                # 两两相减再加一起
                total = 0
                j = 0
                while j < len(datetime_list):
                    total += datetime_list[j + 1] - datetime_list[j]
                    j += 2
                self.question_time[i] = total
        return self.question_time

    def saveNote(self):
        self.note[str(self.current_num)] = self.ui.note.toPlainText()

    def quitAction(self):
        self.add_operation_time("quit query")
        print("saveing Data into DB...")
        # self.paper = 'D:/Desktop/gov/data/行测/国家/json/2007.json'
        if self.ui.totaltime is 0:
            self.ui.totaltime = self.ui.elapsed_time.elapsed()
        # self.question_time = self.getQuestionTime()
        # operation_path = self.genPath("user_data", "operation")
        # datetime_path = self.genPath("user_data", "datetime")
        # totaltime_path = self.genPath("user_data", "totaltime")
        # chosen_path = self.genPath("user_data", "chosen")
        # current_num_path = self.genPath("user_data", "current_num")
        # question_time_path = self.genPath("user_data", "question_time")
        # note_path = self.genPath("user_data", "note")
        # # TODO 根据试卷名，把总时间保存到user_data中的json中
        # with open(operation_path, "w", encoding="utf-8") as f1, open(
        #     datetime_path, "w", encoding="utf-8"
        # ) as f2, open(totaltime_path, "w", encoding="utf-8") as f3, open(
        #     chosen_path, "w", encoding="utf-8"
        # ) as f4, open(
        #     current_num_path, "w", encoding="utf-8"
        # ) as f5, open(
        #     question_time_path, "w", encoding="utf-8"
        # ) as f6, open(
        #     note_path, "w", encoding="utf-8"
        # ) as f7, open(
        #     "D:/Desktop/gov/user_data/current_paper.json", "w", encoding="utf-8"
        # ) as f8:
        #     json.dump(self.operation, f1, ensure_ascii=False)
        #     json.dump(self.datetime, f2, ensure_ascii=False)
        #     json.dump(self.ui.totaltime, f3, ensure_ascii=False)
        #     json.dump(self.chosen, f4, ensure_ascii=False)
        #     json.dump(self.current_num, f5, ensure_ascii=False)
        #     json.dump(self.question_time, f6, ensure_ascii=False)
        #     json.dump(self.note, f7, ensure_ascii=False)
        #     json.dump([self.test_kind, self.region, self.paper], f8, ensure_ascii=False)
        # record = Record(
        #     test_kind="行测",
        #     region="国家",
        #     year=2007,
        #     grade="",
        #     chosen="1",
        #     num=1,
        #     question_time=123,
        # )

        # operation = [
        #     Operation(operation="open query", datetime=13132132, record_id=record.id),
        #     Operation(operation="quit query", datetime=13132135, record_id=record.id),
        # ]
        # self.session.add(record)
        # self.session.add_all(operation)
        # self.session.commit()
        # self.session.close()

