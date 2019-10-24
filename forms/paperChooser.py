from PySide2.QtCore import QStringListModel, QDateTime
from PySide2.QtWidgets import QDialog
from .views import Ui_DialogPaperChooser
from forms.models import (
    dbSession,
    Paper,
    Question,
    Record,
    V_Question,
    Q_Record,
    Q_Property,
)


class paperChooser(QDialog):
    """用来选择试卷的对话框
    """

    def __init__(self):
        super().__init__()
        self.session = dbSession()
        # 获取：所有试卷
        self.test_papers = self.session.query(Paper).all()
        # 初始化：使用designer生成的UI
        self.ui = Ui_DialogPaperChooser()
        self.ui.setupUi(self)
        self.show_testkinds()
        self.setModal(True)
        # 信号连接
        #   改变：科目-> 适配：地区
        self.ui.comboBoxTestKinds.activated.connect(self.show_regions)
        #   改变：地区-> 适配：试卷
        self.ui.comboBoxRegion.activated.connect(self.show_papers)
        #   点击：试卷列表 -> 开放：确定按钮
        self.ui.listViewPapers.clicked.connect(self.enable_OK_button)

    def columns_to_view(self, columns, view):
        """把一个路径下的文件在view中显示出来
        
        Arguments:
            path {str} -- 科目、地区、试卷的路径
            view {object} -- 用来显示的UI组件
        """
        # 读取数据库所有row的某column
        # 1. column -> 模型
        # 2. 模型 -> view
        model = QStringListModel()
        model.setStringList(columns)
        view.setModel(model)

    def show_testkinds(self):
        # 显示：科目
        test_kinds = list(set(paper.test_kind for paper in self.test_papers))
        self.columns_to_view(test_kinds, self.ui.comboBoxTestKinds)
        # 禁用：确定按钮
        self.ui.buttonBox.setDisabled(True)

    def show_regions(self):
        # 获取：已选科目
        current_test_kind = self.ui.comboBoxTestKinds.currentText()
        # 1. 获取：地区
        # 2. 显示：地区
        self.papers = [
            paper for paper in self.test_papers if paper.test_kind == current_test_kind
        ]
        regions = list(set(paper.region for paper in self.papers))
        self.columns_to_view(regions, self.ui.comboBoxRegion)

    def show_papers(self):
        # 获取：已选地区
        current_region = self.ui.comboBoxRegion.currentText()
        # 1. 获取：试卷名
        # 2. 显示：试卷名
        self.papers = [paper for paper in self.papers if paper.region == current_region]
        names = [paper.year + paper.grade for paper in self.papers]
        self.columns_to_view(names, self.ui.listViewPapers)

    def enable_OK_button(self):
        index = self.ui.listViewPapers.currentIndex()
        chosen_paper_name = index.data()
        if chosen_paper_name:
            self.ui.buttonBox.setDisabled(False)
            # 根据选择框中的试卷名得到年和级别
            year = chosen_paper_name[:4]
            grade = chosen_paper_name[4:]
            # 查询科目、地区、年和级别都符合的试卷id
            for paper in self.papers:
                if paper.year == year and paper.grade == grade:
                    self.paper_id = paper.id
                    # print(self.paper_id)

    def new_record(self):
        # 此时已经点了确定按钮，可以开始计时
        time = QDateTime.currentDateTime().toTime_t()
        true_paper = Record(is_practice=False, start_datetime=time)
        self.session.add(true_paper)
        self.session.commit()
        # 用真题一一对应再建一套虚拟问题
        # 查询真题对应的所有question，然后放到虚拟问题里
        questions = (
            self.session.query(Question)
            .filter(Question.paper_id == self.paper_id)
            .all()
        )
        # print(questions)
        # 找到刚才建立的记录id
        record_id = self.session.query(Record).filter(Record.finished == False)[0].id
        v_questions = []
        i = 1
        for question in questions:
            v_question = V_Question(
                record_id=record_id, v_num=i, question_id=question.id
            )
            v_questions.append(v_question)
            i += 1
        self.session.add_all(v_questions)
        self.session.commit()
        v_questions = (
            self.session.query(V_Question)
            .filter(V_Question.record_id == record_id)
            .all()
        )
        q_records = []
        q_properties = []
        for v_question in v_questions:
            q_records.append(Q_Record(v_question_id=v_question.id))
            q_properties.append(Q_Property(v_question_id=v_question.id))
        self.session.add_all(q_records)
        self.session.add_all(q_properties)
        self.session.commit()
        self.session.close()
        return record_id
