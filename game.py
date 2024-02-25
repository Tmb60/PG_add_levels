import pygame
import os
import sys
from pygame.locals import *


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    try:
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except FileNotFoundError:
        raise FileNotFoundError("Файл с уровнем не найден.")


def start_screen(size, screen):
    pygame.display.set_caption('Перемещение игрока. Дополнительные уровни')
    text1 = "Для старта игры выберите карту уровня"
    text2 = "используйте клавиши-стрелки вверх/вниз и Enter"
    fon = pygame.transform.scale(load_image('fon.png'), size)
    fon.set_alpha(220)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 28)
    head = font.render(text1, 1, 'red')
    screen.blit(head, (7, size[1] - 30 * 2))
    head = font.render(text2, 1, 'red')
    screen.blit(head, (7, size[1] - 30))
    menu_items = ["1. Стандартный уровень\
                 (карта level1.txt)",
                  "2. Продвинутый уровень\
                    (карта level2.txt)",
                  "3. Не для слабаков          \
                     (карта level3.txt) "]
    selected_item = 0

    def draw_menu():
        text_coord = 30
        for i, item in enumerate(menu_items):
            string_rendered = font.render(item, 1, 'black' if i == selected_item else 'darkslategray')
            menu_rect = string_rendered.get_rect()
            text_coord += 15
            menu_rect.top = text_coord
            menu_rect.x = 7
            text_coord += menu_rect.height
            screen.blit(string_rendered, menu_rect)

    running = True
    while running:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    try:
                        return load_level(input(f"Введите имя файла для уровня {selected_item + 1}: "))  # начинаем игру
                    except FileNotFoundError as e:
                        print(e)
                        running = False
        pygame.display.flip()
    terminate()


def main():
    player = None
    level = None
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_images = {'wall': load_image('box.png'),
                   'empty': load_image('grass.png')
                   }
    player_image = load_image('mario.png')

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
                tile_width * pos_x + 5, tile_height * pos_y + 2)

        def move(self, dx, dy):
            new_x = self.rect.x + dx
            new_y = self.rect.y + dy
            if 0 <= new_y // tile_height < len(level) and 0 <= new_x // tile_width < len(level[0]):
                if level[new_y // tile_height][new_x // tile_width] != '#':
                    self.rect.x = new_x
                    self.rect.y = new_y

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
        return new_player, x, y

    pygame.init()
    FPS = 50
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    level = start_screen(size, screen)
    stepx = tile_width = width // len(level[0])
    stepy = tile_height = height // len(level)
    player, level_x, level_y = generate_level(level)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.move(-stepx, 0)
                elif event.key == K_RIGHT:
                    player.move(stepx, 0)
                elif event.key == K_UP:
                    player.move(0, -stepy)
                elif event.key == K_DOWN:
                    player.move(0, stepy)

        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
