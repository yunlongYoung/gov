# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Desktop\gov\forms\views\paperChooser.ui',
# licensing of 'd:\Desktop\gov\forms\views\paperChooser.ui' applies.
#
# Created: Wed Oct  2 14:26:06 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DialogPaperChooser(object):
    def setupUi(self, DialogPaperChooser):
        DialogPaperChooser.setObjectName("DialogPaperChooser")
        DialogPaperChooser.resize(176, 283)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(DialogPaperChooser)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTestKinds = QtWidgets.QLabel(DialogPaperChooser)
        self.labelTestKinds.setObjectName("labelTestKinds")
        self.verticalLayout.addWidget(self.labelTestKinds)
        self.comboBoxTestKinds = QtWidgets.QComboBox(DialogPaperChooser)
        self.comboBoxTestKinds.setObjectName("comboBoxTestKinds")
        self.verticalLayout.addWidget(self.comboBoxTestKinds)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelRegion = QtWidgets.QLabel(DialogPaperChooser)
        self.labelRegion.setObjectName("labelRegion")
        self.verticalLayout_2.addWidget(self.labelRegion)
        self.comboBoxRegion = QtWidgets.QComboBox(DialogPaperChooser)
        self.comboBoxRegion.setObjectName("comboBoxRegion")
        self.verticalLayout_2.addWidget(self.comboBoxRegion)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.listViewPapers = QtWidgets.QListView(DialogPaperChooser)
        self.listViewPapers.setObjectName("listViewPapers")
        self.verticalLayout_3.addWidget(self.listViewPapers)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogPaperChooser)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.retranslateUi(DialogPaperChooser)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DialogPaperChooser.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DialogPaperChooser.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogPaperChooser)

    def retranslateUi(self, DialogPaperChooser):
        DialogPaperChooser.setWindowTitle(QtWidgets.QApplication.translate("DialogPaperChooser", "Dialog", None, -1))
        self.labelTestKinds.setText(QtWidgets.QApplication.translate("DialogPaperChooser", "科目", None, -1))
        self.labelRegion.setText(QtWidgets.QApplication.translate("DialogPaperChooser", "省份", None, -1))

