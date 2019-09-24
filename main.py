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
        self.query.ui.timer.start(1000)
        self.query.ui.elapsed_time.start()
        self.query.ui.show()
        print(f'open query:{self.query.ui.getDateTime()}')
        self.setup.close()


if __name__ == "__main__":
    app = QApplication()
    w = Main()
    sys.exit(app.exec_())
