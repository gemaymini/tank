import random
import time
import threading
import keyboard  
import os

total_shape = ["↑↓←→", "NSWE", "▲▼◄►"]
shape_tank1 = -1
shape_tank2 = -1

# 基类Object
class Object:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy

# 子类Tank
class Tank(Object):
    def __init__(self, posx, posy):
        super().__init__(posx, posy)
        self.health = 3  # 初始血量
        self.attack_power = 1  # 初始攻击力
        self.defense_power = 0  # 初始防御力
        self.direction = "up"  # 初始朝向

    def move(self, direction, obstacles, enemy_pos):
        if direction == "up":
            if self.direction == "up" and (self.posx, self.posy - 1) not in [(o.posx, o.posy) for o in obstacles] and (self.posx, self.posy - 1) != enemy_pos:
                self.posy = max(0, self.posy - 1)
            elif self.direction == "down": pass
            else: self.direction = "up"

        elif direction == "down":
            if self.direction == "down" and (self.posx, self.posy + 1) not in [(o.posx, o.posy) for o in obstacles] and (self.posx, self.posy + 1) != enemy_pos:
                self.posy = min(game.height - 1, self.posy + 1)
            elif self.direction == "up": pass
            else: self.direction = "down"

        elif direction == "left":
            if self.direction == "left" and (self.posy, self.posx - 1) not in [(o.posy, o.posx) for o in obstacles] and (self.posx - 1, self.posy) != enemy_pos:
                self.posx = max(0, self.posx - 1)
            elif self.direction == "right": pass
            else: self.direction = "left"

        elif direction == "right":
            if self.direction == "right" and (self.posy, self.posx + 1) not in [(o.posy, o.posx) for o in obstacles] and (self.posx + 1, self.posy) != enemy_pos:
                self.posx = min(game.width - 1, self.posx + 1)
            elif self.direction == "left": pass
            else: self.direction = "right"
    def apply_powerup(self, powerup):
        if powerup.type == "health":
            self.health += powerup.value
        elif powerup.type == "attack":
            self.attack_power += powerup.value
        elif powerup.type == "defense":
            self.defense_power += powerup.value
    def Tank_Directions(self, shape):
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

# 子类SpecialObstacle
class SpecialObstacle(Obstacle):
    def __init__(self, posx, posy, health=2):
        super().__init__(posx, posy)
        self.health = health  # 初始生命值

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            return True  # 返回True表示该障碍物已被摧毁
        return False
    

# 子类PowerUp
class PowerUp(Object):
    def __init__(self, posx, posy, type, value):
        super().__init__(posx, posy)
        self.type = type  # 道具类型: 'health', 'attack', 'defense'
        self.value = value  # 道具加成值
