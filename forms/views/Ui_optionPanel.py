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
    QDialog,
)


class optionButton(QPushButton):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        font = QFont()
        font.setPointSize(8)
        self.setMaximumSize(QSize(25, 18))
        self.setFont(font)
        # 字体颜色设置为红色
        self.setStyleSheet("color:red")
        self.setFlat(True)
        self.isChosen = False  # 储存toggle的状态
        self.clicked.connect(self.toggleChosen)

    def initUi(self):
        """初始化按钮的效果"""
        self.setText(self.name)
        self.setStyleSheet("color:red")
        # 重绘
        self.update()
        self.isChosen = False

    def choose(self):
        """模拟涂卡的效果"""
        self.setText("▆")
        self.setStyleSheet("color:black")
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
        self.btn.setFlat(True)
        self.btn.setStyleSheet("border-top: 1px solid red")
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
        if num % 5 is 0 and num % 20:
            vlayout.setContentsMargins(0, 1, 10, 3)
        else:
            vlayout.setContentsMargins(0, 1, 0, 3)

        vlayout.addWidget(self.btn)
        vlayout.addWidget(self.btnA)
        vlayout.addWidget(self.btnB)
        vlayout.addWidget(self.btnC)
        vlayout.addWidget(self.btnD)
        self.setLayout(vlayout)
        self.btnA.clicked.connect(self.chooseOption)
        self.btnB.clicked.connect(self.chooseOption)
        self.btnC.clicked.connect(self.chooseOption)
        self.btnD.clicked.connect(self.chooseOption)

    def chooseOption(self):
        """self.sender()方法能知道调用槽函数的发送者是谁，就不再需要lambda了"""
        btn = self.sender()
        isChosen = btn.isChosen
        self.btnA.initUi()
        self.btnB.initUi()
        self.btnC.initUi()
        self.btnD.initUi()
        if isChosen:
            btn.choose()
        else:
            btn.initUi()


class Ui_optionPanel(QDialog):
    def __init__(self, max_num):
        super().__init__()
        grid = QGridLayout()
        grid.setSpacing(0)
        option_groups = [optionsGroupButton(i) for i in range(1, max_num + 1)]
        positions = [(i, j) for i in range(7) for j in range(20)]
        for position, option_group in zip(positions, option_groups):
            grid.addWidget(option_group, *position)
        self.setLayout(grid)
        self.setModal(True)
        # 居中显示
        self.move((QDesktopWidget().width() - self.width() - 100) / 2, 0)
