import random
import numpy as np
import keyboard as kb
import time
import threading

FIELD_HEIGHT = 7
FIELD_WIDTH = 5


class Tetris(object):
    def __init__(self, FIELD_HEIGHT, FIELD_WIDTH):
        self.FIELD = np.zeros((FIELD_HEIGHT+3, FIELD_WIDTH+6))
        self.FIELD_BASE = np.zeros((FIELD_HEIGHT+3, FIELD_WIDTH+6))
        self.FIELD_BASE[:, 0:3] = 1
        self.FIELD_BASE[:, FIELD_WIDTH+3:FIELD_WIDTH+6] = 1
        self.FIELD_BASE[FIELD_HEIGHT:FIELD_HEIGHT+3] = 1
        self.FIELD = np.copy(self.FIELD_BASE)
        self.pt = [0, 5]
        self.nextpt = [0, 5]
        self.nowmino = np.zeros((3, 3))

    def init_mino(self):
        self.minolist = np.zeros((1, 3, 3))
        # 縦2ミノ
        self.minolist[0, 0:2, 1] = 1

    def gen_mino(self):
        self.nowmino = self.minolist[0]
        self.pt = [0, 5]
        self.update()

    def keymove(self):
        while True:
            if kb.read_key() == "left":
                self.nextpt[0] = self.pt[0]
                self.nextpt[1] = self.pt[1]-1
                if self.detectCollision():
                    self.pt[1] -= 1
                    self.update()
                    time.sleep(0.2)
            if kb.read_key() == "right":
                self.nextpt[0] = self.pt[0]
                self.nextpt[1] = self.pt[1]+1
                if self.detectCollision():
                    self.pt[1] += 1
                    self.update()
                    time.sleep(0.2)

    def detectCollision(self):
        for i in range(3):
            for j in range(3):
                if self.FIELD_BASE[self.nextpt[0]+i][self.nextpt[1]-1+j] and self.nowmino[i][j] == 1:
                    return False
        return True

    def compDetect(self):
        sum = np.sum(self.FIELD_BASE, axis=1)
        for i in range(7):
            if sum[i] == 11:
                print("COMPLETE LINE!")
                for j in range(i, 0, -1):
                    self.FIELD_BASE[j,
                                    3:8] = np.copy(self.FIELD_BASE[j-1, 3:8])
                self.FIELD_BASE[0, 3:8] = 0

    def gameoverDetect(self):
        pass

    def fallmove(self):
        self.nextpt[0] = self.pt[0]+1
        self.nextpt[1] = self.pt[1]
        if self.detectCollision():
            self.pt[0] += 1
            self.update()
        else:
            self.tet_stab()

    def tet_stab(self):
        self.FIELD_BASE = np.copy(self.FIELD)
        self.compDetect()
        self.gen_mino()

    def update(self):
        self.FIELD = np.copy(self.FIELD_BASE)
        for i in range(3):
            for j in range(3):
                self.FIELD[self.pt[0]+i][self.pt[1]-1 +
                                         j] = np.copy(self.FIELD_BASE[self.pt[0]+i][self.pt[1]-1+j]+self.nowmino[i][j])

    def game(self):
        self.init_mino()
        self.gen_mino()
        thread1 = threading.Thread(target=self.keymove)
        thread1.start()
        thread2 = threading.Thread(target=self.display)
        thread2.start()
        while True:
            self.fallmove()

            time.sleep(1)

    def display(self):
        while True:
            print(self.FIELD)
            time.sleep(0.5)


def test():
    a = 0
    while True:
        a += 1
        print(a)
        time.sleep(2)


t = Tetris(FIELD_HEIGHT, FIELD_WIDTH)
t.game()
# thread1 = threading.Thread(target=test)
# thread2 = threading.Thread(target=t.display)
# thread1.start()
# thread2.start()
print(t.FIELD)
