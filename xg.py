# coding:utf-8

import os
import random
import time
import pygame
import easygui
import sys
from pygame.locals import *

# 加载图片
bg = pygame.image.load("images/bg3.png")
bg2 = pygame.image.load("images/bg2.png")
bg3 = pygame.image.load("images/bg3.jpg")
wanja = pygame.image.load("images/wanja.png")
xinguan = pygame.image.load("images/xinguan.png")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 50)
pygame.init()
canvas = pygame.display.set_mode((480, 650))
pygame.display.set_caption("大战新冠")


def handleEvent():
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()


# 写文字方法
def fillText(text, position):
    TextFont = pygame.font.Font('images/font4.ttf', 25)
    newText = TextFont.render(text, True, (0, 0, 0))
    canvas.blit(newText, position)


def fillText2(text, position):
    TextFont = pygame.font.Font('images/WRYH.ttf', 50)
    newText = TextFont.render(text, True, (255, 240, 10))
    canvas.blit(newText, position)


def fillText3(text, position):
    TextFont = pygame.font.Font('images/WRYH.ttf', 50)
    newText = TextFont.render(text, True, (255, 10, 10))
    canvas.blit(newText, position)


# 声明变量life表示红心的生命值
life = 10
# 创建黑心变量
mouseX = 200
mouseY = 200
xingaunWidth = 20
xingaunHeight = 20
xingaunspeed = 210

# 创建病毒列表
arrXinguan = []


def createXinguan(XinguanNum):
    for i in range(0, XinguanNum):
        randPos = random.randint(0, 3)
        randX = random.random() * (480 - xingaunWidth)
        randY = random.random() * (480 - xingaunHeight)
        speed = random.random() * 200 + xingaunspeed
        if randPos == 0:
            arrXinguan.append(Xinguan(randX, 0, xinguan, xingaunWidth, xingaunHeight, mouseX, mouseY, speed))
        elif randPos == 1:
            arrXinguan.append(Xinguan(462, randY, xinguan, xingaunWidth, xingaunHeight, mouseX, mouseY, speed))
        elif randPos == 2:
            arrXinguan.append(Xinguan(randX, 632, xinguan, xingaunWidth, xingaunHeight, mouseX, mouseY, speed))
        elif randPos == 3:
            arrXinguan.append(Xinguan(0, randY, xinguan, xingaunWidth, xingaunHeight, mouseX, mouseY, speed))


# 创建病毒类
class Xinguan:
    global mouseX, mouseY

    def __init__(self, x, y, img, width, height, mouseX, mouseY, speed):
        self.x = x
        self.y = y
        self.img = img
        self.width = width
        self.height = height
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.speed = speed
        self.xs = (self.mouseX - self.x) / speed
        self.ys = (self.mouseY - self.y) / speed


# 创建玩家类
class Wanja(Xinguan):
    global mouseX, mouseY

    def __init__(self, x, y, img, width, height, mouseX, mouseY, speed, life):
        Xinguan.__init__(self, x, y, img, width, height, mouseX, mouseY, speed)
        self.life = life


# 创建玩家对象
Wanja = Wanja(mouseX, mouseY, wanja, 45, 25, 0, 0, 1, life)

# 创建生成病毒对象方法
XinguanNum = 0


def born():
    global XinguanNum
    if len(arrXinguan) <= 0:
        XinguanNum = XinguanNum + 1
        createXinguan(XinguanNum)


# 创建画图片方法
def drawAll():
    canvas.blit(bg, (0, 0))
    # 绘制病毒
    for arrB in arrXinguan:
        canvas.blit(arrB.img, (arrB.x, arrB.y))
    # 绘制玩家图片
    canvas.blit(Wanja.img, (Wanja.x, Wanja.y))


# 创建移动方法
def moveAll():
    global mouseX, mouseY
    for arrB in arrXinguan:
        arrB.x = arrB.xs + arrB.x
        arrB.y = arrB.ys + arrB.y
    # 设置玩家跟随鼠标移动
    mouseX, mouseY = pygame.mouse.get_pos()
    Wanja.x = mouseX - Wanja.width / 2
    Wanja.y = mouseY - Wanja.height / 2


# 创建越界检测方法
def outSide():
    for arrB in arrXinguan:
        if arrB.x + arrB.width < 0 or arrB.x > 480 or arrB.y + arrB.height < 0 or arrB.y > 650:
            arrXinguan.remove(arrB)
        break


# 创建碰撞检测方法
def collision():
    global s, xingaunspeed, life
    for arrB in arrXinguan:
        if arrB.x + arrB.width > Wanja.x and arrB.x < Wanja.x + Wanja.width:
            if arrB.y + arrB.height > Wanja.y and arrB.y < Wanja.y + Wanja.height:
                # 碰撞后操作
                arrXinguan.remove(arrB)
                life = life - 1  # 扣除生命
                time.sleep(0.1)


# 创建游戏开关方法
# s = easygui.boolbox('确定开始'
# -------------------------------------------------------
s = True
if not s:
    pygame.quit()
    sys.exit()


def switch():
    global s
    if s:
        # 调用画图片方法
        drawAll()
        # 调用生成黑心的方法
        born()
        # 调用移动方法
        moveAll()
        # 调用outSide方法
        outSide()
        # 调用碰撞检测方法
        collision()


# 开始计时
start = int(time.time())
intervalTime = 0
counttime = 10  # 结束倒计时秒数

while True:
    # 调用游戏开关方法
    switch()

    if life <= 0:  # 死亡后操作
        s = False  # 结束游戏

    if s:  # 运行时
        end = int(time.time())
        intervalTime = end + 1 - start
        fillText('你坚持了:' + str(intervalTime) + '天', (40, 20))
        fillText('机会' + str(life), (400, 20))
        if intervalTime >= 30:  # 结束时
            s = False

    if not s:  # 结束后
        if intervalTime >= 15:  # 胜利
            canvas.blit(bg3, (0, 0))
            fillText2('大获全胜！', (30, 120))
            pt = '你坚持了：' + str(intervalTime) + '天'
            fillText(pt, (40, 180))
            # 结束倒计时
            end = int(time.time())
            lasttime = start + intervalTime - end - 1 + counttime
            fillText2(str(lasttime), (225, 400))
            if lasttime <= 0:
                break

        else:  # 失败
            end = int(time.time())
            canvas.blit(bg2, (0, 0))
            fillText3('失败', (30, 120))
            pt = '你坚持了：' + str(intervalTime) + '天'
            fillText(pt, (40, 180))
            # 结束倒计时
            lasttime = start + intervalTime - end - 1 + counttime
            fillText3(str(lasttime), (225, 400))
            if lasttime <= 0:
                life = 10
                start = int(time.time())
                intervalTime = 0
                XinguanNum = 0
                del arrXinguan[start: end]
                s = True
    # 更新屏幕内容
    pygame.display.update()
    # 处理关闭游戏
    handleEvent()
    time.sleep(0.002)
