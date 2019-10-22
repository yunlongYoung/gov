from PySide2.QtWidgets import QMainWindow, QSplitter, QTextEdit, QGraphicsView, QWidget
from PySide2.QtCore import Qt, Signal, QElapsedTimer, QTimer, QDateTime
from PySide2.QtGui import QIcon, QPixmap
from . import Ui_Question


class Question_panel(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Question()
        self.ui.setupUi(self)


class Ui_Query(QMainWindow):
    about_close = Signal()

    def __init__(self, totaltime=0):
        super().__init__()
        # 在主窗口左侧添加题干和选项
        lsplitter = QSplitter(Qt.Vertical)
        self.question_panel = Question_panel()
        lsplitter.addWidget(self.question_panel)
        # 在主窗口右侧添加绘图和文本编辑，并把比例设置为3比1
        rsplitter = QSplitter(Qt.Vertical)
        self.painter = QGraphicsView(rsplitter)
        self.note = QTextEdit(rsplitter)
        rsplitter.setStretchFactor(0, 3)
        rsplitter.setStretchFactor(1, 1)
        # 添加插件的顺序会导致左右不同
        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.addWidget(lsplitter)
        mainSplitter.addWidget(rsplitter)
        self.setCentralWidget(mainSplitter)
        # 点击暂停按钮切换图标和停继时间
        self.question_panel.ui.pushButtonPause.clicked.connect(
            self.toggle_play_and_pause
        )
        self.totaltime = totaltime  # 当前试卷答题总时间
        self.elapsed_time = QElapsedTimer()  # 答题总时间的计时器
        self.paused = False  # 默认刚打开时，还未暂停时间
        self.setTime()  # 更新时间显示
        self.timer = QTimer()
        self.timer.timeout.connect(self.setTime)  # 每秒更新时间显示的定时器

    def getDateTime(self):
        """获取当前日期及时间"""
        return QDateTime.currentDateTime().toTime_t()

    def setTime(self):
        """更新时间显示"""
        time = (
            self.elapsed_time.elapsed() + self.totaltime
        ) // 1000  # totaltime还包括上次答题所用的时间
        hours = time // 3600
        minutes = time % 3600 // 60
        seconds = time % 3600 % 60
        self.question_panel.ui.labelTimeUsed.setText(
            f"{hours}:{minutes:02}:{seconds:02}"
        )  # :02表示补全数字到2位，填充0

    def toggle_play_and_pause(self):
        if self.paused:
            # 继续计时
            # 把继续图标换回暂停图标
            icon_pause = QIcon()
            icon_pause.addPixmap(
                QPixmap(":/icons/icons/ic_pause_black_48dp.png"),
                QIcon.Normal,
                QIcon.Off,
            )
            self.question_panel.ui.pushButtonPause.setIcon(icon_pause)
            # 重新开始计时，包括1秒定时器和总时间计时器
            self.timer.start(1000)
            self.elapsed_time.restart()
            # 把自身状态标记为非暂停状态
            self.paused = False
        else:
            # 暂停计时
            icon_play = QIcon()
            icon_play.addPixmap(
                QPixmap(":/icons/icons/ic_play_arrow_black_48dp.png"),
                QIcon.Normal,
                QIcon.Off,
            )
            self.question_panel.ui.pushButtonPause.setIcon(icon_play)
            self.totaltime += self.elapsed_time.elapsed()
            self.timer.stop()
            self.paused = True

    def closeEvent(self, event):
        self.totaltime += self.elapsed_time.elapsed()  # 关闭前更新答题总时间
        self.about_close.emit()
