import sys
from PySide2.QtCore import QStringListModel
from PySide2.QtWidgets import QListView, QApplication

app = QApplication()
model = QStringListModel()
model.setStringList(["0", "1", "2", "3"])
listview = QListView()
listview.setModel(model)
listview.show()
print(listview.selectionMode())
print(listview.selectionBehavior())
index = model.index(1, 0)
listview.setCurrentIndex(index)
sys.exit(app.exec_())
