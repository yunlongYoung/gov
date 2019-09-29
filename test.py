import sys
import json
from PySide2 import QtCore, QtWidgets, QtGui


class Question(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel()
        self.buttonBox = QtWidgets.QDialogButtonBox()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


app = QtWidgets.QApplication()
q = Question()
q.show()
sys.exit(app.exec_())
