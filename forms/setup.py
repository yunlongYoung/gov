from PySide2.QtWidgets import QDialog
from .views import Ui_Setup


class Setup(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Setup()
        self.ui.setupUi(self)
