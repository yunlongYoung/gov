import os
import sys
import json
from PySide2.QtCore import QDir
from PySide2.QtWidgets import QWidget, QApplication, QFileDialog
from forms import Setup, Query, choosePaper


class Main(QWidget):
    def __init__(self):
        super().__init__()
        # 显示：启动界面
        self.setup = Setup()
        self.setup.show()
        #   获得：上次试卷
        last_paper = self.get_last_paper()
        if last_paper:
            # 如果存在 上次试卷，则
            # 点击：测试按钮 -> 打开: 答题界面
            self.setup.ui.pushButtonQuery.clicked.connect(
                lambda: self.openQuery(last_paper)
            )
        else:
            # 如果不存在 上次试卷，则
            # 1. 打开：选择试卷对话框
            # 2. 选择：试卷
            self.setup.ui.pushButtonQuery.clicked.connect(self.open_paper_chooser)

    def open_paper_chooser(self):
        # 显示：选试卷对话框
        self.paper_chooser = choosePaper()
        self.paper_chooser.show()
        # 点击：确定按钮 -> 调用：openPaper
        self.paper_chooser.ui.buttonBox.accepted.connect(self.openPaper)

    def openPaper(self):
        self.current_paper = self.paper_chooser.data()
        self.openQuery()

    def openQuery(self):
        # current_paper:tuple = (科目, 地区, 试卷名)
        self.query = Query(self.current_paper)
        self.query.ui.timer.start(1000)
        self.query.ui.elapsed_time.start()
        self.query.ui.show()
        # 在操作表中增加打开试卷，并记录当前时间，题目为当前题目
        self.query.add_operation_time("open query")
        # 完全打开答题界面后，再关闭启动界面
        self.setup.close()

    def get_last_paper(self):
        """从该路径获得当前试卷，没有当前试卷则返回None"""
        if os.path.exists("D:/Desktop/gov/user_data/current_paper.json"):
            with open(
                "D:/Desktop/gov/user_data/current_paper.json", encoding="utf-8"
            ) as f:
                return json.load(f)
        else:
            return None


if __name__ == "__main__":
    app = QApplication()
    w = Main()
    sys.exit(app.exec_())
