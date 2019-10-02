import os
import sys
import json
from PySide2.QtCore import QDir
from PySide2.QtWidgets import QWidget, QApplication, QFileDialog
from forms import Setup, Query, paperChooser


class Main:
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
                lambda: self.open_query(last_paper)
            )
        else:
            # 如果不存在 上次试卷，则
            # 1. 打开：选择试卷对话框
            # 2. 选择：试卷
            self.setup.ui.pushButtonQuery.clicked.connect(self.open_paperChooser)

    def get_last_paper(self):
        """从该路径获得当前试卷，没有当前试卷则返回None"""
        # 获得当前项目目录
        base_dir = QDir.currentPath()
        # 上次试卷路径
        last_paper_path = os.path.join(base_dir, "user_data", "current_paper.json")
        # 如果存在上次试卷，取得相关信息
        if os.path.exists(last_paper_path):
            with open(last_paper_path, encoding="utf-8") as f:
                return json.load(f)
        else:
            return None

    def open_paperChooser(self):
        """打开试卷选择对话框，并设置信号"""
        # 显示：选试卷对话框
        self.paper_chooser = paperChooser()
        self.paper_chooser.show()
        # 点击：确定按钮 -> 打开：选择的试卷
        self.paper_chooser.ui.buttonBox.accepted.connect(self.use_chosen_paper)

    def use_chosen_paper(self):
        """使用试卷选择对话框的数据，打开选定的试卷"""
        chosen_paper = self.paper_chooser.data()
        self.open_query(chosen_paper)

    def open_query(self, paper):
        """打开答题界面
        
        Arguments:
            paper {str tuple} -- (科目、地区、试卷名)
        """
        # 启动显示：答题界面
        self.query = Query(paper)
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
