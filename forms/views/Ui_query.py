import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QSplitter, QTextEdit, QGraphicsView, QWidget, QTextBrowser, QGridLayout, QListView
from PySide2.QtCore import Qt, QStringListModel, QSize, Signal, QElapsedTimer, QTimer, QDateTime
from PySide2.QtGui import QTextDocumentFragment, QStandardItem, QIcon, QStandardItemModel, QPixmap
from . import Ui_Question


class Question(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Question()
        self.ui.setupUi(self)


class Ui_Query(QMainWindow):
    about_close = Signal()

    def __init__(self, totaltime=0):
        super().__init__()
        lsplitter = QSplitter(Qt.Vertical)
        self.question = Question()
        lsplitter.addWidget(self.question)

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
        self.question.ui.pushButtonPause.clicked.connect(
            self.toggle_play_and_pause)
        self.totaltime = totaltime
        self.timer = QTimer()
        self.elapsed_time = QElapsedTimer()
        self.paused = False
        self.setTime()
        self.timer.timeout.connect(self.setTime)

    def getDateTime(self):
        return QDateTime.currentDateTime().toTime_t()

    def setTime(self):
        time = (self.elapsed_time.elapsed() + self.totaltime)//1000
        hours = time//3600
        minutes = time % 3600//60
        seconds = time % 3600 % 60
        self.question.ui.labelTimeUsed.setText(
            f'{hours}:{minutes:02}:{seconds:02}')

    def toggle_play_and_pause(self):
        if self.paused:
            # continue the time
            icon_pause = QIcon()
            icon_pause.addPixmap(QPixmap(
                ":/icons/icons/ic_pause_black_48dp.png"), QIcon.Normal, QIcon.Off)
            self.question.ui.pushButtonPause.setIcon(icon_pause)
            self.timer.start(1000)
            self.elapsed_time.restart()
            self.paused = False
        else:
            # pause the time
            icon_play = QIcon()
            icon_play.addPixmap(QPixmap(
                ":/icons/icons/ic_play_arrow_black_48dp.png"), QIcon.Normal, QIcon.Off)
            self.question.ui.pushButtonPause.setIcon(icon_play)
            self.totaltime += self.elapsed_time.elapsed()
            self.timer.stop()
            self.paused = True

    def setBackgroud(self, background):
        self.question.ui.textEditBackground.setHtml(background)

    def setQuestion(self, question):
        if 'img' in question:
            self.question.ui.textEditQuestion.setMinimumHeight(200)
        self.question.ui.textEditQuestion.setHtml(question)

    def setOptions(self, model, has_image):
        if has_image:
            self.question.ui.listViewOptions.setViewMode(QListView.IconMode)
            self.question.ui.listViewOptions.setIconSize(QSize(100, 100))
            self.question.ui.listViewOptions.setMovement(QListView.Static)
            self.question.ui.listViewOptions.setSpacing(12)
            self.question.ui.listViewOptions.setMinimumHeight(230)
        self.question.ui.listViewOptions.setModel(model)

    def closeEvent(self, event):
        # print(self.total_time)
        # print(f'quit query:{self.getDateTime()}')
        self.totaltime += self.elapsed_time.elapsed()
        self.about_close.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_Query()
    w.showMaximized()
    sys.exit(app.exec_())
