# import os
# import sys
# import json
# from PySide2 import QtCore, QtWidgets, QtGui


# app = QtWidgets.QApplication()
# w = Question()
# w.show()
# sys.exit(app.exec_())


# from forms.models import (
#     dbSession,
#     Test_Paper,
#     Num,
#     Num_Property,
#     True_Paper,
#     Virtual_Paper,
#     Virtual_Num,
#     Num_Record,
#     Num_Operation,
#     Overtime,
#     Wrong,
#     Slow,
#     Finished,
#     Guessed,
# )


# session = dbSession()
import os

file = r"d:\Desktop\gov\data\行测\国家\json\2007_questions.json"


def _split(file, n):
    for i in range(n):
        file = os.path.split(file)[0]
    return os.path.split(file)[1]


print(_split(file, 3))

