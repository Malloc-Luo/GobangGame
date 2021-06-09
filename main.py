# -*- coding: utf-8 -*-
from board import Board
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
import sys


class Main(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.board = Board()

    def start(self):
        self.board.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Main()
    m.start()
    sys.exit(app.exec_())
