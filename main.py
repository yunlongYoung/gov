import sys
from PySide2.QtWidgets import QWidget, QApplication
from forms import Setup, Query


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setup = Setup()
        self.query = Query()
        self.setup.show()
        self.setup.ui.pushButtonQuery.clicked.connect(self.openQuery)

    def openQuery(self):
        self.query.ui.show()
        self.setup.close()


if __name__ == "__main__":
    app = QApplication()
    w = Main()
    sys.exit(app.exec_())
