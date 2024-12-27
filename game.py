#作者：王睿，学号：2024317120093, Date: 2024-12-20

import pygame
from game_items import *


class Game(object):

    def __init__(self):
        self.main_window = pygame.display.set_mode((640, 480)) #创建游戏主窗口
        pygame.display.set_caption("贪吃蛇") #设置窗口标题

        self.score_label = Label() #得分的标签(屏幕上显示的得分)
        self.score = 0

        self.tip_label = Label(24, False) #暂停\游戏结束的标签(暂停\游戏结束时屏幕上的提示文字)

        self.is_game_over = True #游戏是否结束的标志
        self.is_pause = False #游戏是否暂停的标志

        self.food = Food()

        self.snake = Snake()



    def start(self):
        """启动、控制游戏"""
        clock = pygame.time.Clock() #游戏时钟
        

        while True:

            #事件监听
            for event in pygame.event.get(): #遍历同一时刻发生的事件列表
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key ==pygame.K_SPACE:
                        if self.is_game_over:
                            self.reset_game()
                            print('游戏重新开始')
                        else:
                            self.is_pause = not self.is_pause
                if not self.is_pause and not self.is_game_over:
                    if event.type ==FOOD_UPDATE_EVENT:
                        #更新食物位置
                        self.food.random_rect()
                    elif event.type == SNAKE_UPDATE_EVENT:
                        #移动蛇的位置
                        self.is_game_over = not self.snake.update()
                    elif event.type == pygame.KEYDOWN:
                        #有键盘按键按下
                        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                            self.snake.change_dir(event.key)
                
            #依次绘制游戏背景元素
            self.main_window.fill(BACKGROUND_COLOR)

            #绘制得分
            self.score_label.draw(self.main_window, "Score: %d"%self.snake.score)

            #绘制暂停、游戏结束时显示的文字
            if self.is_game_over:
                self.tip_label.draw(self.main_window, "游戏结束，按空格键重新开始...")
            elif self.is_pause:
                self.tip_label.draw(self.main_window, "游戏暂停，按空格键继续...")
            else:
                if self.snake.has_eat(self.food):
                    self.food.random_rect()

            #绘制食物
            self.food.draw(self.main_window)


            #绘制贪吃蛇
            self.snake.draw(self.main_window)
            #更新显示
            pygame.display.update()

            clock.tick(60) #设置帧率上限

    def reset_game(self):
        #重置游戏参数
        self.score = 0
        self.is_game_over = False
        self.is_pause = False

        #重置蛇的数据
        self.snake.reset_snake()
        #重置食物的位置
        self.food.random_rect()



if __name__ == '__main__':
    #游戏开始时初始化pygame的模块
    pygame.init() #初始化所有模块
    Game().start() #游戏代码
    #游戏结束，释放pygame模块占用的资源
    pygame.quit() #取消初始化所有模块
