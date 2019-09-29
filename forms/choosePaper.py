import os
from PySide2.QtCore import QDir, QStringListModel
from PySide2.QtWidgets import QDialog
from .views import Ui_DialogChoosePaper


class choosePaper(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.ui = Ui_DialogChoosePaper()
        self.ui.setupUi(self)
        self.base_dir = os.path.join(QDir.currentPath(), "data")
        self.initUi()
        if self.ui.comboBoxTestKinds.currentText():
            self.testKindChanged()
        self.ui.comboBoxTestKinds.currentTextChanged.connect(self.testKindChanged)
        self.ui.comboBoxRegion.currentTextChanged.connect(self.regionChanged)
        self.ui.listViewPapers.clicked.connect(self.paperChanged)
        self.paper = None

    def initUi(self):
        # 获得gov的当前目录，并进入其下的data目录
        # 获取data中的所有目录和文件，不包含.和..
        test_kinds = QDir(self.base_dir).entryList(
            QDir.NoDotAndDotDot | QDir.AllEntries
        )
        model = QStringListModel()
        model.setStringList(test_kinds)
        self.ui.comboBoxTestKinds.setModel(model)

    def testKindChanged(self):
        self.current_test_kind = self.ui.comboBoxTestKinds.currentText()
        region_dir = os.path.join(self.base_dir, self.current_test_kind)
        regions = QDir(region_dir).entryList(QDir.NoDotAndDotDot | QDir.AllEntries)
        model = QStringListModel()
        model.setStringList(regions)
        self.ui.comboBoxRegion.setModel(model)

    def regionChanged(self):
        self.current_region = self.ui.comboBoxRegion.currentText()
        # ! 使用txt文件来作为判断的依据
        paper_dir = os.path.join(
            self.base_dir, self.current_test_kind, self.current_region, "txt"
        )
        papers = QDir(paper_dir).entryList(QDir.NoDotAndDotDot | QDir.AllEntries)
        papers = [paper.split(".")[0] for paper in papers]
        self.paper_model = QStringListModel()
        self.paper_model.setStringList(papers)
        self.ui.listViewPapers.setModel(self.paper_model)

    def paperChanged(self):
        index = self.ui.listViewPapers.currentIndex()
        self.paper = self.paper_model.data(index)
