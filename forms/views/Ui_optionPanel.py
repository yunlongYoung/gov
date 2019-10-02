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
    """option button on the scantron"""

    def __init__(self, name):
        """name: button text
        """
        super().__init__(name)
        # font -> 宋体 8 px
        # font color -> red
        # background -> transpanrent
        font = QFont("宋体", 8)
        self.setFont(font)
        self.setMaximumSize(QSize(25, 18))
        self.setStyleSheet("color:red")
        self.setFlat(True)
        self.name = name
        # if this option is chosen (option is among ABCD)
        self.isChosen = False
        # toggle the choose state
        self.clicked.connect(self.toggle_chosen)

    def set_button_origin(self):
        """set button origin style
        """
        # set: button text
        # font color -> red
        self.setText(self.name)
        self.setStyleSheet("color:red")
        # repaint
        self.update()
        self.isChosen = False

    def set_button_chosen(self):
        """simulate coating card
        """
        self.setText("▆")
        self.setStyleSheet("color:black")
        self.update()
        self.isChosen = True

    def toggle_chosen(self):
        """
        toggle text between rectangle & A|B|C|D
        toggle color between red|black
        """
        if self.isChosen:
            self.set_button_origin()
        else:
            self.set_button_chosen()


class optionsGroupButton(QWidget):
    """orgnize ABCD 4 options together"""

    def __init__(self, num):
        super().__init__()
        name = str(num)
        # set button text
        # set object name for later finding
        self.btn = QPushButton(name)
        self.btn.setFixedSize(QSize(25, 25))
        self.btn.setObjectName(name)
        self.btn.setFlat(True)
        self.btn.setStyleSheet("border-top: 1px solid red")
        self.btnA = optionButton("[A]")
        self.btnA.setObjectName(name + "_0")
        self.btnB = optionButton("[B]")
        self.btnB.setObjectName(name + "_1")
        self.btnC = optionButton("[C]")
        self.btnC.setObjectName(name + "_2")
        self.btnD = optionButton("[D]")
        self.btnD.setObjectName(name + "_3")
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.btn)
        vlayout.addWidget(self.btnA)
        vlayout.addWidget(self.btnB)
        vlayout.addWidget(self.btnC)
        vlayout.addWidget(self.btnD)
        # set no space between these buttons
        vlayout.setSpacing(0)
        # put space in every 5 question column
        if num % 5 is 0 and num % 20:
            vlayout.setContentsMargins(0, 1, 10, 3)
        else:
            vlayout.setContentsMargins(0, 1, 0, 3)
        self.setLayout(vlayout)
        # click button ->
        self.btnA.clicked.connect(self.toggle_chosen_option)
        self.btnB.clicked.connect(self.toggle_chosen_option)
        self.btnC.clicked.connect(self.toggle_chosen_option)
        self.btnD.clicked.connect(self.toggle_chosen_option)

    def toggle_chosen_option(self):
        """sender makes possible to know which button is clicked"""
        sender = self.sender()  # the clicked button
        # toggle the style for clicked button
        # set remain buttons to origin style
        for btn in (self.btnA, self.btnB, self.btnC, self.btnD):
            if btn is sender:
                btn.toggle_chosen()
            else:
                btn.set_button_origin()

class Ui_optionPanel(QDialog):
    def __init__(self, max_num):
        super().__init__()
        grid = QGridLayout()
        grid.setSpacing(0)
        # generate 135 or 140 button groups
        # arrange them in positon 7 rows and 20 columns
        option_groups = [optionsGroupButton(i) for i in range(1, max_num + 1)]
        positions = [(i, j) for i in range(7) for j in range(20)]
        for position, option_group in zip(positions, option_groups):
            grid.addWidget(option_group, *position)
        self.setLayout(grid)
        self.setModal(True)
        # center this widget
        self.move((QDesktopWidget().width() - self.width() - 100) / 2, 0)
