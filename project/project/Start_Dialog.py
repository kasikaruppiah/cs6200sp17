import sys

from PyQt4 import QtCore
from PyQt4.QtGui import (QApplication, QDesktopWidget, QDialog, QFont,
                         QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPalette,
                         QPushButton, QVBoxLayout, QWidget)

import generate_snippet


class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        mainLayout = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedSize(700, 25)
        self.lineEdit.setPlaceholderText("Enter Query")
        self.button = QPushButton("Search", self.cw)
        self.button.setFixedSize(75, 25)
        mainLayout.addWidget(self.lineEdit)
        mainLayout.addWidget(self.button)
        mainLayout.setContentsMargins(100, 0, 100, 0)
        self.cw.setLayout(mainLayout)
        self.cw.setFixedSize(1000, 750)
        self.setWindowTitle("BM25 Search Engine")
        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.Search)
        self.connect(self.lineEdit,
                     QtCore.SIGNAL("returnPressed()"), self.Search)

    def Search(self):
        query = self.lineEdit.text()
        self.close()
        generate_snippet.generate_snippet_html({'QUERY_STRING': str(query)})


class ResultWidget(QDialog):
    def __init__(self, query, results):
        QDialog.__init__(self)

        searchWidget = QWidget()
        self.lineEdit = QLineEdit(query)
        self.lineEdit.setFixedSize(700, 25)
        self.button = QPushButton("Search")
        self.button.setFixedSize(75, 25)
        label = QLabel()
        label.setFixedSize(700, 500)
        label.setTextFormat(QtCore.Qt.RichText)
        label.setText(results)

        searchLayout = QHBoxLayout(searchWidget)
        searchLayout.setSpacing(20)
        searchLayout.setContentsMargins(0, 75, 50, 0)
        searchLayout.addWidget(self.lineEdit)
        searchLayout.addWidget(self.button)
        searchWidget.setLayout(searchLayout)

        self.setWindowTitle(query + " - bm25-ranking")
        self.setFixedSize(1000, 750)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(100, 0, 50, 500)

        mainLayout.addWidget(searchWidget)
        mainLayout.addWidget(label)
        self.setLayout(mainLayout)
        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.Search)
        self.connect(self.lineEdit,
                     QtCore.SIGNAL("returnPressed()"), self.Search)

        self.show()

    def Search(self):
        query = self.lineEdit.text()
        self.close()
        generate_snippet.generate_snippet_html({'QUERY_STRING': str(query)})


class App(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.main = MainWindow()
        self.main.show()
        resolution = QDesktopWidget().screenGeometry()
        self.main.move(
            (resolution.width() / 2) - (self.main.frameSize().width() / 2),
            (resolution.height() / 2) - (self.main.frameSize().height() / 2))


def DisplayResult(query, result):
    dialog = ResultWidget(query, result)
    dialog.exec_()


def main(args, _str):
    global app
    app = App(args)
    app.exec_()


if __name__ == "__main__":
    main(sys.argv, "abc")
