import numpy
import threading
import time
import os
import random
import keyboard
import sys
#引入各种库
"""
numpy：科学计算库，用于处理各种张量、矩阵、多维数组（比如矩阵的转置、卷积）
threading：python自带的线程库
time：python自带的调用系统时间或延迟一类时间相关的库
os：从名字os可以看出来是operate system“操作系统”的缩写，就是调用操作系统的接口
random：字面意思，用一些算法生成随机的数字or字符串
keyboard：字面意思，获取键盘事件（钩子）的库
sys：也是system的前三个字母，差不多就是调用系统、启动传入的参数之类的作用
"""


# 8*18宽高比 这是文字的宽高比

accuracy = 500 # 可以理解为场景大小，详见下面宽高的计算
fps = 10# 刷新率
# 设计要将命令行窗口调整为正方形舒适
hight = int(1/8*accuracy)# 计算高几个字符
width = int(1/18*accuracy)# 计算宽几个字符
display_data = numpy.zeros([width,hight],float)# 使用numpy库生成一个矩阵
# 用于代表每一个字符的状态数据

snake_cor = [[int(width/2),int(hight/2)]]# 设置蛇头和蛇身的(字符)初始坐标位置
#初始化为中心位置(宽高除2就是)
print(snake_cor) # 打印出来我们看到是一个python列表。前面一个就是宽后面就是高
# 因为是列表的坐标结构有顺序、有前后
# 只需要根据坐标顺序尾巴抽走和头部插入就可以实现移动蛇了

direction = 2 # 向前,逆时针到3
# 变量direction的作用是储存现在贪吃蛇前进的方向用的
"""
各数字代表的含义
0-地面:'-'
1-蛇:'@'
2-蛇头:'#'
3-豆子:'*'
"""



# 下面就是按键检测的事件函数，切换相应的方向

def w():# 前
    global direction
    if direction != 0:# 防止回头
        direction = 2

def s():# 后
    global direction
    if direction != 2:
        direction = 0

def a():# 左
    global direction
    if direction != 1:
        direction = 3

def d():# 右
    global direction
    if direction != 3:
        direction = 1


def ran_pules():# 随机生成豆子
    x = random.randint(0, hight-1)
    y = random.randint(0, width-1)
    if display_data[y][x] != 0:
        ran_pules()
    else:
        return [x, y]

def is_detected():# 用于检测场景中是否存在豆子
    for x in range(display_data.shape[0]):
        for y in range(display_data.shape[1]):
            if display_data[x][y] == 3:
                return True
    return False

def pulse():# 整个豆子的生成机制
    if is_detected() == False:
        return ran_pules()# 返回豆子坐标
    else:
        return None

def game_over(str):# 游戏结束时调用这个函数显示结束提示
    os.system('cls')
    print(str)
    input("游戏结束，请回车...\n")
    sys.exit(0)


