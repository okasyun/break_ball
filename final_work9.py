

import pyxel
import random
import math


class Ball:
    game_over = 0

    def __init__(self):
        self.bx = 80
        self.by = 100
        self.bs = 1
        self.bc = 8
        self.sp = random.randint(2, 3)
        self.angle = math.radians(random.randint(70, 150))
        self.vx = math.cos(self.angle)
        self.vy = math.sin(self.angle)
        #self.game_over = 0
        self.start = 0
        self.num = 0

    def move(self, app):
        self.bx += self.vx * self.sp
        self.by += self.vy * self.sp
        if self.bx < 0 or self.bx > 180:
            self.score_flag = 0
       # 画面の左右に出た時
            self.vx = -self.vx  # 跳ね返す
        elif self.by < 0:
            # 画面の上に出た時
            self.vy = -self.vy
            # 跳ね返す
        elif self.by > 170:
            pyxel.play(0, 1)
            Ball.game_over = 1
           


class Pad:
    def __init__(self):
        self.px = 100
        self.py = 167
        self.pw = 30
        self.ph = 2
        self.pc = 14
        self.phit = 0

    def move(self):
        self.px = pyxel.mouse_x
        if (self.px+self.pw/2) > 180:
            self.px = 180 - self.pw/2
        elif (self.px-self.pw/2) < 0:
            self.px = self.pw/2

    def catch(self, ball):
        if self.phit == 0 and self.py <= ball.by and self.px-self.pw/2 <= ball.bx <= self.px+self.pw/2:
            ball.vy = -ball.vy
            pyxel.play(0, 0)
            self.phit = 1
            ball.bc = 6

        if ball.by < self.py - 2:
            self.phit = 0
            ball.bc = 8


class Block:
    def __init__(self, x, y):
        self.blw = 29
        self.blh = 5
        self.blc = 4
        # self.block = []
        self.judge_box = 1
        self.blx = x
        self.bly = y
        if x % 60 != 0 and y % 20 != 0:
            self.blc = 5
        elif (x % 40 == 0 and y % 30 == 0) or (x == 60 and y == 20):
            self.blc = 3
        elif (x == 90 and y == 40) or x == 150 and y == 20:
            self.blc = 6

    def judge_block_hit(self, ball, app):
        # for i in self.block:
        if ((self.blx < ball.bx) and (self.blx + self.blw > ball.bx) and (self.bly < ball.by) and (self.bly + self.blh+4 > ball.by) and self.judge_box == 1):
            self.judge_box = 0
            pyxel.play(0, 0)
            ball.vy = -ball.vy
            if self.blc == 4:
                app.score += 10
            elif self.blc == 5:
                app.score += 20

            elif self.blc == 6:
                app.score += 30
            else:
                app.score += 40


class Obstacle:
    def __init__(self):
        self.ox1 = 90
        self.oy1 = 120
        self.change = 0
        self.sp1 = 2
        self.ow1 = 32
        self.oh1 = 1
        self.oc1 = 12

        self.ox2 = 60
        self.oy2 = 140
        self.sp2 = 1
        self.ow2 = 40
        self.oh2 = 1
        self.oc2 = 8

    def move(self):
        if self.change == 0:
            self.ox1 += 1 * self.sp1
            if self.ox1 + self.ow1 >= 180:
                self.change = 1
        elif self.change == 1:
            self.ox1 -= 1 * self.sp1
            if self.ox1 <= 0:
                self.change = 0

        if self.change == 0:
            self.ox2 += 1 * self.sp2
            if self.ox2 + self.ow2 >= 180:
                self.change = 1
        elif self.change == 1:
            self.ox2 -= 1 * self.sp2
            if self.ox2 <= 0:
                self.change = 0

    def reflect(self, ball):
        if self.oy1 <= ball.by <= self.oy1+3 and self.ox1 <= ball.bx <= self.ox1+self.ow1:
            ball.vy = -ball.vy
            pyxel.play(0, 2)

        if self.oy2 <= ball.by <= self.oy2+3 and self.ox2 <= ball.bx <= self.ox2+self.ow2:
            ball.vy = -ball.vy
            pyxel.play(0, 2)


class App():

    def __init__(self):
        self.width = 180
        self.height = 170
        pyxel.init(self.width, self.height, caption="break_block_game")
        pyxel.sound(0).set(note='C3', tone='T',
                           volume='3', effect='F', speed=20)
        pyxel.sound(1).set(note='C4', tone='N',
                           volume='1', effect='N', speed=30)
        pyxel.sound(2).set(note='B1', tone='P',
                           volume='2', effect='F', speed=20)

        pyxel.sound(3).set(note='D3', tone='P',
                           volume='2', effect='F', speed=60)
        self.score = 0
        self.pad = Pad()
        self.obstacle = Obstacle()
        self.balls = [Ball()]
        self.blocks = []
        self.start = 0
        for a in range(0, 151, 30):
            for b in range(10, 81, 10):
                self.blocks.append(Block(a, b))
        pyxel.run(self.update, self.draw)

    def update(self):
        self.pad.move()
        self.obstacle.move()
        for b in self.balls:
            if Ball.game_over == 0:
                if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and self.start == 0:
                    pyxel.play(0, 3)
                    self.start = 1
                elif self.start == 1:
                    b.move(self)
                self.obstacle.reflect(b)
                self.pad.catch(b)
            for w in self.blocks:
                w.judge_block_hit(b, self)

        if self.score / 60 >= len(self.balls):
            self.balls.append(Ball())

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        for b in self.balls:
            if Ball.game_over == 0:
                if self.start == 0:
                    pyxel.text(70, 3, "MOUSE CLICK!!", pyxel.frame_count % 16)
                pyxel.circ(b.bx, b.by, b.bs, b.bc)
                pyxel.rect(self.pad.px-self.pad.pw/2, self.pad.py,
                           self.pad.pw, self.pad.ph, self.pad.pc)

                for w in self.blocks:
                    # self.blocks[w].blx, self.blocks[w].bly, self.blocks.blw, self.blocks.blh, self.blocks.blc
                    # for a in range(len(self.blocks.block)):
                    if w.judge_box == 1:
                        pyxel.rect(w.blx, w.bly, w.blw, w.blh, w.blc)
                pyxel.text(5, 3, 'score:'+str(self.score), 8)
                pyxel.rect(self.obstacle.ox1, self.obstacle.oy1,
                           self.obstacle.ow1, self.obstacle.oh1, self.obstacle.oc1)
                pyxel.rect(self.obstacle.ox2, self.obstacle.oy2,
                           self.obstacle.ow2, self.obstacle.oh2, self.obstacle.oc2)
            else:
                pyxel.text(70, 70, "GAME OVER", 7)
                pyxel.text(70, 80, "score:"+str(self.score), 8)
                


App()
