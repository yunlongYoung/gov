# import os
# import sys
# import json
# from PySide2 import QtCore, QtWidgets, QtGui


# app = QtWidgets.QApplication()
# w = Question()
# w.show()
# sys.exit(app.exec_())


from forms.models import dbSession, Test_Paper, Num, Record, Operation, Current

session = dbSession()
paper = session.query(Test_Paper).one()
# nums = session.query(Num).filter(Num.paper_id == paper.id).all()
num = session.query(Num).filter(Num.paper_id == paper.id).filter(Num.num == 2).one()
print(num.id)
print(num.paper_id)
print(num.question)
print(num.option_0)
print(num.option_1)
print(num.option_2)
