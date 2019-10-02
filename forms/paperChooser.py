import os
from PySide2.QtCore import QDir, QStringListModel
from PySide2.QtWidgets import QDialog
from .views import Ui_DialogPaperChooser


class paperChooser(QDialog):
    """用来选择试卷的对话框
    """

    def __init__(self):
        super().__init__()
        # 获取：试卷所在的目录
        self.base_dir = os.path.join(QDir.currentPath(), "data")
        # 初始化：使用designer生成的UI
        self.ui = Ui_DialogPaperChooser()
        self.ui.setupUi(self)
        self.show_testkinds()
        self.setModal(True)
        # 信号连接
        #   改变：科目-> 适配：地区
        self.ui.comboBoxTestKinds.activated.connect(self.show_regions)
        #   改变：地区-> 适配：试卷
        self.ui.comboBoxRegion.activated.connect(self.show_papers)
        #   点击：试卷列表 -> 开放：确定按钮
        self.ui.listViewPapers.clicked.connect(self.enable_OK_button)

    def path_to_view(self, path, view, formatter=None):
        """把一个路径下的文件在view中显示出来
        
        Arguments:
            path {str} -- 科目、地区、试卷的路径
            view {object} -- 用来显示的UI组件
        """
        # 读取路径中的文件，不包含.和..
        # 1. 目录 -> 模型
        # 2. 模型 -> view
        li = QDir(path).entryList(QDir.NoDotAndDotDot | QDir.AllEntries)
        if formatter:  # 如果对于目录中的文件名，有格式化的规则，则应用它
            li = [formatter(i) for i in li]
        model = QStringListModel()
        model.setStringList(li)
        view.setModel(model)

    def show_testkinds(self):
        # 显示：科目
        self.path_to_view(self.base_dir, self.ui.comboBoxTestKinds)
        # 禁用：确定按钮
        self.ui.buttonBox.setDisabled(True)

    def show_regions(self):
        # 获取：科目
        self.current_test_kind = self.ui.comboBoxTestKinds.currentText()
        # 1. 获取：地区目录
        # 2. 显示：地区
        region_dir = os.path.join(self.base_dir, self.current_test_kind)
        self.path_to_view(region_dir, self.ui.comboBoxRegion)

    def show_papers(self):
        # 获取：地区
        self.current_region = self.ui.comboBoxRegion.currentText()
        # ! 使用txt目录，后期可能改变
        # 1. 获取：试卷目录
        # 2. 显示：试卷名
        paper_dir = os.path.join(
            self.base_dir, self.current_test_kind, self.current_region, "txt"
        )
        self.path_to_view(paper_dir, self.ui.listViewPapers, self.format_paper_name)

    def format_paper_name(self, paper):
        return paper.split(".")[0]

    def enable_OK_button(self):
        # 能不能在show_papers里就获得self.paper
        index = self.ui.listViewPapers.currentIndex()
        self.paper = index.data()
        if self.paper:
            self.ui.buttonBox.setDisabled(False)

    def data(self):
        return self.current_test_kind, self.current_region, self.paper
