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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        # print(level_map)
    global x_point_hero, y_point_hero, digit_map
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    max_highth = len(level_map)
    print(max_width, max_highth)
    load_map = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    print(load_map)
    digit_map = [[0] * (max_width) for _ in range(max_highth)]
    # print(digit_map)

    for j in range(max_width):
        for i in range(max_highth):
            if load_map[i][j] == '.':
                digit_map[i][j] = 0
            elif load_map[i][j] == '#':
                digit_map[i][j] = 1
            elif load_map[i][j] == '@':
                digit_map[i][j] = 5
                x_point_hero = j
                y_point_hero = i
            elif load_map[i][j] == 'C':
                digit_map[i][j] = 7
                x_point_comp = j
                y_point_comp = i
            elif load_map[i][j] == 'R':
                digit_map[i][j] = 6
                x_point_bad_robot = j
                y_point_bad_robot = i
            elif load_map[i][j] == 'B':
                digit_map[i][j] = 8
                x_point_box_bomb = j
                y_point_box_bomb = i
            elif load_map[i][j] == 'T':
                digit_map[i][j] = 4
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
    'bomb_image': load_image('bomb.png'),
}
player_image = load_image('hero.png')
bad_robot_image = load_image('bad_robot.png')
box_bomb_image = load_image('box_bomb.png')
tool_box_image = load_image('tool_box.png')
bomb_image = load_image('bomb.png')
tile_width = tile_height = step_hero = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


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


class BoxBomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = box_bomb_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 0, tile_height * pos_y + 0)


class ToolBox(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = tool_box_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 0, tile_height * pos_y + 0)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bomb_group, all_sprites)
        self.image = bomb_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 0, tile_height * pos_y + 0)


def check_step(delta_x, delta_y):
    # print(delta_x, delta_y)
    global x_point_hero, y_point_hero, digit_map
    # print(x_point_hero, y_point_hero)
    # print(digit_map)
    if 0 <= (y_point_hero + delta_y) < len(digit_map) and 0 <= (x_point_hero + delta_x) < len(digit_map[0]):
        if digit_map[y_point_hero + delta_y][x_point_hero + delta_x]:
            return False
        else:
            digit_map[y_point_hero][x_point_hero] = 0
            x_point_hero += delta_x
            y_point_hero += delta_y
            digit_map[y_point_hero][x_point_hero] = 5
            return True


def check_step_set_bomb(delta_x, delta_y):
    # print(delta_x, delta_y)
    global x_point_hero, y_point_hero, digit_map
    # print(x_point_hero, y_point_hero)
    # print(digit_map)
    if 0 <= (y_point_hero + delta_y) < len(digit_map) and 0 <= (x_point_hero + delta_x) < len(digit_map[0]):
        if digit_map[y_point_hero + delta_y][x_point_hero + delta_x]:
            return False
        else:
            digit_map[y_point_hero][x_point_hero] = 8
            new_bomb = Bomb(y_point_hero, x_point_hero)
            x_point_hero += delta_x
            y_point_hero += delta_y
            digit_map[y_point_hero][x_point_hero] = 5


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
                new_player = Player(x, y)
            elif level[y][x] == 'C':
                Tile('comp', x, y)
            elif level[y][x] == 'B':
                Tile('empty', x, y)
                new_box_bomb = BoxBomb(x, y)
            elif level[y][x] == 'R':
                Tile('empty', x, y)
                new_bad_robot = BadRobot(x, y)
            elif level[y][x] == 'T':
                Tile('empty', x, y)
                new_tool_box = ToolBox(x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, new_bad_robot, x, y


FPS = 50
x_point_hero = 0
y_point_hero = 0
digit_map = [[]]
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
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    v = 50
    fps = 20
    start_screen()
    # основной персонаж
    player = None
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    pygame.display.set_caption('Перемещение героя. Дополнительные уровни')
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    player, bad_robot, level_x, level_y = generate_level(load_level(file_name_level))

    running = True
    while running:
        speed = v / fps
        clock.tick(fps)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and check_step(-1, 0):
                    player.rect.x -= step_hero
                if event.key == pygame.K_RIGHT and check_step(1, 0):
                    player.rect.x += step_hero
                if event.key == pygame.K_UP and check_step(0, -1):
                    player.rect.y -= step_hero
                if event.key == pygame.K_DOWN and check_step(0, 1):
                    player.rect.y += step_hero
                if (event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_CTRL and
                        check_step_set_bomb(-1, 0)):
                    print('Left и CTRL')
                    # new_bomb = Bomb(x_point_hero, y_point_hero)
                    bad_robot.rect.x -= step_hero

                if (event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_CTRL and
                        check_step_set_bomb(1, 0)):
                    print('Right и CTRL')
                    # new_bomb = Bomb(x_point_hero, y_point_hero)
                    bad_robot.rect.x += step_hero

                if (event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_CTRL and
                        check_step_set_bomb(0, -1)):
                    print('UP и CTRL')
                    # new_bomb = Bomb(x_point_hero, y_point_hero)
                    bad_robot.rect.y -= step_hero

                if (event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_CTRL and
                        check_step_set_bomb(0, 1)):
                    print('DOWN и CTRL')
                    # new_bomb = Bomb(x_point_hero, y_point_hero)
                    bad_robot.rect.y += step_hero

                if event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_ALT:
                    print('Left и ALT')
                if event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_ALT:
                    print('Right и ALT')
                if event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_ALT:
                    print('UP и ALT')
                if event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_ALT:
                    print('DOWN и ALT')

            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        all_sprites.update()
        tiles_group.draw(screen)
        player_group.draw(screen)
        bomb_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
