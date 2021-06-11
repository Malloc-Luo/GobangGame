# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
import sys


class AI(QObject):
    # 发送计算结果
    sendStepSignal = pyqtSignal(dict)
    # 黑棋 白棋 空点
    BLACK, WHITE, EMPTY = 1, -1, 0

    DEPTH = 3  # 搜索深度   只能是单数。  如果是负数， 评估函数评估的的是自己多少步之后的自己得分的最大值，并不意味着是最好的棋， 评估函数的问题
    list_my = []
    list_enemy = []
    chess_board = []  # 整个棋盘的点
    list_all  =[]
    next_point = [0, 0]  # AI下一步最应该下的位置
    COLUMN = 14
    ROW = 14
    blank_list = []

    shape_score = [(50, [0, 1, 1, 0, 0]),
               (50, [0, 0, 1, 1, 0]),
               (200, [1, 1, 0, 1, 0]),
               (500, [0, 0, 1, 1, 1]),
               (500, [1, 1, 1, 0, 0]),
               (5000, [0, 1, 1, 1, 0]),
               (5000, [0, 1, 0, 1, 1, 0]),
               (5000, [0, 1, 1, 0, 1, 0]),
               (5000, [1, 1, 1, 0, 1]),
               (5000, [1, 1, 0, 1, 1]),
               (5000, [1, 0, 1, 1, 1]),
               (5000, [1, 1, 1, 1, 0]),
               (5000, [0, 1, 1, 1, 1]),
               (50000, [0, 1, 1, 1, 1, 0]),
               (99999999, [1, 1, 1, 1, 1])]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.map = None
        self.me = None



    def reverse_list (self,list):
        newlist = []
        for element in list:
            test_pt = [element[1],element[0]]
            newlist.append(test_pt)
        return newlist

          
            
    def ifWin(self,Map):
        myChessMap = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
        for i in range(0,15):
            for j in range(0,15):
                myChessMap[i][j] = Map[i][j]


                
        for i in range(0,15):
            myChessMap[i].extend([5, 5, 5, 5, 5])
            myChessMap[i] = [5, 5, 5, 5, 5] + myChessMap[i]
        for i in range(0,5):
            a = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            myChessMap.append([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
            myChessMap.insert(0,[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])

            
        for i in range(5,20):
            for j in range(5,20):
                if(myChessMap[j][i] != 0):
                    if(myChessMap[j][i] == myChessMap[j][i + 1] and myChessMap[j][i] == myChessMap[j][i + 2] and myChessMap[j][i] == myChessMap[j][i + 3] and myChessMap[j][i] == myChessMap[j][i + 4]):
                        return myChessMap[j][i]
                    elif(myChessMap[j + 1][i] == myChessMap[j][i] and myChessMap[j][i] == myChessMap[j + 2][i] and myChessMap[j][i] == myChessMap[j + 3][i] and myChessMap[j + 4][i] == myChessMap[j][i]):
                        return myChessMap[j][i]
                    elif(myChessMap[j + 1][i + 1] == myChessMap[j][i] and myChessMap[j][i] == myChessMap[j + 2][i + 2] and myChessMap[j][i] == myChessMap[j + 3][i + 3] and myChessMap[j + 4][i + 4] == myChessMap[j][i]):
                        return myChessMap[j][i]
                    elif(myChessMap[j + 1][i - 1] == myChessMap[j][i] and myChessMap[j][i] == myChessMap[j + 2][i - 2] and myChessMap[j][i] == myChessMap[j + 3][i - 3] and myChessMap[j + 4][i - 4] == myChessMap[j][i]):
                        return myChessMap[j][i]                     
        return 0



    
    def Search(self,Map,color):
        myChessMap = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
        for i in range(0,15):
            for j in range(0,15):
                myChessMap[i][j] = Map[i][j]
        xyMark = [0,0,-99999999999999]

        for i in range(0,15):
            for j in range(0,15):
                if(myChessMap[i][j] == 0):
                    myChessMap[i][j] = color
                    a = AI.evaluae(self,myChessMap,color) - AI.evaluae(self,myChessMap,-color)
                    if(a > xyMark[2]):
                        xyMark[0] = i
                        xyMark[1] = j
                        xyMark[2] = a
                        print(a)
                    myChessMap[i][j] = 0
                        
        return xyMark
 
            
    def evaluae(self,Map,color):
        myChessMap = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
        for i in range(0,15):
            for j in range(0,15):
                myChessMap[i][j] = Map[i][j]
                
        if(color == -1):
            for i in range(0,15):
                for j in range(0,15):
                    myChessMap[i][j] = -myChessMap[i][j]
        chessBuffer = []
        mark = 0

        for i in range(0,15):
            myChessMap[i].extend([5, 5, 5, 5, 5])
            myChessMap[i] = [5, 5, 5, 5, 5] + myChessMap[i]
        for i in range(0,5):
            a = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            myChessMap.append([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
            myChessMap.insert(0,[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])



        for i in range(5,20):
            for j in range(5,20):
                chessBuffer.append([myChessMap[i][j + 0], myChessMap[i][j + 1], myChessMap[i][j + 2], myChessMap[i][j + 3], myChessMap[i][j + 4]])
                chessBuffer.append([myChessMap[i + 0][j], myChessMap[i + 1][j], myChessMap[i + 2][j], myChessMap[i + 3][j], myChessMap[i + 4][j]])
                chessBuffer.append([myChessMap[i + 0][j + 0], myChessMap[i + 1][j + 1], myChessMap[i + 2][j + 2], myChessMap[i + 3][j + 3], myChessMap[i + 4][j + 4]])
                chessBuffer.append([myChessMap[i - 0][j + 0], myChessMap[i - 1][j + 1], myChessMap[i - 2][j + 2], myChessMap[i - 3][j + 3], myChessMap[i - 4][j + 4]])
                for k in range(0,len(chessBuffer)):
                    for m in range(0,len(AI.shape_score)):
                        if(chessBuffer[k] == AI.shape_score[m][1]):
                            mark = mark + AI.shape_score[m][0]
                chessBuffer.clear()
        return mark
    


    def get_map(self, info: dict):
        # 这个是棋盘，在这里面进行计算
        self.map = np.array(info['map'])
        # 这个是ai持有的棋子类型
        self.me = info['me']
        ##############################
        # 在这里进行处理
        '''
        for i in range(AI.COLUMN+1):
            for j in range(AI.ROW+1):
                AI.chess_board.append((i, j))
        '''
        map = self.map.tolist()
        #AI.list_my = np.argwhere(self.map == 1)# == self.me
        #AI.list_enemy = np.argwhere(self.map == -1)
        #AI.list_all = AI.list_my+AI.list_enemy
        #AI.blank_list = np.argwhere(self.map == 0)

        '''
        AI.list_my = np.argwhere(self.map == 1).tolist()# == self.me
        AI.list_enemy = np.argwhere(self.map == -1).tolist()
        AI.list_all = AI.list_my+AI.list_enemy
        AI.blank_list = np.argwhere(self.map == 0).tolist()
        '''

        '''
        AI.list_my = AI.reverse_list (self,np.argwhere(self.map == 1).tolist())# == self.me
        AI.list_enemy = AI.reverse_list (self,np.argwhere(self.map == -1).tolist())
        AI.list_all = AI.list_my+AI.list_enemy
        AI.blank_list = AI.reverse_list (self,np.argwhere(self.map == 0).tolist())
        '''

        '''
        AI.list_my = np.swapaxes(np.argwhere(self.map == 1),0,1).tolist()
        AI.list_enemy = np.swapaxes(np.argwhere(self.map == -1),0,1).tolist()
        AI.list_all = AI.list_my+AI.list_enemy
        AI.blank_list = np.swapaxes(np.argwhere(self.map == 0),0,1).tolist()
        '''

        chessMap = [
            [0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]

       # AI.ai(self)
        #AI.ret_result(self,AI.next_point)
        xymark = AI.Search(self,map,1)
        AI.ifWin(self,map)
        print("mark is " , xymark)
        next_pos = [xymark[0],xymark[1]]
        AI.ret_result(self,next_pos)
        ##############################

    def ret_result(self, pos: tuple):
        # 发送结果，在运行完后调用这个函数发送坐标
        self.sendStepSignal.emit({
            'step': pos,
            'me': self.me
        })
