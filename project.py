import pygame
import os
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

WIDTH = 1918
HEIGHT = 1035
FPS = 120
SPEED = 7

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Adventure")

icon = pygame.image.load("assets/icon.png")

pygame.display.set_icon(icon)

clock = pygame.time.Clock()

font = pygame.font.Font("font/YanoneKaffeesatz-Regular.ttf", 28)

# загрузка текстур и анимаций игры
background = pygame.image.load("assets/background.jpg").convert()
background_position = 0

menu_background = pygame.image.load("assets/menu.jpg").convert()

# анимация полёта
fly_frame1 = pygame.image.load("player/dragon1.png").convert_alpha()
fly_frame2 = pygame.image.load("player/dragon2.png").convert_alpha()
fly_frame3 = pygame.image.load("player/dragon3.png").convert_alpha()
fly_frame4 = pygame.image.load("player/dragon4.png").convert_alpha()
fly_animation = [fly_frame1, fly_frame2, fly_frame3, fly_frame4]

# анимация огненного дыхания
breath_frame1 = pygame.image.load("assets/fire1.png").convert_alpha()
breath_frame2 = pygame.image.load("assets/fire2.png").convert_alpha()
breath_frame3 = pygame.image.load("assets/fire3.png").convert_alpha()
breath_frame4 = pygame.image.load("assets/fire4.png").convert_alpha()
breath_animation = [breath_frame1, breath_frame2, breath_frame3, breath_frame4]

# анимация огненных шаров
fire_frame1 = pygame.image.load("assets/fire_ball1.png").convert_alpha()
fire_frame2 = pygame.image.load("assets/fire_ball2.png").convert_alpha()
fire_frame3 = pygame.image.load("assets/fire_ball3.png").convert_alpha()
fire_frame4 = pygame.image.load("assets/fire_ball4.png").convert_alpha()
fire_animation = [fire_frame1, fire_frame2, fire_frame3, fire_frame4]

# анимация вращения монеты
coin_frame1 = pygame.image.load("assets/coin.png").convert_alpha()
coin_frame2 = pygame.image.load("assets/coin2.png").convert_alpha()
coin_frame3 = pygame.image.load("assets/coin3.png").convert_alpha()
coin_frame4 = pygame.image.load("assets/coin4.png").convert_alpha()
coin_frame5 = pygame.image.load("assets/coin5.png").convert_alpha()
coin_frame6 = pygame.image.load("assets/coin6.png").convert_alpha()
coin_frame7 = pygame.image.load("assets/coin7.png").convert_alpha()
coin_animation = [coin_frame1, coin_frame2, coin_frame3, coin_frame4, coin_frame5, coin_frame6, coin_frame7]

# анимация буквы R для рестарта
r_frame1, r_frame2 = pygame.image.load("assets/0.png"), pygame.image.load("assets/1.png")
r_frame3, r_frame4 = pygame.image.load("assets/2.png"), pygame.image.load("assets/3.png")
r_frame5, r_frame6 = pygame.image.load("assets/4.png"), pygame.image.load("assets/5.png")
r_animation = [r_frame1, r_frame2, r_frame3, r_frame4, r_frame5, r_frame6]

# текстура препятствий
obstacle_texture = pygame.image.load("assets/obstacle.png").convert_alpha()

# интерфейс
coin_icon = pygame.image.load("assets/coin_icon.png").convert_alpha()
info_bar = pygame.image.load("assets/info_bar.png").convert_alpha()

# элементы меню
game_logo = pygame.image.load("assets/game_logo.png").convert_alpha()
start_game = pygame.image.load("assets/start_game.png").convert_alpha()
new_game = pygame.image.load("assets/new_game.png").convert_alpha()
help_play = pygame.image.load("assets/how_play.png").convert_alpha()
end_game = pygame.image.load("assets/end_game.png").convert_alpha()
back_menu = pygame.image.load("assets/back_menu.png").convert_alpha()
control = pygame.image.load("assets/control.png").convert_alpha()

# звуковое сопровождение
breath_sound = pygame.mixer.Sound("sounds/fire_breath.wav")
wings_sound = pygame.mixer.Sound("sounds/wings.wav")
collect_coin = pygame.mixer.Sound("sounds/collect_coin.wav")
fire_shoot = pygame.mixer.Sound("sounds/fire_shoot.wav")

