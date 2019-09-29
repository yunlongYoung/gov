from PySide2.QtWidgets import QFileDialog


class choosePaper(QFileDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        filename = QFileDialog.getOpenFileName(self)
