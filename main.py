import os
import sys
import pygame


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
    pygame.display.set_caption('Перемещение героя. Дополнительные уровни')
    intro_text = ["Программа 'Перемещение героя'",
                  "Управление героем: клавиши:",
                  "Влево, Вправо, Вверх, Вниз",
                  "для загрузки уровня нажмите Enter",
                  ]

    fon = pygame.transform.scale(load_image('start_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 350
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        pygame.display.flip()
        clock.tick(FPS)


def info_line():
    fon = pygame.transform.scale(load_image('info_line_fon.png'), (1200, 50))
    screen.blit(fon, (0, 800))
    font = pygame.font.Font(None, 30)
    bomb = pygame.transform.scale(load_image('bomb.png'), (30, 30))
    screen.blit(bomb, (70, 810))
    text_coord = 810
    string_rendered = font.render('(ctrl) Бомбы:', 1, pygame.Color('blue'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 100
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)

    barrier = pygame.transform.scale(load_image('wall.png'), (30, 30))
    screen.blit(barrier, (360, 810))
    string_rendered = font.render('(alt) Препятствия:', 1, pygame.Color('blue'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 400
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)



def info_line_update(wall_count, bomb_count):
    text_coord = 805
    font = pygame.font.Font(None, 40)
    text_bomb_count = str(bomb_count)
    string_rendered = font.render(text_bomb_count, 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 240
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)
    text_wall_count = str(wall_count)
    string_rendered = font.render(text_wall_count, 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 590
    intro_rect.top = text_coord + 10
    screen.blit(string_rendered, intro_rect)



def load_level(filename):
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


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('hex.png'),
    'comp': load_image('comp.png'),
    'box_bomb': load_image('box_bomb.png'),
    'tool_box': load_image('tool_box.png'),
    # 'bomb_image': load_image('bomb.png'),
}
player_image = load_image('hero.png')
bad_robot_image = load_image('bad_robot.png')
box_bomb_image = load_image('box_bomb.png')
tool_box_image = load_image('tool_box.png')
bomb_image = load_image('bomb.png')
barrier_image = load_image('barrier.png')
tile_width = tile_height = step_hero = 50


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
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = bad_robot_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 0, tile_height * pos_y + 0)


class BombBox(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bomb_box_group, all_sprites)
        self.image = box_bomb_image
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
        self.image = bomb_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 0, tile_height * pos_y + 0)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        print(pos_x, pos_y)
        super().__init__(barrier_group, all_sprites)
        self.image = barrier_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 0, tile_height * pos_y + 0)


# def check_step(direction):
#     print('вызов check_step')
#     if direction == 'L':
#         delta_x, delta_y = -1, 0
#     elif direction == 'R':
#         delta_x, delta_y = 1, 0
#     elif direction == 'U':
#         delta_x, delta_y = 0, -1
#     elif direction == 'D':
#         delta_x, delta_y = 0, 1
#
#     global x_point_hero, y_point_hero, digit_map
#     print('шаг стрелкой', x_point_hero, y_point_hero)
#     # print(digit_map)
#     if 0 <= (y_point_hero + delta_y) < len(digit_map) and 0 <= (x_point_hero + delta_x) < len(digit_map[0]):
#         if digit_map[y_point_hero + delta_y][x_point_hero + delta_x] != 0:
#             return False
#         if digit_map[y_point_hero + delta_y][x_point_hero + delta_x] == 0:
#             digit_map[y_point_hero][x_point_hero] = 0
#             print('до шага', x_point_hero, y_point_hero)
#             x_point_hero += delta_x
#             y_point_hero += delta_y
#             print('после шага', x_point_hero, y_point_hero)
#             digit_map[y_point_hero][x_point_hero] = 5
#             return True


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
                    bad_robot_map[y_point_hero][x_point_hero] = 3
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
board = [[]]
clock = pygame.time.Clock()

if __name__ == '__main__':
    # global file_name_level
    print('Введите имя файла уровня map1.txt, map2.txt, map3.txt:')
    file_name_level = input()
    if (file_name_level == 'map1.txt' or file_name_level == 'map2.txt'
            or file_name_level == 'map3.txt'):
        print('Начинаем игру!')
    else:
        print('Неправильное имя файла, завершаем игру...')
        terminate()
    pygame.init()
    size = width, height = 1200, 850
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

    clock = pygame.time.Clock()
    pygame.display.set_caption('Перемещение героя. Дополнительные уровни')
    size = width, height = 1200, 850
    screen = pygame.display.set_mode(size)
    player, bad_robot, level_x, level_y = generate_level(load_level(file_name_level))

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
        if has_path(x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp):
            path = get_path(x_point_bad_robot, y_point_bad_robot, x_point_comp, y_point_comp)

            for step in path[1:]:
                for j in range(max_height):
                    for i in range(max_width):
                        x_step, y_step = step
                        if x_step == i and y_step == j:
                            pass
                            # Bomb(i,j)

        # print(path)
        info_line_update(barrier_count, bomb_count)
        all_sprites.draw(screen)
        all_sprites.update()
        tiles_group.draw(screen)
        player_group.draw(screen)
        bomb_group.draw(screen)
        barrier_group.draw(screen)
        tool_box_group.draw(screen)
        bomb_box_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
