import sys
import json
from PySide2.QtWidgets import QMainWindow, QApplication, QDialog, QWidget
from PySide2.QtCore import QCoreApplication, QStringListModel,  Qt, QModelIndex, QElapsedTimer, QTimer
from PySide2.QtGui import QStandardItemModel, QIcon, QStandardItem, QPixmap
from .views import Ui_Query
from .models import queryModel


class Query(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Query()
        self.query_model = queryModel()
        self.index = QModelIndex()
        self.index.column = 0
        self.setQuery()
        self.init_signals()

    def init_signals(self):
        self.ui.about_close.connect(self.saveData)
        self.ui.question.ui.pushButtonPrevious.clicked.connect(
            self.previousQuestion)
        self.ui.question.ui.pushButtonNext.clicked.connect(
            self.nextQuestion)

    def setQuery(self):
        bg, q, model, has_image = self.query_model.data(
            self.index, Qt.DisplayRole)
        self.ui.setBackgroud(bg)
        self.ui.setQuestion(q)
        self.ui.setAnswers(model, has_image)

    def previousQuestion(self):
        self.index.column -= 1
        if self.index.column < 0:
            self.index.column = self.query_model.maxnum-1
        self.setQuery()
        # print(self.elapsed_time.elapsed())

    def nextQuestion(self):
        self.index.column += 1
        if self.index.column is self.query_model.maxnum:
            self.index.column = 0
        self.setQuery()
        # print(self.elapsed_time.elapsed())

    def saveData(self):
        print('saveData')
        # TODO 根据试卷名，把总时间保存到user_data中的json中


if __name__ == "__main__":
    app = QApplication()
    w = Query()
    sys.exit(app.exec_())
