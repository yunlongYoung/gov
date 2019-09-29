import os
import sys
import json
from PySide2.QtWidgets import QWidget, QApplication, QFileDialog
from forms import Setup, Query, choosePaper


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setup = Setup()
        self.setup.show()
        # 点击测试按钮就打开答题界面
        self.setup.ui.pushButtonQuery.clicked.connect(self.openQuery)

    def openQuery(self):
        current_paper = self.getCurrentPaper()
        if not current_paper:
            current_paper = self.choosePaper()
        self.query = Query(current_paper)
        self.query.ui.timer.start(1000)
        self.query.ui.elapsed_time.start()
        self.query.ui.show()
        # 在操作表中增加打开试卷，并记录当前时间，题目为当前题目
        self.query.add_operation_time("open query")
        # 完全打开答题界面后，再关闭启动界面
        self.setup.close()

    def getCurrentPaper(self):
        if os.path.exists("D:/Desktop/gov/user_data/current_paper.json"):
            with open(
                "D:/Desktop/gov/user_data/current_paper.json", encoding="utf-8"
            ) as f:
                return json.load(f)
        else:
            return None

    def choosePaper(self):
        filename = QFileDialog.getOpenFileName(
            self, dir="D:/Desktop/gov/data/行测/国家/txt"
        )
        # self.choosePaper = choosePaper()
        # self.choosePaper.show()
        return filename[0]


if __name__ == "__main__":
    app = QApplication()
    w = Main()
    sys.exit(app.exec_())
