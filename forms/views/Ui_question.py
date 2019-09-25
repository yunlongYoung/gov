# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Desktop\gov\forms\views\question.ui',
# licensing of 'd:\Desktop\gov\forms\views\question.ui' applies.
#
# Created: Wed Sep 25 11:41:51 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from . import Icons_rc
from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Question(object):
    def setupUi(self, Question):
        Question.setObjectName("Question")
        Question.resize(1085, 882)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Question)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEditBackground = QtWidgets.QTextEdit(Question)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textEditBackground.sizePolicy().hasHeightForWidth())
        self.textEditBackground.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.textEditBackground.setFont(font)
        self.textEditBackground.setReadOnly(True)
        self.textEditBackground.setObjectName("textEditBackground")
        self.verticalLayout_2.addWidget(self.textEditBackground)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEditQuestion = QtWidgets.QTextEdit(Question)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textEditQuestion.sizePolicy().hasHeightForWidth())
        self.textEditQuestion.setSizePolicy(sizePolicy)
        self.textEditQuestion.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.textEditQuestion.setFont(font)
        self.textEditQuestion.setReadOnly(True)
        self.textEditQuestion.setObjectName("textEditQuestion")
        self.verticalLayout.addWidget(self.textEditQuestion)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonCommit = QtWidgets.QPushButton(Question)
        self.pushButtonCommit.setMinimumSize(QtCore.QSize(50, 30))
        self.pushButtonCommit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonCommit.setObjectName("pushButtonCommit")
        self.horizontalLayout.addWidget(self.pushButtonCommit)
        spacerItem = QtWidgets.QSpacerItem(
            78, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.labelTimeUsed = QtWidgets.QLabel(Question)
        self.labelTimeUsed.setMinimumSize(QtCore.QSize(90, 30))
        self.labelTimeUsed.setText("")
        self.labelTimeUsed.setObjectName("labelTimeUsed")
        self.horizontalLayout.addWidget(self.labelTimeUsed)
        self.pushButtonPrevious = QtWidgets.QPushButton(Question)
        self.pushButtonPrevious.setMinimumSize(QtCore.QSize(50, 30))
        self.pushButtonPrevious.setMaximumSize(QtCore.QSize(50, 30))
        self.pushButtonPrevious.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/icons/icons/ic_skip_previous_black_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonPrevious.setIcon(icon)
        self.pushButtonPrevious.setIconSize(QtCore.QSize(25, 25))
        self.pushButtonPrevious.setObjectName("pushButtonPrevious")
        self.horizontalLayout.addWidget(self.pushButtonPrevious)
        self.pushButtonPause = QtWidgets.QPushButton(Question)
        self.pushButtonPause.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButtonPause.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButtonPause.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
            ":/icons/icons/ic_pause_black_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonPause.setIcon(icon1)
        self.pushButtonPause.setIconSize(QtCore.QSize(25, 25))
        self.pushButtonPause.setObjectName("pushButtonPause")
        self.horizontalLayout.addWidget(self.pushButtonPause)
        self.pushButtonNext = QtWidgets.QPushButton(Question)
        self.pushButtonNext.setMinimumSize(QtCore.QSize(50, 30))
        self.pushButtonNext.setMaximumSize(QtCore.QSize(50, 30))
        self.pushButtonNext.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(
            ":/icons/icons/ic_skip_next_black_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonNext.setIcon(icon2)
        self.pushButtonNext.setIconSize(QtCore.QSize(25, 25))
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.horizontalLayout.addWidget(self.pushButtonNext)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listViewOptions = QtWidgets.QListView(Question)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.listViewOptions.sizePolicy().hasHeightForWidth())
        self.listViewOptions.setSizePolicy(sizePolicy)
        self.listViewOptions.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.listViewOptions.setFont(font)
        self.listViewOptions.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listViewOptions.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.listViewOptions.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.listViewOptions.setTextElideMode(QtCore.Qt.ElideNone)
        self.listViewOptions.setSpacing(20)
        self.listViewOptions.setGridSize(QtCore.QSize(0, 30))
        self.listViewOptions.setObjectName("listViewOptions")
        self.verticalLayout.addWidget(self.listViewOptions)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(Question)
        QtCore.QMetaObject.connectSlotsByName(Question)

    def retranslateUi(self, Question):
        Question.setWindowTitle(
            QtWidgets.QApplication.translate("Question", "Form", None, -1))
        self.pushButtonCommit.setText(
            QtWidgets.QApplication.translate("Question", "交卷", None, -1))