def refresh(fps):# 刷新（渲染）界面
    while True:
        Render_temp = ''
        # 检测任何一个蛇的坐标是否超出 宽/高
        if snake_cor[-1][0] >= width or snake_cor[-1][1] >= hight or snake_cor[-1][0] <= 0 or snake_cor[-1][1] <= 0:
            game_over("超出游戏界面")# 如果是的游戏结束

        # add()
        # 随机豆子
        pulse_cor = None
        pulse_cor = pulse()# 接下豆子机制函数返回的豆子坐标
        if pulse_cor != None:# 如果豆子坐标不为空则在实际界面数据替换数据为豆子
            display_data[pulse_cor[1]][pulse_cor[0]] = 3

        for x in range(display_data.shape[0]):
            for y in range(display_data.shape[1]):
                if display_data[x,y] == 1 or display_data[x,y] == 2:
                    display_data[x,y] = 0 # 先清除蛇身的数据（刷新所需）



        """

        把每一个界面显示数据渲染成字符【重点】
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        """

        for x in range(display_data.shape[0]):# 遍历列数
            #Render_temp变量就是实际要输出到控制台的渲染出来的临时字符串
            Render_temp += '\n'# 添加换行符(换行的表示方法在python里就是转义符“\n”)
            for y in range(display_data.shape[1]):# 遍历行数
                for i in range(int(len(snake_cor))):# 【检测是否吃到了豆子或者是吃到了自己】
                    if display_data[snake_cor[i][0],snake_cor[i][1]] == 3:# 判断如果蛇头碰到豆子加长蛇身
                        add() # 加长身体
                    if snake_cor.count(snake_cor[i]) > 1:# 如果一个位置重复有两个蛇的坐标点判定吃自己游戏结束
                        game_over("蛇头吃蛇身")# 游戏结束函数
                    display_data[snake_cor[i][0],snake_cor[i][1]] = 1# 落实设定显示数据中的蛇身坐标，1就是蛇身
                display_data[snake_cor[-1][0],snake_cor[-1][1]] = 2# 落实设定显示数据中的蛇【头】坐标，1就是蛇【头】


                #--------------------------------------------------------------------------------------------#
                Render_temp += num2char(display_data[x,y])   #++= [将数字代表的数据转换为字符！] =++          |
                #--------------------------------------------------------------------------------------------#


        sys.stdout.flush()# 刷新缓存(减少闪烁)
        os.system('mode ' + str(hight) + ',' + str(width+3))# 调整窗口大小
        print(Render_temp)# 打印(输出)字符串
        # print(snake_cor)
        time.sleep(1/fps)# 延时限制刷新（帧数）
        move()# 蛇（玩家角色）移动

def num2char(num):# 渲染函数
    if num == 0:
        return '-'# 无物品
    elif num == 1:
        return '@'# 蛇
    elif num == 2:
        return '#'# 蛇头
    elif num == 3:
        return '*'# 豆子

def move():# 按照方向属性让蛇爬动
    if direction == 0:# 每一个方向的检测
        snake_cor.append([snake_cor[len(snake_cor)-1][0]+1,snake_cor[len(snake_cor)-1][1]])# 向前("前"指对应方向)添加一个移动了的蛇身坐标
        snake_cor.remove(snake_cor[0])# 删除最后一个坐标实现移动
    elif direction == 1:# 以下同
        snake_cor.append([snake_cor[len(snake_cor)-1][0],snake_cor[len(snake_cor)-1][1]+1])
        snake_cor.remove(snake_cor[0])
    elif direction == 2:
        snake_cor.append([snake_cor[len(snake_cor)-1][0]-1,snake_cor[len(snake_cor)-1][1]])
        snake_cor.remove(snake_cor[0])
    elif direction == 3:
        snake_cor.append([snake_cor[len(snake_cor)-1][0],snake_cor[len(snake_cor)-1][1]-1])
        snake_cor.remove(snake_cor[0])

def add():# 增加蛇身长度
    if direction == 2:# 每一个方向的检测
        snake_cor.insert(0, [snake_cor[0][0]+1,snake_cor[0][1]])
    elif direction == 3:
        snake_cor.insert(0, [snake_cor[0][0],snake_cor[0][1]+1])
    elif direction == 0:
        snake_cor.insert(0, [snake_cor[0][0]-1,snake_cor[0][1]])
    elif direction == 1:
        snake_cor.insert(0, [snake_cor[0][0],snake_cor[0][1]-1])

if __name__ == '__main__':# 如果该脚本不是作为模块加载
    for i in range(3):
        add()
    ref = threading.Thread(target=refresh,args=(fps,))# 单独建立一个线程提供刷新
    ref.start()# 启动刷新线程

    # 每一个按键的钩子绑定
    keyboard.add_hotkey('w',w)
    keyboard.add_hotkey('s',s)
    keyboard.add_hotkey('a',a)
    keyboard.add_hotkey('d',d)
        

# G:\水培社项目\python教学试点\宣传项目\复杂1_贪吃蛇.bat