import sys
import json
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QWidget,
    QDesktopWidget,
)


def format_name(s):
    if "_0" in s:
        return "[A]"
    elif "_1" in s:
        return "[B]"
    elif "_2" in s:
        return "[C]"
    elif "_3" in s:
        return "[D]"
    else:
        return s


class optionButton(QPushButton):
    def __init__(self, name):
        super().__init__(name)
        font = QFont()
        font.setPointSize(8)
        self.setMaximumSize(QSize(25, 18))
        self.setFont(font)
        self.setStyleSheet("color:red")
        self.isChosen = False
        self.clicked.connect(self.toggleChosen)

    def toggleChosen(self):
        print("optionButton is clicked")
        if self.isChosen:
            self.setStyleSheet("background-color:balck")
            self.isChosen = True
        else:
            self.setStyleSheet("color:red")
            self.isChosen = False


class optionsGroupButton(QWidget):
    def __init__(self, num):
        super().__init__()
        btn = QPushButton(str(num))
        btn.setFixedSize(QSize(25, 25))
        btn.setObjectName(str(num))
        btnA = optionButton("[A]")
        btnA.setObjectName(str(num) + "_0")
        btnB = optionButton("[B]")
        btnB.setObjectName(str(num) + "_1")
        btnC = optionButton("[C]")
        btnC.setObjectName(str(num) + "_2")
        btnD = optionButton("[D]")
        btnD.setObjectName(str(num) + "_3")
        vlayout = QVBoxLayout()
        vlayout.setSpacing(2)
        vlayout.addWidget(btn)
        vlayout.addWidget(btnA)
        vlayout.addWidget(btnB)
        vlayout.addWidget(btnC)
        vlayout.addWidget(btnD)
        self.setLayout(vlayout)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            print("optionsGroupButton is clicked!")


class optionPanel(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        grid.setSpacing(0)
        option_groups = [optionsGroupButton(i) for i in range(1, 141)]
        positions = [(i, j) for i in range(7) for j in range(20)]
        for position, option_group in zip(positions, option_groups):
            grid.addWidget(option_group, *position)
        self.setLayout(grid)
        # 居中显示
        self.move((QDesktopWidget().width() - self.width() - 100) / 2, 0)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            print("optionPanel is clicked!")


app = QApplication()
op = optionPanel()
op.show()
sys.exit(app.exec_())