obstacle_position = [650, 750, 800]

obstacle_list = []

coin_list = []

fire_list = []

# основные игровые события
OBSTACLE_GENERATOR = pygame.USEREVENT
pygame.time.set_timer(OBSTACLE_GENERATOR, 1500)

COIN_GENERATOR = pygame.USEREVENT + 1
pygame.time.set_timer(COIN_GENERATOR, 1800)

ANIMATION = pygame.USEREVENT + 2
pygame.time.set_timer(ANIMATION, 120)


def draw_background(position):
    display.blit(background, (position, 0))
    display.blit(background, (position + WIDTH, 0))


class Menu(object):
    def __init__(self):
        self.frames = 0

    @staticmethod
    def run_menu(statement):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                quit()

            if statement == "Меню":
                pygame.mixer.stop()
                if not playing:
                    while not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load("sounds/main_music.mp3")
                        pygame.mixer.music.set_volume(0.6)
                        pygame.mixer.music.play(-1)
                    dragon.falling_speed = 0
                    dragon.health = 100
                    dragon.energy = 50
                    dragon.score = 0
                    dragon.coins = 0
                    dragon.y = position_y
                    obstacle_list.clear()
                    coin_list.clear()

            elif statement == "Конец игры":
                pygame.mixer.stop()
                if keys[pygame.K_r] and not playing:
                    dragon.falling_speed = 0
                    dragon.health = 100
                    dragon.energy = 50
                    dragon.score = 0
                    dragon.coins = 0
                    dragon.y = position_y
                    obstacle_list.clear()
                    coin_list.clear()

                    return True

    @staticmethod
    def menu_load():

        display.blit(menu_background, (0, 0))
        display.blit(game_logo, (645, 90))

        start_button = start_game.get_rect(center=(950, 400))
        display.blit(start_game, start_button)

        new_button = new_game.get_rect(center=(950, 500))
        display.blit(new_game, new_button)

        how_button = help_play.get_rect(center=(950, 600))
        display.blit(help_play, how_button)

        end_button = end_game.get_rect(center=(950, 700))
        display.blit(end_game, end_button)

        record_text = font.render("Всего монет: " + str(int(dragon.all_coins)), 1, (255, 255, 255))
        record_pos = record_text.get_rect(center=(1600, 450))
        display.blit(coin_icon, (record_pos.right + 10, record_pos.y))
        display.blit(record_text, record_pos)

        record2_text = font.render("Наилучший результат: " + str(int(dragon.height_score)) + " м", 1, (255, 255, 255))
        display.blit(record2_text, (record_pos.x, record_pos.y + 40))

        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_focused() and mouse[0]:
            x, y = pos
            if start_button.left < x < start_button.right and start_button.top < y < start_button.bottom:
                return "Начать игру"
            elif new_button.left < x < new_button.right and new_button.top < y < new_button.bottom:
                return "Новая игра"
            elif how_button.left < x < how_button.right and how_button.top < y < how_button.bottom:
                return "Как играть"
            elif end_button.left < x < end_button.right and end_button.top < y < end_button.bottom:
                return "Выход"
        return "Бездействие"

    @staticmethod
    def how_play():
        display.blit(menu_background, (0, 0))
        display.blit(control, (800, 150))

    def result_load(self, player):
        display.blit(menu_background, (0, 0))
        display.blit(game_logo, (640, 90))
        menu_font = pygame.font.Font("font/YanoneKaffeesatz-Regular.ttf", 35)

        res_text = menu_font.render("Ваш результат: ", 1, (255, 255, 255))
        res_pos = res_text.get_rect(center=(950, 370))
        display.blit(res_text, res_pos)

        info_text = menu_font.render("Пройденное расстояние: " + str(int(player.score)) + " м | Собрано монет: "
                                     + str(int(player.coins)), 1, (255, 255, 255))
        info_pos = info_text.get_rect(center=(930, 440))
        display.blit(info_text, info_pos)
        display.blit(coin_icon, (info_pos.right + 10, info_pos.y))

        replay_text = menu_font.render("Нажмите клавишу         чтобы начать заново!", 1, (255, 255, 255))
        replay_pos = replay_text.get_rect(center=(950, 540))
        display.blit(replay_text, replay_pos)
        if self.frames + 1 >= 48:
            self.frames = 0
        display.blit(r_animation[self.frames // 8], (replay_pos.left + 202, replay_pos.y - 20))
        self.frames += 1

        # display.blit(game_over, (760, 530))

        button = back_menu.get_rect(center=(940, 750))
        display.blit(back_menu, button)

        position = pygame.mouse.get_pos()

        if pygame.mouse.get_focused() and mouse[0]:
            x, y = position
            if button.left < x < button.right and button.top < y < button.bottom:
                return True
        return False


class Player(object):
    def __init__(self, x, y):
        # основные характеристики
        self.x = x
        self.y = y
        self.speed = SPEED
        self.gravity = 1
        self.fall = True
        self.fly = False
        self.falling_speed = 0

        # основные элементы
        self.conf = open("save.conf", "r")
        self.health = 100
        self.energy = 50
        self.coins = 0
        self.all_coins = int(self.conf.readline())
        self.score = 0
        self.height_score = int(self.conf.readline())

        # обработка анимации
        self.frames = 0

    def draw(self):

        # прорисовка анимации и получение границ объекта
        dragon_fly = fly_animation[self.frames]
        dragon_bounds = dragon_fly.get_rect(center=(self.x, self.y))
        new_dragon_bounds = dragon_bounds.inflate(0, -30)
        display.blit(dragon_fly, dragon_bounds)

        return new_dragon_bounds

    def gui_draw(self):

        info_pos_x = 400
        info_pos_y = 880

        # отображение текущего здоровья объекта
        pygame.draw.rect(display, (255, 0, 0), (info_pos_x + 90, info_pos_y + 50, int(self.health * 3), 22))

        # отображение текущей выносливости
        pygame.draw.rect(display, (0, 155, 250), (info_pos_x + 705, info_pos_y + 50, self.energy * 6, 22))

        display.blit(info_bar, (info_pos_x, info_pos_y))

        # численное количество жизней
        health_text = font.render(str(int(self.health)) + " HP", 1, (255, 255, 255))
        health_place = health_text.get_rect(center=(info_pos_x + 250, info_pos_y + 50))
        display.blit(health_text, health_place)

        # численное количество энергии
        energy_text = font.render(str(self.energy) + " SP", 1, (255, 255, 255))
        energy_place = energy_text.get_rect(center=(info_pos_x + 870, info_pos_y + 50))
        display.blit(energy_text, energy_place)

        # численное количество монет
        coin_text = font.render("Монеты :  " + str(self.coins), 1, (255, 255, 255))
        coin_place = coin_text.get_rect(center=(info_pos_x + 800, info_pos_y))
        display.blit(coin_text, coin_place)
        display.blit(coin_icon, (coin_place.right + 10, info_pos_y - 17))

        # отображение пройденного расстояния
        score_text = font.render("Вы пролетели: " + str(int(self.score)) + " м", 1, (255, 255, 255))
        score_place = score_text.get_rect(center=(info_pos_x + 545, info_pos_y + 63))
        display.blit(score_text, score_place)

    # обработка полёта
    def flying(self):
        self.fly = True
        self.falling_speed = 0
        self.y -= 3

    # обработка гравитации
    def falling(self):
        if self.fall:
            self.falling_speed += self.gravity
            self.y += self.falling_speed // 9

    # проверка столкновений объекта с препятствиями
    def check_collision(self, items):
        dragon_bounds = self.draw()
        for element in items:
            if dragon_bounds.colliderect(element):
                if self.health >= 0.5:
                    self.health -= 0.5
                    return True
                else:
                    self.health = 0
                    return False
        if dragon_bounds.top <= -150 or dragon_bounds.bottom >= 1100:
            self.health = 0
            return False
        return True

    def energy_recover(self):
        if 0 <= self.energy < 50:
            self.energy += 1

    def collect_item(self, items):
        dragon_bounds = self.draw()
        for element in items:
            if dragon_bounds.colliderect(element):
                wings_sound.stop()
                collect_coin.play()
                self.coins += 1
                self.all_coins += 1
                items.remove(element)

    def saving(self):
        conf = open("save.conf", "w")
        conf.write(str(self.all_coins) + "\n" + str(self.height_score))
        conf.close()


class Item(object):
    def __init__(self):
        self.x = 1980
        self.frames = 0
        self.rotate = False

    def draw(self, items, kind):
        if kind == "obstacle":
            for element in items:
                if element.bottom >= 900:
                    display.blit(obstacle_texture, element)
                else:
                    reverse_obstacle = pygame.transform.flip(obstacle_texture, False, True)
                    display.blit(reverse_obstacle, element)

        elif kind == "coin":
            if self.rotate:
                item_animation = coin_animation[self.frames]
                for element in items:
                    display.blit(item_animation, element)

    def create(self, kind):
        if kind == "obstacle":
            random_height = random.choice(obstacle_position)
            obstacle_bottom = obstacle_texture.get_rect(midtop=(self.x, random_height))
            obstacle_top = obstacle_texture.get_rect(midbottom=(self.x, random_height - 400))
            return obstacle_bottom, obstacle_top

        elif kind == "coin":
            random_pos = random.randrange(100, 800)
            coin_bounds = coin_frame1.get_rect(midtop=(self.x, random_pos))
            return coin_bounds

    def collision_with(self, items):
        obstacle_bottom, obstacle_top = self.create("obstacle")
        for element in items:
            if element.colliderect(obstacle_bottom) or element.colliderect(obstacle_top):
                element.y = element.y + 100

    @staticmethod
    def move_position(items):
        for element in items:
            element.centerx -= SPEED
        return items

    @staticmethod
    def delete(items):
        for element in items:
            if element.centerx == - 30:
                items.remove(element)


class Attack(object):
    # инициализация параметров атакующего объекта
    def __init__(self, player):
        self.x = player.x
        self.y = player.y
        self.frames = 0
        self.attack = False

    # отрисовка анимации атакующего объекта
    def draw(self, player):
        if self.attack:
            pos_x = player.x + 200
            pos_y = player.y + 20
            attack_animation = breath_animation[self.frames]
            breath_bounds = attack_animation.get_rect(center=(pos_x, pos_y))
            display.blit(attack_animation, breath_bounds)
            return breath_bounds

    def check_collision(self, obstacles):
        breath_bounds = self.draw(dragon)
        for element in obstacles:
            if breath_bounds is not None:
                if breath_bounds.colliderect(element):
                    obstacles.remove(element)


class Bullet(object):
    def __init__(self):
        self.x = dragon.x
        self.y = dragon.y
        self.frames = 0
        self.speed = 6
        self.animation = False
        self.destroy = False

    def draw(self, items):
        if self.animation:
            bullet_animation = fire_animation[self.frames]
            for element in items:
                display.blit(bullet_animation, element)

    def move_position(self, items):
        for element in items:
            element.centerx += self.speed
            return element

    @staticmethod
    def create(player):
        pos_x = player.x + 150
        pos_y = player.y + 20
        ball_bounds = fire_frame1.get_rect(center=(pos_x, pos_y))
        return ball_bounds

    def check_collision(self, obstacles):
        fire_bounds = self.move_position(fire_list)
        if fire_bounds is not None:
            for element in obstacles:
                if fire_bounds.colliderect(element):
                    obstacles.remove(element)
                    self.destroy = True

    def delete(self, items):
        for element in items:
            if element.centerx > 1940:
                items.remove(element)
            elif self.destroy:
                items.remove(element)
                self.destroy = False


position_x = 400
position_y = 300

dragon = Player(position_x, position_y)
obstacle = Item()
coin = Item()
breath = Attack(dragon)
bullet = Bullet()
menu = Menu()


starting = "Бездействие"
playing = False
running = True

while running:

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    if starting == "Бездействие":
        Menu.run_menu("Меню")
        state = Menu.menu_load()
        if state == "Начать игру":
            playing = True
            starting = False
        elif state == "Новая игра":
            dragon.all_coins = 0
            dragon.height_score = 0
            save = open("save.conf", "w")
            save.write(str(dragon.all_coins) + "\n" + str(dragon.height_score))
            save.close()
            playing = True
            starting = False
        elif state == "Как играть":
            Menu.how_play()
        elif state == "Выход":
            exit()

    elif playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == ANIMATION and keys[pygame.K_w]:
                dragon.fly = True
                if dragon.frames < 3:
                    dragon.frames += 1
                else:
                    dragon.frames = 0
            elif keys[pygame.K_w]:
                dragon.fly = True
            else:
                if dragon.frames != 0:
                    dragon.frames -= 1
                dragon.fly = False

            if event.type == ANIMATION and not keys[pygame.K_SPACE] and not keys[pygame.K_f]:
                dragon.energy_recover()

            if event.type == ANIMATION and keys[pygame.K_SPACE]:
                if dragon.energy >= 5:
                    breath.attack = True
                    dragon.energy -= 5
                    breath_sound.play()
                else:
                    breath.attack = False

                if breath.attack:
                    if breath.frames < 3:
                        breath.frames += 1
                    else:
                        breath.frames = 0

            elif event.type == ANIMATION:
                breath.attack = False
                coin.rotate = True
                if coin.frames < 6:
                    coin.frames += 1
                else:
                    coin.frames = 0

            if event.type == ANIMATION:
                bullet.animation = True
                if bullet.frames < 3:
                    bullet.frames += 1
                else:
                    bullet.frames = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:

                    if dragon.energy >= 25:
                        bullet.attack = True

                        if bullet.attack:
                            fire_list.append(bullet.create(dragon))
                            pygame.mixer.stop()
                            fire_shoot.play()

                        dragon.energy -= 25
                    else:
                        bullet.attack = False

            if keys[pygame.K_d]:
                dragon.score += 0.025
                if dragon.height_score < dragon.score:
                    dragon.height_score = int(dragon.score)
                if event.type == OBSTACLE_GENERATOR:
                    obstacle_list.extend(obstacle.create("obstacle"))
                if event.type == COIN_GENERATOR:
                    coin_list.append(coin.create("coin"))

        if keys[pygame.K_w]:
            dragon.flying()

        if keys[pygame.K_d]:
            background_position -= dragon.speed
            obstacle_list = obstacle.move_position(obstacle_list)
            coin_list = coin.move_position(coin_list)
            bullet.speed = 2
        else:
            bullet.speed = 6

        if dragon.fall and not dragon.fly:
            dragon.falling()

        if keys[pygame.K_w] and not breath.attack:
            wings_sound.play()

        elif keys[pygame.K_w] and breath.attack:
            wings_sound.stop()
        else:
            wings_sound.stop()

        # прорисовка фона
        draw_background(background_position)

        if background_position <= -WIDTH:
            background_position = 0

        # прорисовка элементов игры и их своевременная очистка
        obstacle.draw(obstacle_list, "obstacle")
        obstacle.delete(obstacle_list)

        obstacle.collision_with(coin_list)
        coin.draw(coin_list, "coin")
        coin.delete(coin_list)

        # прорисовка игрока
        dragon.draw()
        playing = dragon.check_collision(obstacle_list)
        dragon.collect_item(coin_list)

        if dragon.health == 0:
            pygame.mixer.music.load("C:/Users/acer/Desktop/GameProject/sounds/death_music.wav")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        elif dragon.health > 0:
            pygame.mixer.music.stop()

        # проверка столкновения и прорисовка огненного дыхания
        breath.check_collision(obstacle_list)

        # прорисовка, движение и удаление огненных шаров
        bullet.draw(fire_list)
        bullet.move_position(fire_list)
        bullet.check_collision(obstacle_list)
        bullet.delete(fire_list)

        # прорисовка информации о текущих параметрах
        dragon.gui_draw()
        # сохранение прогресса
        dragon.saving()
    else:
        playing = Menu.run_menu("Конец игры")
        state = menu.result_load(dragon)
        if state:
            pygame.mixer.music.stop()
            starting = "Бездействие"

    fps = int(clock.get_fps())
    fps_text = font.render("FPS: " + str(fps), 1, (255, 255, 255))
    fps_pos = fps_text.get_rect(center=(60, 35))
    display.blit(fps_text, fps_pos)

    pygame.display.update()
    clock.tick(FPS)
