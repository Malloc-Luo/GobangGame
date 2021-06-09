# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPixmap, QFont
from PyQt5.QtCore import Qt, QEvent, QObject, QPoint, pyqtSignal
from Ui_board import Ui_Form
from pprint import pprint
import sys
import json


class Board(QWidget):
    # 定位点
    xbegin, ybegin, xend, yend, step = 30, 30, 871, 871, 60
    # 棋子编号
    BLACK, WHITE, EMPTY = 1, -1, 0
    # paintState状态
    START, GAME = 'START', 'GAME'
    # 发送给算法端
    sendmapSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('五子棋')
        self.set_pen()
        self.ui.map.installEventFilter(self)
        self.piece = self.BLACK
        self.piecePos = None
        self.paintState = self.START
        # 绘图缓冲区
        self.pix = QPixmap(1200, 1000)
        self.pix.fill(QColor(255, 255, 191))
        self.ui.rbt_black.toggled.connect(lambda: self.choose_piece(self.BLACK))
        self.ui.rbt_white.toggled.connect(lambda: self.choose_piece(self.WHITE))
        self.ui.pbt_start.clicked.connect(self.start_game)
        self.map = [[self.EMPTY] * 15 for _ in range(15)]
        self.isRunning = False
        self.tag = ''

    def transfer_json(self):
        return json.dumps({'map': self.map, 'me': self.piece})

    def set_pen(self):
        # 画线用的
        self.linePen = QPen()
        self.linePen.setColor(Qt.gray)
        self.linePen.setWidth(3)
        # 画点用的
        self.pointPen = QPen()
        self.pointPen.setColor(Qt.gray)
        self.pointPen.setWidth(15)

    def draw_map(self, size=15):
        self.painter = QPainter(self.pix)
        self.painter.setPen(self.linePen)
        self.painter.setFont(QFont('Microsoft YaHei UI', 12))
        for x in range(self.xbegin, self.xend, self.step):
            self.painter.drawLine(x, self.ybegin, x, self.yend)
            self.painter.drawLine(self.ybegin, x, self.yend, x)
            self.painter.drawText(QPoint(self.xend + 25, x), str(15 - int(x / 60)))
            self.painter.drawText(QPoint(x, self.xend + 38), chr(int(x / 60) + ord('A')))
        self.painter.end()

    def draw_point(self, x, y):
        self.painter = QPainter(self.pix)
        self.painter.setPen(self.pointPen)
        _x, _y = self.xbegin + x * self.step, self.ybegin + self.step * y
        self.painter.drawPoint(QPoint(_x, _y))
        self.painter.end()

    def draw_piece(self, pos, col):
        x, y = pos[0], pos[1]
        _x, _y = self.xbegin + x * self.step, self.ybegin + self.step * y
        self.painter = QPainter(self.pix)
        color = Qt.black if col == self.BLACK else Qt.white
        self.painter.setPen(QColor(Qt.black))
        self.painter.setBrush(QBrush(color))
        self.painter.drawEllipse(_x - 20, _y - 20, 40, 40)
        self.painter.end()

    def eventFilter(self, obj, event) -> bool:
        if obj == self.ui.map and event.type() == QEvent.Paint:
            if self.paintState == self.START:
                self.draw_map()
                self.draw_point(3, 3)
                self.draw_point(3, 11)
                self.draw_point(11, 3)
                self.draw_point(11, 11)
                self.draw_point(7, 7)
                self.paintState = self.GAME
            elif self.paintState == self.GAME:
                self.draw_piece(self.piecePos, self.piece)
            painter = QPainter(self.ui.map)
            painter.drawPixmap(0, 0, self.pix)
        return QObject.eventFilter(self, obj, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if (event.pos().x() <= self.xend + 10) and (event.pos().y() <= self.yend + 10):
                x, y = event.pos().x() - self.xbegin, event.pos().y() - self.ybegin
                if x % 60 <= 10 and int(x / 60) < 15:
                    x = int(x / 60)
                elif x % 60 >= 50 and int(x / 60) < 15:
                    x = int(x / 60) + 1
                else:
                    return None
                if y % 60 <= 10 and int(y / 60) < 15:
                    y = int(y / 60)
                elif y % 60 >= 50 and int(y / 60) < 15:
                    y = int(y / 60) + 1
                else:
                    return None
                if self.map[y][x] == self.EMPTY:
                    self.map[y][x] = self.piece
                    self.piecePos = [x, y]
                    self.tag = chr(x + ord('A')) + str(15 - y)
                    self.ui.tb_logs.append(str('黑棋' if self.piece == self.BLACK else '白棋') + ': ' + self.tag)
                    self.sendmapSignal.emit(self.transfer_json())
                    self.update()

    def choose_piece(self, piece):
        self.piece = piece

    def start_game(self):
        ...


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Board()
    w.show()
    sys.exit(app.exec_())
