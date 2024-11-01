import random
import time
import threading
import keyboard  # 确保安装 keyboard 库
import os

total_shape=["↑↓←→","㊤㊦㊧㊨","▲▼◄►"]
shape_tank1=-1;
shape_tank2=-1;
# 基类Object
class Object:
    def __init__(self, posx, posy,):
        self.posx = posx
        self.posy = posy


# 子类Tank
class Tank(Object):
    def __init__(self, posx, posy):
        super().__init__(posx, posy)
        self.health = 3  # 初始血量
        self.direction = "up"  # 初始朝向

    def move(self, direction,obstacles,emeny_pos):
        if direction == "up":

            # 方向已经向上 开始移动
            if self.direction == "up" and (self.posx,self.posy-1) not in [(o.posx, o.posy) for o in obstacles] and  (self.posx,self.posy-1)!=emeny_pos: 
                self.posy = max(0, self.posy - 1)
            # 方向相反 不移动
            elif self.direction == "down": pass
            # 方向不向上 改变方向
            else: self.direction = "up"

        elif direction == "down":

            # 方向已经向下 开始移动
            if self.direction == "down" and (self.posx,self.posy+1) not in [(o.posx, o.posy) for o in obstacles] and (self.posx,self.posy+1)!=emeny_pos:
                self.posy = min(game.height - 1, self.posy + 1)
            # 方向相反 不移动
            elif self.direction == "up": pass
            # 方向不向下 改变方向
            else: self.direction = "down"

        elif direction == "left":

            # 方向已经向左 开始移动
            if self.direction == "left" and (self.posy,self.posx-1) not in [(o.posy, o.posx) for o in obstacles] and (self.posx-1,self.posy)!=emeny_pos: 
                self.posx = max(0, self.posx - 1)
            # 方向相反 不移动
            elif self.direction == "right": pass
            # 方向不向左 改变方向
            else: self.direction = "left"

        elif direction == "right":

            # 方向已经向左 开始移动
            if self.direction == "right" and (self.posy,self.posx+1) not in [(o.posy, o.posx) for o in obstacles]and (self.posx+1,self.posy)!=emeny_pos: 
                self.posx = min(game.width - 1, self.posx + 1)
            # 方向相反 不移动
            elif self.direction == "left": pass
            # 方向不向左 改变方向
            else: self.direction = "right"

    # 返回表示当前坦克外形的字符
    def Tank_Directions(self,shape):
        t = total_shape[shape][0]
        if self.direction == "down":
            t = total_shape[shape][1]
        elif self.direction == "left":
            t = total_shape[shape][2]
        elif self.direction == "right":
            t = total_shape[shape][3]
        return t

    def is_hit(self):
        return self.health <= 0


# 子类Bullet
class Bullet(Object):
    def __init__(self, posx, posy, direction):
        super().__init__(posx, posy)
        self.direction = direction  # 子弹方向
        if direction == "up":
            self.posy -= 1
        elif direction == "down":
            self.posy += 1
        elif direction == "left":
            self.posx -= 1
        elif direction == "right":
            self.posx += 1
        


    def move(self):
        if self.direction == "up":
            self.posy -= 1
        elif self.direction == "down":
            self.posy += 1
        elif self.direction == "left":
            self.posx -= 1
        elif self.direction == "right":
            self.posx += 1


# 子类Obstacle
class Obstacle(Object):
    def __init__(self, posx, posy):
        super().__init__(posx, posy)


