import os
import sys
import pygame
import random
import csv


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # if colorkey is not None:
    #     image = image.convert()
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global input_name_player
    sound_intro = 'data\start_sound.mp3'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sound_intro)
    pygame.mixer.music.play()
    need_input = True
    while True:
        pygame.display.set_caption('Космическая база.')
        intro_text = ["Задача игрока управляя стрелками на клавиатуре Зеленым Роботом ",
                      "недопусить захвата центрального компьютера Красным Роботом.",
                      "Игрок может установить на пути Красного Робота",
                      "Препятствие или Бомбу.",
                      "Чтобы установить препятствие нужно найти инструментальный ящик.",
                      "ALT+ стрелка - установить препятствие.",
                      "Чтобы установить бомбу нужно найти сейф с бомбами.",
                      "CTRL+ стрелка - устанавить бомбу.",
                      " ",
                      "Красный Робот строит маршрут к компьютеру обходя стенки и препятствия,",
                      "но при этом не видит бомбы на поле.",
                      "При полном блоировании прохода к Центральному компьютеру или",
                      "перемещений Красного Робота препятствиями,",
                      "робот активирует уничтожение препятствия за 5 ходов.",
                      " ",
                      "для загрузки уровня введите Имя Игрока и нажмите Enter",
                      " ",
                      ">",
                      ]
        fon = pygame.transform.scale(load_image('start_fon.jpg'), (width, height))
        screen.blit(fon, (0, 0))

        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('blue'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 20
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        font_player_name = pygame.font.Font(font_file_name, 40)
        string_rendered1 = font_player_name.render(input_name_player, 1, pygame.Color('red'))
        intro_rect = string_rendered1.get_rect()
        text_coord = 550
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered1, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                terminate()
            elif event.type == pygame.KEYDOWN and need_input:
                if event.key == pygame.K_RETURN and need_input:
                    need_input = False
                    # input_name_player = ''
                    return  # начинаем игру

                elif event.key == pygame.K_BACKSPACE:
                    input_name_player = input_name_player[:-1]
                else:
                    if len(input_name_player) < 15:
                        input_name_player += event.unicode

            # elif event.type == pygame.KEYDOWN and need_input:
            #     if event.key == pygame.K_RETURN and need_input:
            #         need_input = False
            #         input_name_player = ''
            #     elif event.key == pygame.K_BACKSPACE:
            #         pass
            #     else:
            #         # input_name_player += event.unicode
            #         intro_text += event.unicode

        pygame.display.flip()

        clock.tick(FPS)


def end_screen():
    sound_intro = 'data\end_sound.mp3'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sound_intro)
    pygame.mixer.music.play()
    need_input = True
    score_file_name = 'data\score.txt'

    with open(score_file_name, encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter=",")
        count = 0
        print(file_reader)
        list_for_table = []
        for row in file_reader:
            if count == 0:
                # Вывод строки, содержащей заголовки для столбцов
                print(f'Файл содержит столбцы: {", ".join(row)}')
            # Вывод строк
            print(f' {row["Name"]} - {row["Score"]}')
            list_for_table.append([row["Name"], int(row["Score"])])
            print(list_for_table)
            count += 1
        print(f'Всего в файле {count + 1} строк.')
        find = 0
        for i in range(len(list_for_table)):
            if list_for_table[i][0] == input_name_player:
                find = 1
                if list_for_table[i][1] < score:
                    list_for_table[i][1] = score
        if not find:
            list_for_table.append([input_name_player, score])

        # find = 0
        # for i in range(len(list_for_table)):
        #     if list_for_table[i][0] == input_name_player and list_for_table[i][1] < score:
        #         del list_for_table[i]
        #         list_for_table.append([input_name_player, score])
        #         find = 1
        #     elif list_for_table[i][0] == input_name_player and list_for_table[i][1] >= score:
        #         find = 1
        # if find == 0:
        #     list_for_table.append([input_name_player, score])

        list_for_table.sort(key=lambda x: [x[1], x[0]], reverse=1)
        print(list_for_table)

    count = 0
    with open(score_file_name, mode="w", encoding='utf-8') as w_file:
        header_names = ["Name", "Score"]
        file_writer = csv.DictWriter(w_file, delimiter=",",
                                     lineterminator="\r", fieldnames=header_names)
        file_writer.writeheader()
        for row in list_for_table:
            file_writer.writerow({"Name": row[0], "Score": row[1]})

    while True:
        pygame.display.set_caption('Космическая база. Рекорды')
        fon = pygame.transform.scale(load_image('end_fon.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(font_file_name, 30)
        text_coord = 156
        for line in list_for_table:
            str_text_name, str_text_score = str(line[0]), str(line[1])
            name_string_rendered = font.render(str_text_name, 1, pygame.Color('red'))
            intro_rect0 = name_string_rendered.get_rect()
            score_string_rendered = font.render(str_text_score, 1, pygame.Color('red'))
            intro_rect1 = score_string_rendered.get_rect()
            text_coord += 10
            intro_rect0.top = text_coord
            intro_rect1.top = text_coord
            intro_rect0.x = 300
            intro_rect1.x = 700
            text_coord += intro_rect0.height
            screen.blit(name_string_rendered, intro_rect0)
            screen.blit(score_string_rendered, intro_rect1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                pygame.mixer.music.stop()
                return  # начинаем игру

        pygame.display.flip()

        clock.tick(FPS)


def reset_level():
    global x_point_hero, y_point_hero, x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp, takt, \
        max_width, max_height, bomb_count, barrier_count, bad_robot_move_path, bad_robot_map, digit_map, \
        flag_stop_score_time, flag_movie_bad_robot, flag_exploded_bad_robot, falg_end_level, flag_game_over, \
        takt_bad_robot, takt_end_level
    x_point_hero = 0
    y_point_hero = 0
    x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp, max_width, max_height = 0, 0, 0, 0, 0, 0
    bomb_count, barrier_count = 0, 0
    bad_robot_move_path = []
    bad_robot_map, digit_map = [[]], [[]]
    all_sprites.empty()
    tiles_group.empty()
    player_group.empty()
    bomb_group.empty()
    barrier_group.empty()
    tool_box_group.empty()
    bomb_box_group.empty()
    bad_robot_group.empty()
    detonation_group.empty()
    game_over_group.empty()
    takt = 0
    flag_stop_score_time = False
    flag_movie_bad_robot = True
    flag_exploded_bad_robot = False
    falg_end_level = False
    flag_game_over = False
    takt = 1
    takt_bad_robot = 0
    takt_end_level = 0


def game_over():
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.mixer.music.stop()
    #             terminate()
    #         elif event.type == pygame.KEYDOWN or \
    #                 event.type == pygame.MOUSEBUTTONDOWN:
    #             pygame.mixer.music.stop()
    #             return  # начинаем игру

    reset_level()
    end_screen()
    start_screen()


def start_new_level(number_level):
    list_file_name_level = ['map1.txt', 'map2.txt', 'map3.txt', 'map4.txt', 'map5.txt']
    file_name_level = list_file_name_level[number_level - 1]
    return file_name_level


def info_line():
    fon = pygame.transform.scale(load_image('info_line_fon.png'), (1200, 50))
    screen.blit(fon, (0, 650))
    font = pygame.font.Font(font_file_name, 25)
    bomb = pygame.transform.scale(load_image('bomb.png'), (40, 40))
    screen.blit(bomb, (15, 655))
    text_coord = 650
    string_rendered = font.render('(ctrl) Бомбы:', 1, pygame.Color('blue'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 50
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)

    barrier = pygame.transform.scale(load_image('wall.png'), (35, 35))
    screen.blit(barrier, (330, 657))
    string_rendered = font.render('(alt) Препятствия:', 1, pygame.Color('blue'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 365
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render('Уровень:', 1, pygame.Color('blue'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 750
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render('Баллы:', 1, pygame.Color('blue'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 970
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)


def info_line_update(wall_count, bomb_count, number_level):
    text_coord = 650
    font = pygame.font.Font(font_file_name, 27)

    text_bomb_count = str(bomb_count)
    string_rendered = font.render(text_bomb_count, 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 260
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)
    text_wall_count = str(wall_count)
    string_rendered = font.render(text_wall_count, 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 670
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)
    text_number_level = str(number_level)
    string_rendered = font.render(text_number_level, 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 910
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)
    text_score = str(score)
    string_rendered = font.render(text_score, 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 1090
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)


def load_level(filename):
    sound_level1 = 'data\sound_level1.mp3'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sound_level1)
    pygame.mixer.music.play()
    global max_width, max_height
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        # print(level_map)
    global x_point_hero, y_point_hero, digit_map, bad_robot_map, x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    max_height = len(level_map)
    print(max_width, max_height)
    load_map = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    print(load_map)
    digit_map = [[0] * (max_width) for _ in range(max_height)]
    bad_robot_map = [[0] * (max_width) for _ in range(max_height)]
    # print(digit_map)

    for j in range(max_width):
        for i in range(max_height):
            if load_map[i][j] == '.':
                digit_map[i][j] = 0
                bad_robot_map[i][j] = 0
            elif load_map[i][j] == '#':
                digit_map[i][j] = 1
                bad_robot_map[i][j] = 1
            elif load_map[i][j] == '@':
                digit_map[i][j] = 5
                bad_robot_map[i][j] = 0
                x_point_hero = j
                y_point_hero = i
                print('позиция героя из файла', x_point_hero, y_point_hero)
            elif load_map[i][j] == 'C':
                digit_map[i][j] = 7
                bad_robot_map[i][j] = 0
                x_point_comp = j
                y_point_comp = i
            elif load_map[i][j] == 'R':
                digit_map[i][j] = 6
                bad_robot_map[i][j] = 0
                x_point_bad_robot = j
                y_point_bad_robot = i
            elif load_map[i][j] == 'B':
                digit_map[i][j] = 8
                bad_robot_map[i][j] = 1
                x_point_bomb_box = j
                y_point_bomb_box = i
            elif load_map[i][j] == 'T':
                digit_map[i][j] = 4
                bad_robot_map[i][j] = 1
                x_point_tool_box = j
                y_point_tool_box = i

    # print(x_point_hero, y_point_hero)
    # print(digit_map)
    # print(digit_map)
    # print(load_map)
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

font_file_name = 'data\conthrax-sb.ttf'
tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('hex.png'),
    'comp': load_image('comp.png'),
    'box_bomb': load_image('box_bomb.png'),
    'tool_box': load_image('tool_box.png'),
    # 'bomb_image': load_image('bomb.png'),
}
computer_image = load_image('comp.png')
player_image = load_image('hero.png')
bad_robot_image = load_image('bad_robot.png')
box_bomb_image = load_image('box_bomb.png')
tool_box_image = load_image('tool_box.png')
bomb_image = load_image('bomb.png')
barrier_image = load_image('barrier.png')
image_boom = load_image('boom.png')
broken_barrier_sheet = load_image('broken_barrier_sheet.png')
bad_robot_sheet = load_image('bad_robot_sheet.png')
tile_width = tile_height = step_hero = 50
input_name_player = ''


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 0, tile_height * pos_y + 0)


class BadRobot(pygame.sprite.Sprite):
    bad_robot_sheet = load_image('bad_robot.png')
    image_boom = load_image('boom.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(bad_robot_group, all_sprites)
        self.frames = []
        self.cut_sheet(bad_robot_sheet, 3, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 0, tile_height * pos_y + 0)

    def boom(self):
        self.image = image_boom
        sound_exploded = 'data\sound_exploded.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(sound_exploded)
        pygame.mixer.music.play()

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update_broken_barrier(self, takt):
        print('update_broken_barrier', takt)
        self.cur_frame = takt
        print(self.cur_frame)
        self.image = self.frames[self.cur_frame]


class BombBox(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bomb_box_group, all_sprites)
        self.image = box_bomb_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 0, tile_height * pos_y + 0)


class Computer(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(computer_group, all_sprites)
        self.image = computer_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 0, tile_height * pos_y + 0)


class ToolBox(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tool_box_group, all_sprites)
        self.image = tool_box_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 0, tile_height * pos_y + 0)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # print(pos_x, pos_y)
        super().__init__(bomb_group, all_sprites)
        self.add(bomb_group)
        self.image = bomb_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 0, tile_height * pos_y + 0)


class Barrier(pygame.sprite.Sprite):
    barrier_boom_image = load_image('boom.png')

    def __init__(self, pos_x, pos_y):
        print(pos_x, pos_y)
        super().__init__(barrier_group, all_sprites)
        self.image = barrier_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 0, tile_height * pos_y + 0)

    def delite_barrier(self):
        # if self.rect.x == x_step_bad_robot * tile_width and self.rect.y == y_step_bad_robot * tile_height:
        self.image = self.barrier_boom_image


class BrokenBarrier(pygame.sprite.Sprite):
    broken_barrier_sheet = load_image('broken_barrier_sheet.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(barrier_group, all_sprites)
        self.frames = []
        self.cut_sheet(broken_barrier_sheet, 3, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 0, tile_height * pos_y + 0)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update_broken_barrier(self, takt):
        print('update_broken_barrier', takt)
        self.cur_frame = takt
        print(self.cur_frame)
        self.image = self.frames[self.cur_frame]


class Detonation(pygame.sprite.Sprite):
    fire = [load_image("boom.png")]
    for scale in (2, 3, 5):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(detonation_group, all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.rect_boom = self.rect.x - 50, self.rect.y - 50, 100, 100

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.rect_boom):
            self.kill()


def create_detonation(position):
    detonation_count = 150
    numbers = range(-10, 10)
    for _ in range(detonation_count):
        Detonation(position, random.choice(numbers), random.choice(numbers))


def check_step_set_hero(direction, install='еmpty'):
    print('вызов check_step_set_bomb ')
    if direction == 'L':
        delta_x, delta_y = -1, 0
    elif direction == 'R':
        delta_x, delta_y = 1, 0
    elif direction == 'U':
        delta_x, delta_y = 0, -1
    elif direction == 'D':
        delta_x, delta_y = 0, 1

    global x_point_hero, y_point_hero, digit_map, bad_robot_map, bomb_count, barrier_count
    print('шаг стрелкой', x_point_hero, y_point_hero)
    # print(digit_map)
    if 0 <= (y_point_hero + delta_y) < len(digit_map) and 0 <= (x_point_hero + delta_x) < len(digit_map[0]):
        if digit_map[y_point_hero + delta_y][x_point_hero + delta_x] == 4:
            tool_box_group.empty()
            barrier_count = 20
            digit_map[y_point_hero][x_point_hero] = 0
            x_point_hero += delta_x
            y_point_hero += delta_y
            print('после шага', x_point_hero, y_point_hero)
            digit_map[y_point_hero][x_point_hero] = 5
            bad_robot_map[y_point_hero][x_point_hero] = 0
            return True
        if digit_map[y_point_hero + delta_y][x_point_hero + delta_x] == 8:
            bomb_box_group.empty()
            bomb_count = 5
            digit_map[y_point_hero][x_point_hero] = 0
            x_point_hero += delta_x
            y_point_hero += delta_y
            print('после шага', x_point_hero, y_point_hero)
            digit_map[y_point_hero][x_point_hero] = 5
            bad_robot_map[y_point_hero][x_point_hero] = 0
            return True
        if digit_map[y_point_hero + delta_y][x_point_hero + delta_x]:
            return False
        else:
            if install == 'bomb':
                if bomb_count > 0:
                    digit_map[y_point_hero][x_point_hero] = 9
                    bomb_count -= 1
                    Bomb(x_point_hero, y_point_hero)
                else:
                    digit_map[y_point_hero][x_point_hero] = 0
                    bad_robot_map[y_point_hero][x_point_hero] = 0
            if install == 'barrier':
                if barrier_count > 0:
                    digit_map[y_point_hero][x_point_hero] = 3
                    barrier_count -= 1
                    bad_robot_map[y_point_hero][x_point_hero] = 1
                    Barrier(x_point_hero, y_point_hero)
                else:
                    digit_map[y_point_hero][x_point_hero] = 0
                    bad_robot_map[y_point_hero][x_point_hero] = 0
            if install == 'еmpty':
                digit_map[y_point_hero][x_point_hero] = 0
                bad_robot_map[y_point_hero][x_point_hero] = 0

            x_point_hero += delta_x
            y_point_hero += delta_y
            print('после шага', x_point_hero, y_point_hero)
            digit_map[y_point_hero][x_point_hero] = 5
            bad_robot_map[y_point_hero][x_point_hero] = 0
            return True


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                print(x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'C':
                Tile('comp', x, y)
                computer = Computer(x, y)
            elif level[y][x] == 'B':
                Tile('empty', x, y)
                # new_box_bmb =
                bomb_box_group.add(BombBox(x, y))
            elif level[y][x] == 'R':
                Tile('empty', x, y)
                new_bad_robot = BadRobot(x, y)
            elif level[y][x] == 'T':
                Tile('empty', x, y)
                # new_tool_box = ToolBox(x, y)
                # all_sprites.add(new_tool_box)
                # all_sprites.add(ToolBox(x, y))
                tool_box_group.add(ToolBox(x, y))

    # вернем игрока, а также размер поля в клетках
    return new_player, new_bad_robot, x, y


def has_path(x1, y1, x2, y2):
    d = get_distance(x1, y1)
    # print('дистанция в has_path', d)
    dist = d.get((x2, y2), -1)
    return dist >= 0


def get_distance(start_x_point, start_y_point):
    global max_width, max_height, bad_robot_map
    # print('bad robot map', bad_robot_map)
    # print('ширина высота поля', max_width, max_height)

    v = [(start_x_point, start_y_point)]
    d = {(start_x_point, start_y_point): 0}
    while len(v) > 0:
        x, y = v.pop(0)
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx * dy != 0:
                    continue
                if x + dx < 0 or x + dx >= max_width or y + dy < 0 or y + dy >= max_height:
                    continue
                # print(y + dy, x + dx)
                if bad_robot_map[y + dy][x + dx] == 0:
                    dn = d.get((x + dx, y + dy), -1)
                    if dn == -1:
                        d[(x + dx, y + dy)] = d[(x, y)] + 1
                        v.append((x + dx, y + dy))
    # print('дистанция - ', d)
    return d


def get_path(x1, y1, x2, y2):
    global max_width, max_height, bad_robot_move_path
    d = get_distance(x1, y1)
    v = x2, y2
    path = [v]
    while v != (x1, y1):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx * dy != 0 or (dx == 0 and dy == 0):
                    continue
                x = v[0]
                y = v[1]
                if x + dx < 0 or x + dx >= max_width or \
                        y + dy < 0 or y + dy >= max_height:
                    continue
                if d.get((x + dx, y + dy), -100) == d[v] - 1:
                    v = (x + dx, y + dy)
                    path.append(v)
    path.reverse()
    bad_robot_move_path = path[:]
    bad_robot_move_path.pop(0)
    # print('путь выхода - ', path)
    if len(path) > 1:
        pass
        # self.start_draw_path_ball = True

    return path[:]


FPS = 50
x_point_hero = 0
y_point_hero = 0
x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp, max_width, max_height = 0, 0, 0, 0, 0, 0
bomb_count, barrier_count = 0, 0
bad_robot_move_path = []
bad_robot_map, digit_map = [[]], [[]]
clock = pygame.time.Clock()

if __name__ == '__main__':
    # # global file_name_level
    # print('Введите имя файла уровня map1.txt, map2.txt, map3.txt:')
    # file_name_level = input()
    # if (file_name_level == 'map1.txt' or file_name_level == 'map2.txt'
    #         or file_name_level == 'map3.txt'):
    #     print('Начинаем игру!')
    # else:
    #     print('Неправильное имя файла, завершаем игру...')
    #     terminate()
    pygame.init()
    size = width, height = 1200, 700
    screen_rect = (0, 0, width, height)
    screen = pygame.display.set_mode(size)
    v = 50
    fps = 20
    start_screen()
    info_line()
    # основной персонаж
    player = None
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    barrier_group = pygame.sprite.Group()
    tool_box_group = pygame.sprite.Group()
    bomb_box_group = pygame.sprite.Group()
    bad_robot_group = pygame.sprite.Group()
    detonation_group = pygame.sprite.Group()
    computer_group = pygame.sprite.Group()
    game_over_group = pygame.sprite.Group()
    flag_movie_bad_robot = True
    flag_exploded_bad_robot = False
    number_level = 1
    score = 0
    falg_end_level = False
    flag_game_over = False
    flag_stop_score_time = False

    clock = pygame.time.Clock()
    pygame.display.set_caption('Космическая база.')
    size = width, height = 1200, 700
    screen = pygame.display.set_mode(size)
    player, bad_robot, level_x, level_y = generate_level(load_level(start_new_level(number_level)))
    takt = 1
    takt_bad_robot = 0
    takt_end_level = 0

    running = True
    while running:

        speed = v / fps
        clock.tick(fps)
        screen.fill((0, 0, 0))
        info_line()
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    print('нажата LEFT + CTRL')
                    if check_step_set_hero('L', 'bomb'):
                        player.rect.x -= step_hero
                elif event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_ALT:
                    if check_step_set_hero('L', 'barrier'):
                        player.rect.x -= step_hero
                elif event.key == pygame.K_LEFT:
                    print('нажата LEFT')
                    if check_step_set_hero('L'):
                        player.rect.x -= step_hero

                if event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    print('нажата R + CTRL')
                    if check_step_set_hero('R', 'bomb'):
                        player.rect.x += step_hero
                elif event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_ALT:
                    if check_step_set_hero('R', 'barrier'):
                        player.rect.x += step_hero
                elif event.key == pygame.K_RIGHT:
                    print('нажата R')
                    if check_step_set_hero('R'):
                        player.rect.x += step_hero

                if event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    print('нажата UP + CTRL')
                    if check_step_set_hero('U', 'bomb'):
                        player.rect.y -= step_hero
                elif event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_ALT:
                    if check_step_set_hero('U', 'barrier'):
                        player.rect.y -= step_hero
                elif event.key == pygame.K_UP:
                    print('нажата UP')
                    if check_step_set_hero('U'):
                        player.rect.y -= step_hero

                if event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    print('нажата DOWN + CTRL')
                    if check_step_set_hero('D', 'bomb'):
                        player.rect.y += step_hero
                elif event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_ALT:
                    if check_step_set_hero('D', 'barrier'):
                        player.rect.y += step_hero
                elif event.key == pygame.K_DOWN:
                    print('нажата DOWN')
                    if check_step_set_hero('D'):
                        player.rect.y += step_hero

                if event.key == pygame.K_d:
                    print('нажата клавиша d')
                    # all_sprites.remove(new_tool_box)
                    # tool_box_group.remove(new_tool_box)
                    print(tool_box_group)
                    tool_box_group.empty()
                    print(tool_box_group)
                    # all_sprites.remove(sprite)
                    # new_tool_box.kill

                player_group.draw(screen)
                bomb_group.draw(screen)
                barrier_group.draw(screen)

            if event.type == pygame.QUIT:
                running = False

        # if start_find_path:
        # print(x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp)
        # print(has_path(x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp))
        if takt - takt_bad_robot > 20 and flag_movie_bad_robot:
            # bad_robot_move_path = []
            if has_path(x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp):
                path = get_path(x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp)

                # for step in path[1:]:
                #     for j in range(max_height):
                #         for i in range(max_width):
                #             x_step, y_step = step
                #             if x_step == i and y_step == j:
                #                 pass
                #                 # Bomb(i,j)

            if len(bad_robot_move_path) > 0:
                x_step_bad_robot, y_step_bad_robot = bad_robot_move_path[0]
                if bad_robot_map[y_step_bad_robot][x_step_bad_robot] == 0:
                    bad_robot_stop_takt = 0
                    x_step_bad_robot, y_step_bad_robot = bad_robot_move_path.pop(0)
                    bad_robot_map[y_step_bad_robot][x_step_bad_robot] = 6
                    digit_map[y_step_bad_robot][x_step_bad_robot] = 6
                    # print('bad robot coord: ', x_point_bad_robot, y_point_bad_robot)
                    # print(bad_robot_map)
                    bad_robot_map[y_point_bad_robot][x_point_bad_robot] = 0
                    digit_map[y_point_bad_robot][x_point_bad_robot] = 0
                    x_point_bad_robot, y_point_bad_robot = x_step_bad_robot, y_step_bad_robot
                    bad_robot.rect.x = x_point_bad_robot * tile_width
                    bad_robot.rect.y = y_point_bad_robot * tile_height

                    if pygame.sprite.spritecollideany(bad_robot, player_group) or pygame.sprite.spritecollideany(
                            bad_robot, computer_group):
                        # GAME OVER
                        sprite_game_over = pygame.sprite.Sprite()
                        # определим его вид
                        sprite_game_over.image = load_image("game_over.png")
                        # и размеры
                        sprite_game_over.rect = sprite_game_over.image.get_rect()
                        sprite_game_over.rect.x = 50
                        sprite_game_over.rect.y = 200
                        # добавим спрайт в группу
                        game_over_group.add(sprite_game_over)
                        sound_game_over = 'data\game_over.mp3'
                        pygame.init()
                        pygame.mixer.init()
                        pygame.mixer.music.load(sound_game_over)
                        pygame.mixer.music.play()
                        flag_movie_bad_robot = False
                        falg_end_level = False
                        flag_game_over = True
                        takt_end_level = takt
                        if number_level == 1:
                            score = 0

                    if pygame.sprite.spritecollideany(bad_robot, bomb_group):
                        bad_robot.boom()
                        flag_exploded_bad_robot = True
                        flag_movie_bad_robot = False
                        position_boom = bad_robot.rect.x, bad_robot.rect.y
                        create_detonation(position_boom)
                        # number_level += 1
                        takt_end_level = takt
                        # flag_movie_bad_robot = True
                        falg_end_level = True
                        flag_stop_score_time = True

                    if len(bad_robot_move_path) == 0:
                        print('GAME OVER!')

                        # x_point_bad_robot, y_point_bad_robot = x, y
                        # self.start_move_ball = False
                # self.ticks = 0
                else:
                    print('Bad Robot STOP - ', bad_robot_stop_takt)
                    if bad_robot_stop_takt == 0:
                        broken_barrier = BrokenBarrier(x_step_bad_robot, y_step_bad_robot)
                        bad_robot_stop_takt += 1
                        bad_robot.update_broken_barrier(bad_robot_stop_takt)
                    else:
                        bad_robot_stop_takt += 1
                        if bad_robot_stop_takt < 6:
                            broken_barrier.update_broken_barrier(bad_robot_stop_takt)
                            bad_robot.update_broken_barrier(bad_robot_stop_takt)
                    if bad_robot_stop_takt > 5:
                        bad_robot_map[y_point_bad_robot][x_point_bad_robot] = 0
                        digit_map[y_point_bad_robot][x_point_bad_robot] = 0
                        x_step_bad_robot, y_step_bad_robot = bad_robot_move_path.pop(0)
                        bad_robot_map[y_step_bad_robot][x_step_bad_robot] = 0
                        digit_map[y_step_bad_robot][x_step_bad_robot] = 0
                        x_point_bad_robot, y_point_bad_robot = x_step_bad_robot, y_step_bad_robot
                        bad_robot.rect.x = x_point_bad_robot * tile_width
                        bad_robot.rect.y = y_point_bad_robot * tile_height
                        bad_robot_map[y_point_bad_robot][x_point_bad_robot] = 6
                        digit_map[y_point_bad_robot][x_point_bad_robot] = 6
                        bad_robot_stop_takt = 0
                        bad_robot.update_broken_barrier(bad_robot_stop_takt)
                        bad_robot_group.draw(screen)
                        # barrier_group.delite_barrier()
                        all_sprites.draw(screen)
            takt_bad_robot = takt

        if takt - takt_end_level > 70 and falg_end_level:
            pygame.init()
            size = width, height = 1200, 700
            screen_rect = (0, 0, width, height)
            screen = pygame.display.set_mode(size)
            v = 50
            fps = 20
            info_line()
            reset_level()
            player = None
            screen = pygame.display.set_mode(size)
            number_level += 1
            player, bad_robot, level_x, level_y = generate_level(
                load_level(start_new_level(number_level)))
            flag_movie_bad_robot = True
            falg_end_level = False

        if takt - takt_end_level > 70 and flag_game_over:
            game_over()
            number_level = 1
            player, bad_robot, level_x, level_y = generate_level(load_level(start_new_level(number_level)))
            flag_game_over = False
            flag_movie_bad_robot = True

        # print(path)
        info_line_update(barrier_count, bomb_count, number_level)
        all_sprites.draw(screen)
        all_sprites.update()
        tiles_group.draw(screen)
        bomb_group.draw(screen)
        barrier_group.draw(screen)
        player_group.draw(screen)
        tool_box_group.draw(screen)
        bomb_box_group.draw(screen)
        bad_robot_group.draw(screen)
        detonation_group.draw(screen)
        game_over_group.draw(screen)
        pygame.display.flip()
        takt += 1
        if not flag_stop_score_time:
            #score = int((500 / takt) * (bomb_count / 5) * (barrier_count / 20) * 100)
            score = int((500 / takt) * (bomb_count / 5) * (barrier_count / 20) * 100)
        if takt > 10000:
            takt = 0

    pygame.quit()
