import os
import sys
import json
from PySide2.QtCore import QDir
from PySide2.QtWidgets import QWidget, QApplication, QFileDialog
from forms import Setup, Query, choosePaper


class Main(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化启动界面
        self.setup = Setup()
        self.setup.show()
        # 点击测试按钮就打开答题界面
        # 获得当前试卷
        self.current_paper = self.getCurrentPaper()
        if self.current_paper:
            # 如果存在当前试卷，则点击测试按钮，就直接打开答题界面
            self.setup.ui.pushButtonQuery.clicked.connect(self.openQuery)
        else:
            # 如果不存在当前试卷，则打开选则试卷对话框，选择一张试卷
            self.setup.ui.pushButtonQuery.clicked.connect(self.init_choose_paper)

    def init_choose_paper(self):
        self.choosePaper = choosePaper()
        self.choosePaper.show()
        self.choosePaper.ui.buttonBox.accepted.connect(self.openPaper)

    def openPaper(self):
        self.current_paper = self.choosePaper.data()
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

    def getCurrentPaper(self):
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
