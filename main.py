import sys
from PySide2.QtWidgets import QWidget, QApplication
from forms import Setup, Query


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setup = Setup()
        self.query = Query()
        self.setup.show()
        # 点击测试按钮就打开答题界面
        self.setup.ui.pushButtonQuery.clicked.connect(self.openQuery)

    def openQuery(self):
        self.query.ui.timer.start(1000)
        self.query.ui.elapsed_time.start()
        self.query.ui.show()
        # 在操作表中增加打开试卷，并记录当前时间，题目为当前题目
        self.query.add_operation_time('open query')
        # 完全打开答题界面后，再关闭启动界面
        self.setup.close()


if __name__ == "__main__":
    app = QApplication()
    w = Main()
    sys.exit(app.exec_())