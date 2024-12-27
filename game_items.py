#作者：王睿，学号：2024317120093, Date: 2024-12-20
import random
import pygame

#全局变量
SCREEN_RECT = pygame.Rect(0, 0, 640, 480) #游戏窗口矩形大小
CELL_SIZE = 20 #单元格宽高
BACKGROUND_COLOR = (136, 175, 215) #主窗口背景颜色
SCORE_TEXT_COLOR = (192, 192, 192) #分数文字颜色
TIP_TEXT_COLOR = (0, 0, 0) #提示文字颜色
FOOD_UPDATE_EVENT = pygame.USEREVENT #更新食物事件
SNAKE_UPDATE_EVENT = pygame.USEREVENT + 1 #更新食物事件

class Label(object):
    """文字标签类"""
    def __init__(self, size=48, is_score=True):
        """初始化标签信息
        :param size 文本的大小
        :param is_score 是否显示得分的对象"""
        self.font = pygame.font.SysFont('simhei', size) #设置黑体字
        self.is_score = is_score
    def draw(self, window, text):
        """绘制当前对象的内容"""
        #使用字体渲染文本内容
        color = SCORE_TEXT_COLOR if self.is_score else TIP_TEXT_COLOR
        text_surface = self.font.render(text, True, color)
        #获取文本的矩形信息
        text_rect = text_surface.get_rect()
        #获取窗口的矩形信息
        window_rect = window.get_rect()
        #修改文本的显示位置
        if self.is_score:
            #游戏得分
            text_rect.bottomleft = window_rect.bottomleft
        else:
            #提示信息(暂停、游戏结束)
            text_rect.center = window_rect.center
        #在游戏窗口中绘制渲染结果
        window.blit(text_surface, text_rect)

class Food(object):
    "食物类"
    def __init__(self):
        "初始化食物"
        self.color = (255, 0, 0)
        self.score = 10 #吃到一个食物得10分
        self.rect = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE) #初始的显示位置
        self.random_rect() #设置食物随机位置
    def random_rect(self):
        col = SCREEN_RECT.w / CELL_SIZE - 1 #窗口中单元格的列数
        row = SCREEN_RECT.h / CELL_SIZE - 1 #窗口中单元格的行数
        x = random.randint(0, col) * CELL_SIZE
        y = random.randint(0, row) * CELL_SIZE
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        #食物初始不可见
        self.rect.inflate_ip(-CELL_SIZE, -CELL_SIZE)
        #设置定时，时间到了以后更新食物的位置
        pygame.time.set_timer(FOOD_UPDATE_EVENT, 30000)
    def draw(self, window):
        #判断宽度是否到达单元格大小
        if self.rect.w < CELL_SIZE:
            self.rect.inflate_ip(2, 2) #向四周各放大一个元素
        "在当前食物的矩形内，绘制实心圆"
        pygame.draw.ellipse(window, self.color, self.rect)

class Snake(object):
    """蛇类"""
    def __init__(self):
        """初始化蛇的数据"""
        self.dir = pygame.K_RIGHT #运动方向
        self.time_interval = 500 #运动时间间隔 500
        self.score = 0 #游戏得分
        self.color = (64, 64, 64) #身体颜色,深灰色
        self.body_list = [] #身体列表
        self.reset_snake()
    def reset_snake(self):
        """重置蛇的数据"""
        self.dir = pygame.K_RIGHT
        self.time_interval = 500
        self.score = 0
        self.body_list.clear()
        for _ in range(3):
            self.add_node()
    def add_node(self):
        """添加一节身体"""
        if self.body_list:
            #已经有身体了
            head = self.body_list[0].copy()
        else:
            #还没有身体
            head = pygame.Rect(-CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)
        #根据移动方向，把新生成的头部放到恰当的位置
        if self.dir == pygame.K_RIGHT:
            head.x += CELL_SIZE
        elif self.dir == pygame.K_LEFT:
            head.x -= CELL_SIZE
        elif self.dir == pygame.K_UP:
            head.y -= CELL_SIZE
        elif self.dir == pygame.K_DOWN:
            head.y += CELL_SIZE
        #把新生成的头部放到列表的最前面
        self.body_list.insert(0, head)
        #定时更新身体
        pygame.time.set_timer(SNAKE_UPDATE_EVENT, self.time_interval)
    def draw(self, window):
        #遍历绘制每一节身体
        for idx, rect in enumerate(self.body_list):
            pygame.draw.rect(window,
                        self.color,
                        rect.inflate(-2, -2), #缩小矩形区域
                        idx == 0) #蛇头绘制边框不填充
    def update(self):
        """移动蛇的身体"""
        #备份移动之前的身体列表
        body_list_copy = self.body_list.copy()
        self.add_node()
        self.body_list.pop()
        #判断是否死亡
        if self.is_dead():
            self.body_list = body_list_copy
            return False
        return True
    def change_dir(self, to_dir):
        """改变贪吃蛇的运动方向
        :param to_dir : 要变化的方向"""
        hor_dirs = (pygame.K_RIGHT, pygame.K_LEFT) #水平方向
        ver_dirs = (pygame.K_UP, pygame.K_DOWN) #垂直方向
        #判断当前运动方向以及要修改的方向
        if ((self.dir in hor_dirs and to_dir not in hor_dirs) or 
            (self.dir in ver_dirs and to_dir not in ver_dirs)):
            self.dir = to_dir
    def has_eat(self, food):
        """判断蛇头是否与食物相遇 -吃到食物
        :param food :食物对象
        :return :是否吃到食物"""
        if self.body_list[0].contains(food.rect):
            self.score += food.score
            #修改运动时间间隔
            if self.time_interval > 100:
                self.time_interval -= 50
            self.add_node() #增加一节身体
            return True
        return False
    def is_dead(self):
        """判断是否已经死亡，如果死亡则返回True"""
        #获取蛇头的矩形
        head = self.body_list[0]
        #判断蛇头是否在窗口里
        if not SCREEN_RECT.contains(head):
            return True
        #判断蛇头是否与身体重叠
        for body in self.body_list[1:]:
            if head.contains(body):
                return True
        return False