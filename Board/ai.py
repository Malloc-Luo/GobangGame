# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
import sys


class AI(QObject):
    # 发送计算结果
    sendStepSignal = pyqtSignal(dict)
    # 黑棋 白棋 空点
    BLACK, WHITE, EMPTY = 1, -1, 0

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.map = None
        self.me = None

    def get_map(self, info: dict):
        # 这个是棋盘
        self.map = np.array(info['map'])
        # 这个是ai持有的棋子类型
        self.me = info['me']
        ##############################
        # 在这里进行处理
        ##############################

    def ret_result(self, pos: tuple):
        # 发送结果，在运行完后调用这个函数发送坐标
        self.sendStepSignal.emit({
            'step': pos,
            'me': self.me
        })
