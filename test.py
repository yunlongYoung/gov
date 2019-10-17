# import os
# import sys
# import json
# from PySide2 import QtCore, QtWidgets, QtGui


# app = QtWidgets.QApplication()
# w = Question()
# w.show()
# sys.exit(app.exec_())


from forms.models import (
    dbSession,
    Test_Paper,
    Num,
    Num_Property,
    True_Paper,
    Virtual_Paper,
    Virtual_Num,
    Num_Record,
    Num_Operation,
    Overtime,
    Wrong,
    Slow,
    Finished,
    Guessed,
)


session = dbSession()
