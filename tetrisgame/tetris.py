import random
import numpy as np
import keyboard as kb
import time
import threading

FIELD_HEIGHT = 7
FIELD_WIDTH = 5


class Tetris(object):
    def __init__(self, FIELD_HEIGHT, FIELD_WIDTH):
        "ゲームの初期化"
        self.FIELD = np.zeros((FIELD_HEIGHT+3, FIELD_WIDTH+6))
        self.FIELD_BASE = np.zeros((FIELD_HEIGHT+3, FIELD_WIDTH+6))
        self.FIELD_BASE[:, 0:3] = 1
        self.FIELD_BASE[:, FIELD_WIDTH+3:FIELD_WIDTH+6] = 1
        self.FIELD_BASE[FIELD_HEIGHT:FIELD_HEIGHT+3] = 1
        self.FIELD = np.copy(self.FIELD_BASE)
        self.pt = [0, 5]
        self.nextpt = [0, 5]
        self.nowmino = np.zeros((3, 3))
        self.nextmino = np.zeros((3, 3))

    def init_mino(self):
        "ミノの一覧の作成"
        self.minolist = np.zeros((1, 3, 3))
        # 縦2ミノ
        self.minolist[0, 0:2, 1] = 1

    def gen_mino(self):
        "ミノの生成"
        self.nowmino = self.minolist[0]
        self.pt = [0, 5]
        self.update()

    def keymove(self):
        "キーによる横移動"
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

    def rotate(self):
        "キーによる回転移動"
        pass

    def detectCollision(self):
        "平行移動の衝突検出"
        for i in range(3):
            for j in range(3):
                if self.FIELD_BASE[self.nextpt[0]+i][self.nextpt[1]-1+j] and self.nowmino[i][j] == 1:
                    return False
        return True

    def detectStuck(self):
        "回転，ブロック生成時の埋没検知"
        pass

    def compDetect(self):
        "行消去の検出，実行"
        sum = np.sum(self.FIELD_BASE, axis=1)
        for i in range(7):
            if sum[i] == 11:
                print("COMPLETE LINE!")
                for j in range(i, 0, -1):
                    self.FIELD_BASE[j,
                                    3:8] = np.copy(self.FIELD_BASE[j-1, 3:8])
                self.FIELD_BASE[0, 3:8] = 0

    def gameoverDetect(self):
        "ゲームオーバーの検出"
        pass

    def fallmove(self):
        "ミノ落下"
        self.nextpt[0] = self.pt[0]+1
        self.nextpt[1] = self.pt[1]
        if self.detectCollision():
            self.pt[0] += 1
            self.update()
        else:
            self.tet_stab()

    def tet_stab(self):
        "地面に触れたミノ固定"
        self.FIELD_BASE = np.copy(self.FIELD)
        self.compDetect()
        self.gen_mino()

    def update(self):
        "表示するFIELDの更新"
        self.FIELD = np.copy(self.FIELD_BASE)
        for i in range(3):
            for j in range(3):
                self.FIELD[self.pt[0]+i][self.pt[1]-1 +
                                         j] = np.copy(self.FIELD_BASE[self.pt[0]+i][self.pt[1]-1+j]+self.nowmino[i][j])

    def game(self):
        "ゲーム実行部"
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
        "FIELDの表示"
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
