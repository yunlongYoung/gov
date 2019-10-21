import os
import sys
import json
from PySide2.QtCore import QDir
from PySide2.QtWidgets import QWidget, QApplication, QFileDialog
from forms import Setup, Query, paperChooser
from forms.models import dbSession, Record
from sqlalchemy import and_


class Main:
    def __init__(self):
        super().__init__()
        # 显示：启动界面
        self.setup = Setup()
        self.setup.show()
        self.session = dbSession()
        self.setup.ui.pushButtonQuery.clicked.connect(self.open_paper)

    def open_paper(self):
        def get_last_paper_id():
            """从数据库的True_Paper的最后一行读取数据
            如果表中没有行，或者最后一行已经finished，则返回None"""
            # and_:使用两个条件，即未完成的真题测试
            last_paper = (
                self.session.query(Record)
                .filter(and_(Record.finished == False, Record.is_practice == True))
                .one_or_none()
            )
            if last_paper:
                return last_paper.id
            else:
                return None

        last_paper_id = get_last_paper_id()
        if last_paper_id:  # 如果存在 上次试卷，则
            # 打开: 答题界面
            self.open_query(last_paper_id)
        else:  # 如果不存在 上次试卷，则
            # 打开：选择试卷对话框
            self.open_paperChooser()

    def open_paperChooser(self):
        """打开试卷选择对话框，并设置信号"""
        # 显示：选试卷对话框
        self.paper_chooser = paperChooser()
        self.paper_chooser.show()
        # 点击：确定按钮 -> 打开：选择的试卷
        self.paper_chooser.ui.buttonBox.accepted.connect(self.use_chosen_paper_id)

    def use_chosen_paper_id(self):
        """使用试卷选择对话框的数据，打开选定的试卷"""
        chosen_paper_id = self.paper_chooser.data()
        self.open_query(chosen_paper_id)

    def open_query(self, paper_id):
        """打开答题界面
        
        Arguments:
            paper {str tuple} -- (科目、地区、试卷名)
        """
        # 启动显示：答题界面
        self.query = Query(paper_id)
        self.query.ui.show()
        # 启动：定时器(每秒触发)
        self.query.ui.timer.start(1000)
        # 启动：答题总时间计时器
        self.query.ui.elapsed_time.start()
        # 记录：打开试卷时间
        self.query.add_operation_time("open query")
        # 完全打开答题界面后，再
        # 关闭：启动界面
        self.setup.close()


if __name__ == "__main__":
    app = QApplication()
    w = Main()
    sys.exit(app.exec_())
