import os
import sys
import json
from PySide2 import QtCore, QtWidgets, QtGui


class Question(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel("2017")
        self.button = QtWidgets.QPushButton("Hello!")
        # self.buttonBox = QtWidgets.QDialogButtonBox()
        # self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.accept)
        self.i = 1

    def accept(self):
        self.button.setFlat(bool(self.i))
        self.i = abs(self.i - 1)


app = QtWidgets.QApplication()
q = Question()
q.show()
sys.exit(app.exec_())

