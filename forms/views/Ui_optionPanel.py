import sys
import json
from PySide2.QtCore import QSize
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QWidget,
    QDesktopWidget,
)


class optionButton(QPushButton):
    def __init__(self, name):
        super().__init__(name)
        font = QFont()
        font.setPointSize(8)
        self.setMaximumSize(QSize(25, 18))
        self.setFont(font)
        # 字体颜色设置为红色
        self.setStyleSheet("color:red")
        self.isChosen = False  # 储存toggle的状态
        self.clicked.connect(self.toggleChosen)

    def initUi(self):
        """初始化按钮的效果"""
        self.setStyleSheet("color:red")
        # 重绘
        self.update()
        self.isChosen = False

    def choose(self):
        """全黑背景"""
        self.setStyleSheet("background-color:balck")
        self.update()
        self.isChosen = True

    def toggleChosen(self):
        """切换全黑和红字，模拟答题卡涂卡的效果"""
        if self.isChosen:
            self.initUi()
        else:
            self.choose()


class optionsGroupButton(QWidget):
    def __init__(self, num):
        super().__init__()
        self.btn = QPushButton(str(num))
        self.btn.setFixedSize(QSize(25, 25))
        self.btn.setObjectName(str(num))
        self.btnA = optionButton("[A]")
        self.btnA.setObjectName(str(num) + "_0")
        self.btnB = optionButton("[B]")
        self.btnB.setObjectName(str(num) + "_1")
        self.btnC = optionButton("[C]")
        self.btnC.setObjectName(str(num) + "_2")
        self.btnD = optionButton("[D]")
        self.btnD.setObjectName(str(num) + "_3")
        vlayout = QVBoxLayout()
        vlayout.setSpacing(0)
        vlayout.addWidget(self.btn)
        vlayout.addWidget(self.btnA)
        vlayout.addWidget(self.btnB)
        vlayout.addWidget(self.btnC)
        vlayout.addWidget(self.btnD)
        self.setLayout(vlayout)
        self.btnA.clicked.connect(lambda: self.chooseOption(self.btnA))
        self.btnB.clicked.connect(lambda: self.chooseOption(self.btnB))
        self.btnC.clicked.connect(lambda: self.chooseOption(self.btnC))
        self.btnD.clicked.connect(lambda: self.chooseOption(self.btnD))

    def chooseOption(self, btn):
        isChosen = btn.isChosen
        self.btnA.initUi()
        self.btnB.initUi()
        self.btnC.initUi()
        self.btnD.initUi()
        if isChosen:
            btn.choose()
        else:
            btn.initUi()


class Ui_optionPanel(QWidget):
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
