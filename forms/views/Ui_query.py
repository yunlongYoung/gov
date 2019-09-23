import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QSplitter, QTextEdit, QGraphicsView, QWidget, QTextBrowser, QGridLayout, QListView
from PySide2.QtCore import Qt, QStringListModel, QSize, Signal
from PySide2.QtGui import QTextDocumentFragment, QStandardItem, QIcon, QStandardItemModel, QPixmap
from . import Ui_Question


class Question(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Question()
        self.ui.setupUi(self)


class Ui_Query(QMainWindow):
    about_close = Signal()
    about_pause = Signal(int)

    def __init__(self):
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
        self.paused = False

    def toggle_play_and_pause(self):
        if self.paused:
            icon_pause = QIcon()
            icon_pause.addPixmap(QPixmap(
                ":/icons/icons/ic_pause_black_48dp.png"), QIcon.Normal, QIcon.Off)
            self.question.ui.pushButtonPause.setIcon(icon_pause)
            self.about_pause.emit(1)
            self.paused = False
        else:
            icon_play = QIcon()
            icon_play.addPixmap(QPixmap(
                ":/icons/icons/ic_play_arrow_black_48dp.png"), QIcon.Normal, QIcon.Off)
            self.question.ui.pushButtonPause.setIcon(icon_play)
            self.about_pause.emit(0)
            self.paused = True

    def setBackgroud(self, background):
        self.question.ui.textEditBackground.setHtml(background)

    def setQuestion(self, question):
        if 'img' in question:
            self.question.ui.textEditQuestion.setMinimumHeight(200)
        self.question.ui.textEditQuestion.setHtml(question)

    def setAnswers(self, model, has_image):
        if has_image:
            self.question.ui.listViewAnswers.setViewMode(QListView.IconMode)
            self.question.ui.listViewAnswers.setIconSize(QSize(100, 100))
            self.question.ui.listViewAnswers.setMovement(QListView.Static)
            self.question.ui.listViewAnswers.setSpacing(12)
            self.question.ui.listViewAnswers.setMinimumHeight(230)
        self.question.ui.listViewAnswers.setModel(model)

    def closeEvent(self, event):
        self.about_close.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_Query()
    w.showMaximized()
    sys.exit(app.exec_())
