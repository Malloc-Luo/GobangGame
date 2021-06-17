# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPixmap, QFont
from PyQt5.QtCore import Qt, QEvent, QObject, QPoint, pyqtSignal, QTimer
from resource.Ui_board import Ui_Form
import sys
import json
from time import sleep, time


class Board(QWidget):
    # 定位点
    xbegin, ybegin, xend, yend, step = 30, 30, 871, 871, 60
    # 棋子编号
    BLACK, WHITE, EMPTY = 1, -1, 0
    # paintState状态
    START, GAME, FIRST = 'START', 'GAME', 'FIRST'
    # 发送给算法端
    sendmapSignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('五子棋')
        self.ui.lcd_timer.display('00:00:00')
        self.set_pen()
        self.ui.map.installEventFilter(self)
        self.piece = self.BLACK
        self.piecePos = None
        self.paintState = self.START
        # 绘图缓冲区
        self.pix = QPixmap(930, 930)
        self.pix.fill(QColor(255, 255, 191))
        self.ui.rbt_black.toggled.connect(lambda: self.choose_piece(self.BLACK))
        self.ui.rbt_white.toggled.connect(lambda: self.choose_piece(self.WHITE))
        self.ui.pbt_swap.clicked.connect(self.thrid_swap)
        self.ui.pbt_start.clicked.connect(self.start_game)
        self.ui.pbt_save.clicked.connect(self.save_map)
        self.map = [[self.EMPTY] * 15 for _ in range(15)]
        self.isRunning = False
        self.tag = ''
        # 步骤列表，所有点放在这里面
        self.steps = []
        # Ai模块是否正在运行，如果是则不能落子
        self.isAiRunning = False
        # 定时器，刷新计时
        self.timer = QTimer(self)
        self.timeCnt = 0
        self.timer.timeout.connect(self.refresh_lcd_display)
        self.timer.start(10)
        self.timer.stop()

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
        self.map[y][x] = col
        self.tag = chr(x + ord('A')) + str(15 - y)
        self.ui.tb_logs.append(str('黑棋' if col == self.BLACK else '白棋') + ': ' + self.tag)

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
            elif self.paintState == self.FIRST:
                self.first_game()
                self.paintState = self.GAME
            elif self.paintState == self.GAME:
                while len(self.steps) != 0:
                    pos = self.steps.pop(0)
                    self.draw_piece(pos['step'], pos['me'])
            painter = QPainter(self.ui.map)
            painter.drawPixmap(0, 0, self.pix)
        return QObject.eventFilter(self, obj, event)

    def first_game(self):
        '''先手下'''
        self.draw_piece((7, 7), self.BLACK)
        # self.draw_piece((7, 8), self.WHITE)
        # self.draw_piece((8, 7), self.BLACK)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and (self.isAiRunning is False):
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
                    self.map[y][x] = -self.piece
                    self.piecePos = [x, y]
                    self.steps.append({'step': self.piecePos, 'me': -self.piece})
                    self.update()
                    self.sendmapSignal.emit({
                        'map': self.map,
                        'me': self.piece
                    })
                    self.isAiRunning = True
                    self.timer.start()

    def choose_piece(self, piece):
        self.piece = piece

    def start_game(self):
        self.paintState = self.FIRST
        self.update()
        self.ui.pbt_start.setDisabled(True)

    def get_result(self, res: dict):
        self.isAiRunning = False
        self.timer.stop()
        self.steps.append(res)
        self.update()
        if ("winner" in res.keys()) and (res['winner'] is not None):
            piece = '黑棋' if res['winner'] == self.BLACK else '白棋'
            QMessageBox.information(None, "游戏结束", "{}方获胜".format(piece), QMessageBox.Ok)
            print("%s获胜" % piece)

    def thrid_swap(self):
        self.piece = -self.piece
        if self.ui.rbt_white.isChecked():
            self.ui.rbt_black.setChecked(True)
        else:
            self.ui.rbt_white.setChecked(True)
        self.ui.tb_logs.append('三手交换')
        self.ui.pbt_swap.setDisabled(True)

    def save_map(self):
        with open(str(int(time())) + '.json', 'w', encoding='utf-8') as f:
            json.dump({
                'map': self.map,
                'me': self.piece
            }, f, indent=4)

    def refresh_lcd_display(self):
        self.timeCnt += 1
        minute, sec, msec = int(self.timeCnt / 6000), int(self.timeCnt / 100) % 60, self.timeCnt % 100
        self.ui.lcd_timer.display('%02d:%02d:%02d' % (minute, sec, msec))
        self.timer.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Board()
    w.show()
    sys.exit(app.exec_())