# 游戏类
class TankGame:
    def __init__(self, width, height, num_obstacles):
        self.width = width
        self.height = height
        self.tank1 = Tank(random.randint(0, width - 1), random.randint(0, height - 1))  # 玩家1
        self.tank2 = Tank(random.randint(0, width - 1), random.randint(0, height - 1))  # 玩家2
        self.obstacles = self.generate_obstacles(num_obstacles)
        self.bullet1 = None
        self.bullet2 = None
        self.running = True
        self.obstacles=self.generate_obstacles(num_obstacles)

    def generate_obstacles(self, num_obstacles):
        obstacles = []
        while len(obstacles) < num_obstacles:
            posx = random.randint(0, self.width - 1)
            posy = random.randint(0, self.height - 1)
            obstacle = Obstacle(posx, posy)
            if (posx, posy) != (self.tank1.posx, self.tank1.posy) and (posx, posy) != (self.tank2.posx, self.tank2.posy) and (posx, posy) not in [(o.posx, o.posy) for o in obstacles]:
                obstacles.append(obstacle)
        return obstacles

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def draw_map(self):
        self.clear_screen()
        game_map = [["." for _ in range(self.width)] for _ in range(self.height)]
        game_map[self.tank1.posy][self.tank1.posx] = self.tank1.Tank_Directions(shape_tank1)  # Tank 1
        game_map[self.tank2.posy][self.tank2.posx] = self.tank2.Tank_Directions(shape_tank2)  # Tank 2
        for obstacle in self.obstacles:
            game_map[obstacle.posy][obstacle.posx] = "#"  # Obstacle
        if self.bullet1:
            game_map[self.bullet1.posy][self.bullet1.posx] = "*"  # Bullet 1
        if self.bullet2:
            game_map[self.bullet2.posy][self.bullet2.posx] = "o"  # Bullet 2

        print(f"Player 1 Health: {self.tank1.health} | Player 2 Health: {self.tank2.health}")
        for row in game_map:
            print(" ".join(row))
        print("\n" + "-" * self.width * 2)

    def move_bullets(self):
        while self.running:
            if self.bullet1:
                self.bullet1.move()
                if self.bullet1.posy < 0 or self.bullet1.posy >= self.height or self.bullet1.posx < 0 or self.bullet1.posx >= self.width or (self.bullet1.posx, self.bullet1.posy) in [(o.posx, o.posy) for o in self.obstacles]:
                    self.bullet1 = None  # 子弹超出边界
                elif (self.bullet1.posx, self.bullet1.posy) == (self.tank2.posx, self.tank2.posy):
                    self.tank2.health -= 1
                    # print(f"Player 2 hit! Health: {self.tank2.health}")
                    self.bullet1 = None  # 子弹消失

            if self.bullet2:
                self.bullet2.move()
                if self.bullet2.posy < 0 or self.bullet2.posy >= self.height or self.bullet2.posx < 0 or self.bullet2.posx >= self.width or (self.bullet2.posx, self.bullet2.posy) in [(o.posx, o.posy) for o in self.obstacles]: 
                    self.bullet2 = None  # 子弹超出边界
                elif (self.bullet2.posx, self.bullet2.posy) == (self.tank1.posx, self.tank1.posy):
                    self.tank1.health -= 1
                    # print(f"Player 1 hit! Health: {self.tank1.health}")
                    self.bullet2 = None  # 子弹消失

            if self.tank1.is_hit() or self.tank2.is_hit():
                self.running = False  # 停止游戏
            time.sleep(0.05)

    def handle_input(self):
        while self.running:
            # 玩家1控制
            if keyboard.is_pressed('w') :
                self.tank1.move("up",self.obstacles,(self.tank2.posx,self.tank2.posy))
            elif keyboard.is_pressed('s'):
                self.tank1.move("down",self.obstacles,(self.tank2.posx,self.tank2.posy))
            elif keyboard.is_pressed('a') :
                self.tank1.move("left",self.obstacles,(self.tank2.posx,self.tank2.posy))
            elif keyboard.is_pressed('d') :
                self.tank1.move("right",self.obstacles,(self.tank2.posx,self.tank2.posy))
            elif keyboard.is_pressed('o'):
                if not self.bullet1:  # 玩家1发射子弹
                    self.bullet1 = Bullet(self.tank1.posx, self.tank1.posy, self.tank1.direction)
                    # print(f"Player 1 shot from ({self.bullet1.posx}, {self.bullet1.posy})!")

            # 玩家2控制
            if keyboard.is_pressed('5') :
                self.tank2.move("up",self.obstacles,(self.tank1.posx,self.tank1.posy))
            elif keyboard.is_pressed('2'):
                self.tank2.move("down",self.obstacles,(self.tank1.posx,self.tank1.posy))
            elif keyboard.is_pressed('1') :
                self.tank2.move("left",self.obstacles,(self.tank1.posx,self.tank1.posy))
            elif keyboard.is_pressed('3'):
                self.tank2.move("right",self.obstacles,(self.tank1.posx,self.tank1.posy))
            elif keyboard.is_pressed('enter'):
                if not self.bullet2:  # 玩家2发射子弹
                    self.bullet2 = Bullet(self.tank2.posx, self.tank2.posy, self.tank2.direction)
                    # print(f"Player 2 shot from ({self.bullet2.posx}, {self.bullet2.posy})!")

            time.sleep(0.1)  # 适当降低检查频率

    def play(self):
        bullet_thread = threading.Thread(target=self.move_bullets)
        bullet_thread.start()

        while self.running:
            self.draw_map()
            time.sleep(0.05)  # 刷新地图的频率

        # 游戏结束，输出胜利者
        if self.tank1.is_hit():
            print("游戏结束,玩家2获胜！")
        elif self.tank2.is_hit():
            print("游戏»结束,玩家1获胜！")

# 运行游戏
if __name__ == "__main__":

    print("欢迎来到坦克大战！\n");
    print("玩家1使用 WASD 控制，玩家2使用 5213 控制。\n");
    print("玩家1按下O发射子弹, 玩家2按下Enter发射子弹。\n");
    width=int(input("请输入地图宽度：")) 
    height=int(input("请输入地图高度："))
    num_obstacles=int(input("请输入障碍物数量："))
    shape_tank1=int(input("请选择玩家一的坦克形状:\n1.↑↓←→\n2.㊤㊦㊧㊨\n3.▲▼◄►\n"))-1
    shape_tank2=int(input("请选择玩家二的坦克形状:\n1.↑↓←→\n2.㊤㊦㊧㊨\n3.▲▼◄►\n"))-1
    print("游戏开始！\n");
    game = TankGame(width, height, num_obstacles)
    input_thread = threading.Thread(target=game.handle_input)
    input_thread.start()
    game.play()
