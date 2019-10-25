from time import sleep
import json
from PySide2.QtCore import QStringListModel, QDateTime
from PySide2.QtWidgets import QMainWindow, QPushButton
from sqlalchemy import and_
from .views import Ui_Query, Ui_optionPanel
from .models import (
    dbSession,
    Paper,
    Question,
    Record,
    V_Question,
    Q_Record,
    Q_Property,
    Q_Operation,
    OP,
)


class Query(QMainWindow):
    """显示试卷和练习题的容器"""

    def __init__(self, record_id):
        super().__init__()
        self.record_id = record_id
        self.session = dbSession()
        # 获取答题总时间和当前题号
        self.totaltime, self.current_v_question_id, self.max_num = self.load_data()
        # 使用答题已用时间初始化UI
        self.ui = Ui_Query(self.totaltime)
        self.option_model = QStringListModel()
        self.ui.question_panel.ui.listViewOptions.setModel(self.option_model)
        self.update_question()
        # 信号连接
        self.ui.about_close.connect(self.quit_action)
        self.ui.question_panel.ui.pushButtonPrevious.clicked.connect(
            self.previous_question
        )
        self.ui.question_panel.ui.pushButtonPause.clicked.connect(
            self.toggle_pause_question
        )
        self.ui.question_panel.ui.pushButtonNext.clicked.connect(self.next_question)
        self.ui.question_panel.ui.pushButtonCommit.clicked.connect(self.commit_query)
        self.ui.question_panel.ui.listViewOptions.clicked.connect(self.choose_option)
        # TODO 能不能改进，当前index改变时
        self.ui.note.textChanged.connect(self.update_note)
        self.ui.question_panel.ui.pushButtonChooseQuestion.clicked.connect(
            self.open_option_panel
        )

    def load_data(self):
        record = self.session.query(Record).get(self.record_id)
        totaltime = record.totaltime
        # ! 新建的试卷，此值为None
        current_v_question_id = record.last_v_question_id
        if record.max_num:
            max_num = record.max_num
        else:
            # 所有问题的数量 -> 最大题号
            v_questions = (
                self.session.query(V_Question).filter_by(record_id=self.record_id).all()
            )
            max_num = len(v_questions)
            record.max_num = max_num
            self.session.commit()
        if not current_v_question_id:
            # 把此值改为record_id相同的第一个
            # 记录的第一个是不是就是第一题？
            current_v_question_id = v_questions[0].id
        return totaltime, current_v_question_id, max_num

    def update_question(self):
        v_question = self.session.query(V_Question).get(self.current_v_question_id)
        question = self.session.query(Question).get(v_question.question_id)
        q = f"{question.num}. {question.question}"
        options = []
        options.append(f"A. {question.A}")
        options.append(f"B. {question.B}")
        options.append(f"C. {question.C}")
        options.append(f"D. {question.D}")
        self.ui.question_panel.ui.textEditQuestion.setHtml(q)
        self.option_model.setStringList(options)
        # 如果这道题已经被选过答案，则阴影突出答案
        record = self.session.query(Q_Record).get(v_question.id)
        if record:
            row = record.chosen
            index = self.option_model.index(row, 0)
            self.ui.question_panel.ui.listViewOptions.setCurrentIndex(index)

    def add_operation_time(self, operation):
        question_operation = Q_Operation(
            v_question_id=self.current_v_question_id,
            operation=operation,
            datetime=QDateTime.currentDateTime().toTime_t(),
        )
        self.session.add(question_operation)
        self.session.commit()

    def previous_question(self):
        # 改变model，以改变view
        self.add_operation_time(OP.PREVIOUS_QUESTION)
        self.current_v_question_id -= 1
        v_question = self.session.query(V_Question).get(self.current_v_question_id)
        if not v_question or v_question.record_id != self.record_id:
            self.current_v_question_id += self.max_num
        self.add_operation_time(OP.PASSIVE_START)
        self.update_question()

    def toggle_pause_question(self):
        if self.ui.paused:
            self.add_operation_time(OP.PAUSE_QUESTION)
        else:
            self.add_operation_time(OP.CONTINUE_QUESTION)

    def next_question(self):
        # 改变model，以改变view
        self.add_operation_time(OP.NEXT_QUESTION)
        self.current_v_question_id += 1
        v_question = self.session.query(V_Question).get(self.current_v_question_id)
        if not v_question or v_question.record_id != self.record_id:
            self.current_v_question_id -= self.max_num
        self.add_operation_time(OP.PASSIVE_START)
        self.update_question()

    def choose_option(self):
        # 0, 1, 2, 3代表 A, B, C, D
        choice = self.ui.question_panel.ui.listViewOptions.currentIndex().row()
        q_record = self.session.query(Q_Record).get(self.current_v_question_id)
        if q_record:
            q_record.chosen = choice
        else:
            q_record = Q_Record(v_question_id=self.current_v_question_id, chosen=choice)
            self.session.add(q_record)
        self.session.commit()
        # print(choice)
        self.next_question()

    def open_option_panel(self):
        self.optionPanel = Ui_optionPanel(self.max_num)
        # 根据131_0的格式，131为题号，0是选项A
        # 找到所有已经做了的题，把答案显示出来
        v_questions = (
            self.session.query(V_Question).filter_by(record_id=self.record_id).all()
        )
        for v_question in v_questions:
            v_num = v_question.v_num
            q_record = self.session.query(Q_Record).get(v_question.id)
            if q_record:
                chosen = q_record.chosen
                if chosen != -1:
                    btn = self.optionPanel.findChild(QPushButton, f"{v_num}_{chosen}")
                    btn.set_button_chosen()
        self.optionPanel.show()
        # 找到所有的数字按钮，把点击他们的信号连接到跳转题目
        for i in range(1, self.max_num + 1):
            btn = self.optionPanel.findChild(QPushButton, str(i))
            btn.clicked.connect(self.goto_question)
            for j in range(4):
                option_btn = self.optionPanel.findChild(QPushButton, f"{i}_{j}")
                # TODO 这个信号连接不太优雅
                option_btn.clicked.connect(self.choose_with_option_panel)

    def choose_with_option_panel(self):
        """点击答题卡，同样db中的数据也被修改，不只是UI"""
        option_btn = self.sender()
        name = option_btn.objectName()
        v_num, chosen = name.split("_")
        v_question = (
            self.session.query(V_Question)
            .filter_by(record_id=self.record_id, v_num=int(v_num))
            .one_or_none()
        )
        q_record = self.session.query(Q_Record).get(v_question.id)
        # 如果鼠标点击的按钮为选中状态，则在db中也选中该选项
        # 如果鼠标点击的按钮为非选中状态，则该题没有任何选项被选中
        if option_btn.isChosen:
            q_record.chosen = int(chosen)
        else:
            q_record.chosen = -1
        self.session.commit()
        self.update_question()

    def goto_question(self):
        """self.sender()方法能知道调用槽函数的发送者是谁，就不再需要lambda了"""
        self.add_operation_time(OP.GOTO_QUESTION)
        btn = self.sender()
        v_num = int(btn.objectName())
        v_question = (
            self.session.query(V_Question)
            .filter_by(record_id=self.record_id, v_num=v_num)
            .one_or_none()
        )
        self.current_v_question_id = v_question.id
        self.add_operation_time(OP.PASSIVE_START)
        self.update_question()

    def commit_query(self):
        # TODO 这个提交需要终止答题
        self.add_operation_time(OP.COMMIT_QUERY)
        self.count_question_time()
        # finished变为True
        record = (
            self.session.query(Record)
            .filter_by(id=self.record_id, is_practice=False)
            .one_or_none()
        )
        record.finished = True
        self.session.commit()

    def count_question_time(self):
        # 查询所有v_questions
        v_questions = (
            self.session.query(V_Question).filter_by(record_id=self.record_id).all()
        )
        # 对于每个v_question，到Q_Operation中去查找有无operation
        datetimes = []
        for v_question in v_questions:
            operations = (
                self.session.query(Q_Operation)
                .filter_by(v_question_id=v_question.id)
                .all()
            )
            if operations:
                datetimes = [operation.datetime for operation in operations]
                # 两两成对，舍去最后一位
                if len(datetimes) % 2:
                    datetimes = datetimes[:-1]
                total = 0
                j = 0
                # 将每两位的差加在一起，就是该问题的总时间
                while j < len(datetimes):
                    total += datetimes[j + 1] - datetimes[j]
                    j += 2
                q_record = self.session.query(Q_Record).get(v_question.id)
                q_record.question_time = total
        self.session.commit()

    def update_note(self):
        # TODO 能不能做题时只显示本次做题的note
        # TODO 交卷时显示历次的note
        note = self.ui.note.toPlainText()
        q_record = self.session.query(Q_Record).get(self.current_v_question_id)
        q_record.note = note
        self.session.commit()

    def quit_action(self):
        self.add_operation_time(OP.QUIT_QUERY)
        print("saveing Data into DB...")
        # 如果本试卷还没有交卷，则计算question_time，否则不再计算question_time
        record = self.session.query(Record).get(self.record_id)
        if not record.finished:
            self.count_question_time()
        if self.ui.totaltime is 0:
            # ! totaltime的单位是毫秒
            self.ui.totaltime = self.ui.elapsed_time.elapsed()
        record.totaltime = self.ui.totaltime
        record.last_v_question_id = self.current_v_question_id
        self.session.commit()
