# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Desktop\gov\UI\setup.ui',
# licensing of 'd:\Desktop\gov\UI\setup.ui' applies.
#
# Created: Mon Sep 16 08:08:07 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Setup(object):
    def setupUi(self, Setup):
        Setup.setObjectName("Setup")
        Setup.resize(210, 243)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Setup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButtonQuery = QtWidgets.QPushButton(Setup)
        self.pushButtonQuery.setObjectName("pushButtonQuery")
        self.verticalLayout.addWidget(self.pushButtonQuery)
        spacerItem2 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButtonPractice = QtWidgets.QPushButton(Setup)
        self.pushButtonPractice.setObjectName("pushButtonPractice")
        self.verticalLayout.addWidget(self.pushButtonPractice)
        spacerItem3 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.pushButtonProfile = QtWidgets.QPushButton(Setup)
        self.pushButtonProfile.setObjectName("pushButtonProfile")
        self.verticalLayout.addWidget(self.pushButtonProfile)
        spacerItem4 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.pushButtonSetup = QtWidgets.QPushButton(Setup)
        self.pushButtonSetup.setObjectName("pushButtonSetup")
        self.verticalLayout.addWidget(self.pushButtonSetup)
        spacerItem5 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Setup)
        QtCore.QMetaObject.connectSlotsByName(Setup)

    def retranslateUi(self, Setup):
        Setup.setWindowTitle(QtWidgets.QApplication.translate("Setup", "公考", None, -1))
        self.pushButtonQuery.setText(QtWidgets.QApplication.translate("Setup", "测试", None, -1))
        self.pushButtonPractice.setText(QtWidgets.QApplication.translate("Setup", "练习", None, -1))
        self.pushButtonProfile.setText(QtWidgets.QApplication.translate("Setup", "个人数据", None, -1))
        self.pushButtonSetup.setText(QtWidgets.QApplication.translate("Setup", "设置", None, -1))