# 游戏类
class TankGame:
    def __init__(self, width, height, num_obstacles, num_powerups):
        self.width = width
        self.height = height
        self.tank1 = Tank(random.randint(0, width - 1), random.randint(0, height - 1))  # 玩家1
        self.tank2 = Tank(random.randint(0, width - 1), random.randint(0, height - 1))  # 玩家2
        self.obstacles = self.generate_obstacles(num_obstacles)
        self.powerups = self.generate_powerups(num_powerups)
        self.bullet1 = None
        self.bullet2 = None
        self.running = True

    def generate_obstacles(self, num_obstacles):
        obstacles = []
        while len(obstacles) < num_obstacles:
            posx = random.randint(0, self.width - 1)
            posy = random.randint(0, self.height - 1)
            if random.random() < 0.3:  # 30%概率生成特殊障碍物
                obstacle = SpecialObstacle(posx, posy)
            else:
                obstacle = Obstacle(posx, posy)

            if (posx, posy) != (self.tank1.posx, self.tank1.posy) and (posx, posy) != (self.tank2.posx, self.tank2.posy) and (posx, posy) not in [(o.posx, o.posy) for o in obstacles]:
                obstacles.append(obstacle)
        return obstacles

    def generate_powerups(self, num_powerups):
        powerups = []
        occupied_positions = {(self.tank1.posx, self.tank1.posy), (self.tank2.posx, self.tank2.posy)}
        occupied_positions.update((o.posx, o.posy) for o in self.obstacles)

        while len(powerups) < num_powerups:
            posx = random.randint(0, self.width - 1)
            posy = random.randint(0, self.height - 1)
            if (posx, posy) not in occupied_positions:  # 确保道具位置不与坦克或障碍物重叠
                type = random.choice(["health", "attack", "defense"])
                value = random.randint(1, 2)  # 加成值
                powerup = PowerUp(posx, posy, type, value)
                powerups.append(powerup)
                occupied_positions.add((posx, posy))  # 将道具位置加入已占用位置
        return powerups
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def draw_map(self):
        self.clear_screen()
        game_map = [["." for _ in range(self.width)] for _ in range(self.height)]
        game_map[self.tank1.posy][self.tank1.posx] = self.tank1.Tank_Directions(shape_tank1)  # Tank 1
        game_map[self.tank2.posy][self.tank2.posx] = self.tank2.Tank_Directions(shape_tank2)  # Tank 2
        
        for obstacle in self.obstacles:
            if isinstance(obstacle, SpecialObstacle):
                game_map[obstacle.posy][obstacle.posx] = "M"  # 特殊障碍物
            else:
                game_map[obstacle.posy][obstacle.posx] = "#"  # 普通障碍物
        for powerup in self.powerups:
            game_map[powerup.posy][powerup.posx] = "P"  # 道具

        if self.bullet1:
            game_map[self.bullet1.posy][self.bullet1.posx] = "*"  # Bullet 1
        if self.bullet2:
            game_map[self.bullet2.posy][self.bullet2.posx] = "o"  # Bullet 2

        print(f"Player 1 Health: {self.tank1.health} | Attack: {self.tank1.attack_power} | Defense: {self.tank1.defense_power}")
        print(f"Player 2 Health: {self.tank2.health} | Attack: {self.tank2.attack_power} | Defense: {self.tank2.defense_power}")
        for row in game_map:
            print(" ".join(row))
        print("\n" + "-" * self.width * 2)

    def check_powerup_pickup(self, tank):
        for powerup in self.powerups[:]:  # 创建列表副本以便安全删除
            if (tank.posx, tank.posy) == (powerup.posx, powerup.posy):
                tank.apply_powerup(powerup)
                self.powerups.remove(powerup)  # 从游戏中移除道具

    def move_bullets(self):
        while self.running:
            if self.bullet1:
                self.bullet1.move()
                if self.bullet1.posy < 0 or self.bullet1.posy >= self.height or self.bullet1.posx < 0 or self.bullet1.posx >= self.width:
                    self.bullet1 = None  # 子弹超出边界
                elif (self.bullet1.posx, self.bullet1.posy) == (self.tank2.posx, self.tank2.posy):
                    hurt=self.tank1.attack_power-self.tank2.defense_power
                    if hurt<=0:
                        self.bullet1 = None
                    else:
                        self.tank2.health -= hurt
                        self.bullet1 = None  # 子弹消失
                else:
                    for obstacle in self.obstacles:
                        if (self.bullet1.posx, self.bullet1.posy) == (obstacle.posx, obstacle.posy):
                            if isinstance(obstacle, SpecialObstacle):
                                if obstacle.hit():
                                    self.obstacles.remove(obstacle)  # 移除已摧毁的特殊障碍物
                                    # print("特殊障碍物被摧毁！")
                                self.bullet1 = None  # 子弹消失
                                break
                            else:
                                self.bullet1 = None  # 子弹消失
                                break

            if self.bullet2:
                self.bullet2.move()
                if self.bullet2.posy < 0 or self.bullet2.posy >= self.height or self.bullet2.posx < 0 or self.bullet2.posx >= self.width:
                    self.bullet2 = None  # 子弹超出边界
                elif (self.bullet2.posx, self.bullet2.posy) == (self.tank1.posx, self.tank1.posy):
                    hurt=self.tank2.attack_power-self.tank1.defense_power
                    if hurt<=0:
                        self.bullet2 = None
                    else:
                        self.tank1.health -= hurt
                        self.bullet2 = None  # 子弹消失
                else:
                    for obstacle in self.obstacles:
                        if (self.bullet2.posx, self.bullet2.posy) == (obstacle.posx, obstacle.posy):
                            if isinstance(obstacle, SpecialObstacle):
                                if obstacle.hit():
                                    self.obstacles.remove(obstacle)  # 移除已摧毁的特殊障碍物
                                    # print("特殊障碍物被摧毁！")
                                self.bullet2 = None  # 子弹消失
                                break
                            else:
                                self.bullet2 = None  # 子弹消失
                                break

            if self.tank1.is_hit() or self.tank2.is_hit():
                self.running = False  # 停止游戏
            time.sleep(0.05)

    def handle_input(self):
        while self.running:
            # 玩家1控制
            if keyboard.is_pressed('w'):
                self.tank1.move("up", self.obstacles, (self.tank2.posx, self.tank2.posy))
            elif keyboard.is_pressed('s'):
                self.tank1.move("down", self.obstacles, (self.tank2.posx, self.tank2.posy))
            elif keyboard.is_pressed('a'):
                self.tank1.move("left", self.obstacles, (self.tank2.posx, self.tank2.posy))
            elif keyboard.is_pressed('d'):
                self.tank1.move("right", self.obstacles, (self.tank2.posx, self.tank2.posy))
            elif keyboard.is_pressed('o'):
                if not self.bullet1:  # 玩家1发射子弹
                    self.bullet1 = Bullet(self.tank1.posx, self.tank1.posy, self.tank1.direction)

            # 玩家2控制
            if keyboard.is_pressed('5'):
                self.tank2.move("up", self.obstacles, (self.tank1.posx, self.tank1.posy))
            elif keyboard.is_pressed('2'):
                self.tank2.move("down", self.obstacles, (self.tank1.posx, self.tank1.posy))
            elif keyboard.is_pressed('1'):
                self.tank2.move("left", self.obstacles, (self.tank1.posx, self.tank1.posy))
            elif keyboard.is_pressed('3'):
                self.tank2.move("right", self.obstacles, (self.tank1.posx, self.tank1.posy))
            elif keyboard.is_pressed('enter'):
                if not self.bullet2:  # 玩家2发射子弹
                    self.bullet2 = Bullet(self.tank2.posx, self.tank2.posy, self.tank2.direction)

            # 检查是否拾取道具
            self.check_powerup_pickup(self.tank1)
            self.check_powerup_pickup(self.tank2)

            time.sleep(0.1)  # 适当降低检查频率

    def play(self):
        bullet_thread = threading.Thread(target=self.move_bullets)
        bullet_thread.start()

        while self.running:
            self.draw_map()
            time.sleep(0.05)  # 刷新地图的频率

        # 游戏结束，输出胜利者
        if self.tank1.is_hit():
            print("游戏结束, 玩家2获胜！")
        elif self.tank2.is_hit():
            print("游戏结束, 玩家1获胜！")

# 运行游戏
if __name__ == "__main__":
    print("欢迎来到坦克大战！\n")
    print("玩家1使用 WASD 控制，玩家2使用 5213 控制。\n")
    print("玩家1按下O发射子弹, 玩家2按下Enter发射子弹。\n")
    print("普通障碍物#不可摧毁,特殊障碍物M可以被摧毁, 道具P可以被拾取\n")
    width = int(input("请输入地图宽度："))
    height = int(input("请输入地图高度："))
    num_obstacles = int(input("请输入障碍物数量："))
    num_powerups = int(input("请输入道具数量："))
    shape_tank1 = int(input("请选择玩家一的坦克形状:\n1.↑↓←→\n2.NSWE\n3.▲▼◄►\n")) - 1
    shape_tank2 = int(input("请选择玩家二的坦克形状:\n1.↑↓←→\n2.NSWE\n3.▲▼◄►\n")) - 1
    print("游戏开始！\n")
    game = TankGame(width, height, num_obstacles, num_powerups)
    input_thread = threading.Thread(target=game.handle_input)
    input_thread.start()
    game.play()
