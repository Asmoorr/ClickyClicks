import random
import sys
import os
import pygame

FPS = 144
SIZE = WIDTH, HEIGHT = 1600, 900
CLOCK = pygame.time.Clock()

WHITE = (220, 220, 220)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (224, 224, 224)

MONTSERRAT_BLACK = 'data/montserrat_black.ttf'

AUTOMONEY = pygame.USEREVENT + 1

MONG_MULTIPLY = 1.5
CLICK_UPGRADE_COST_MULTIPLY = 2.5
AUTO_MULTIPLY = 1.5
AUTO_UPGRADE_COST_MULTIPLY = 2

SOUNDS = dict(
    click='data/click.mp3',
    upgrade='data/upgrade.mp3'
)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


os.environ['SDL_VIDEO_CENTERED'] = '1'
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.transform.scale(load_image('main_background.png'), (WIDTH, HEIGHT))
pygame.display.set_caption("Clicky clicks")
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
pygame.mixer.music.load('data/background_1.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()


class Coin(pygame.sprite.Sprite):
    image = load_image("coin_dark.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Coin.image
        self.image = pygame.transform.smoothscale(self.image, (250, 250))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 + 340, 400

    def update(self, event):
        if (
                event.type == pygame.MOUSEBUTTONDOWN
                and self.rect.collidepoint(event.pos)
                and main.coins >= main.click_upgrade_cost
        ):
            main.sound_effects['upgrade'].play()
            main.coins -= main.click_upgrade_cost
            main.mong *= MONG_MULTIPLY
            main.click_upgrade_cost *= CLICK_UPGRADE_COST_MULTIPLY


# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error


# render text
class Number(pygame.sprite.Sprite):
    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error

    def __init__(self, *group):
        super().__init__(*group)
        self.myfont = pygame.font.SysFont(MONTSERRAT_BLACK, 40)
        self.label = self.myfont.render(f'+{main.mong:.2f}', True, LIGHT_GREY)
        self.image = self.label
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pygame.mouse.get_pos()

    def update(self):
        if self.rect.y < 0:
            self.kill()

        self.rect.y -= 1


class Button(pygame.sprite.Sprite):
    image = load_image('pizza.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Button.image
        self.image = pygame.transform.smoothscale(self.image, (200, 150))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - 120, 160

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            main.sound_effects['click'].play()
            main.coins += main.mong
            FallingPizza(falling_pizza_group)
            Number(number_group)


class FallingPizza(pygame.sprite.Sprite):
    image = load_image('pizza_dark.png')

    def __init__(self, *group):
        super().__init__(*group)

        self.image = FallingPizza.image
        self.image = pygame.transform.smoothscale(self.image, (100, 75))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.random() * WIDTH, 0
        self.speed = random.randint(1, 4)

    def update(self):
        if self.rect.y > HEIGHT:
            self.kill()

        self.rect.y += self.speed


class Chef_one(pygame.sprite.Sprite):
    image = load_image("chef_1_dark.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Chef_one.image
        self.image = pygame.transform.smoothscale(self.image, (250, 320))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - 350, HEIGHT - 330

    def update(self, event):
        if (
                event.type == pygame.MOUSEBUTTONDOWN
                and self.rect.collidepoint(event.pos)
                and main.coins >= main.auto_one_upgrade_cost
        ):
            main.sound_effects['upgrade'].play()
            main.coins -= main.auto_one_upgrade_cost
            main.auto_coins *= AUTO_MULTIPLY
            main.auto_one_upgrade_cost *= AUTO_UPGRADE_COST_MULTIPLY


class Chef_two(pygame.sprite.Sprite):
    image = load_image("chef_2_dark.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Chef_two.image
        self.image = pygame.transform.smoothscale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - 700, HEIGHT - 320

    def update(self, event):
        if (
                event.type == pygame.MOUSEBUTTONDOWN
                and self.rect.collidepoint(event.pos)
                and main.coins >= main.auto_two_upgrade_cost
        ):
            main.sound_effects['upgrade'].play()
            main.coins -= main.auto_two_upgrade_cost
            main.auto_coins *= AUTO_MULTIPLY
            main.auto_two_upgrade_cost *= AUTO_UPGRADE_COST_MULTIPLY


def draw_text(text, text_color, x, y, font_size) -> None:
    font = pygame.font.Font(MONTSERRAT_BLACK, font_size)
    text = font.render(text, True, text_color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    main_screen.blit(text, text_rect)


class Main:
    def __init__(self):
        pygame.mixer.music.load('data/background_2.mp3')
        pygame.mixer.music.play()
        self.auto_two_upgrade_cost = 5000
        self.click_upgrade_cost = 10
        self.auto_one_upgrade_cost = 50
        self.auto_coins = 5
        self.coins = 0
        self.mong = 1
        self.sound_effects = {
            name: pygame.mixer.Sound(sound)
            for name, sound in SOUNDS.items()}

    def rendering(self):  # sourcery skip: simplify-fstring-formatting
        pygame.time.set_timer(AUTOMONEY, 1000)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pizza_group.update(event)
                    coin_group.update(event)
                    chef_two_group.update(event)
                    chef_one_group.update(event)

                if event.type == AUTOMONEY:
                    main.auto_miner()

            main_screen.blit(background, (0, 0))
            # main_screen.fill(WHITE)

            falling_pizza_group.update()
            falling_pizza_group.draw(main_screen)

            draw_text("Clicky Clicks", WHITE, WIDTH // 2 - 20, 100, 50)
            draw_text(f"you have {f'{self.coins:.2f}'} coins", WHITE, WIDTH - 130, 50, 20)
            draw_text(f"upgrade clicker {self.click_upgrade_cost:.2f}", WHITE, WIDTH // 2 + 440, 380, 20)
            draw_text(f"common cooker {self.auto_one_upgrade_cost:.2f}", WHITE, WIDTH // 2 - 230, HEIGHT - 350, 20)
            draw_text(f"professional chef cooker {self.auto_two_upgrade_cost:.2f}", WHITE, WIDTH // 2 - 570,
                      HEIGHT - 350, 20)

            chef_one_group.draw(main_screen)
            chef_two_group.draw(main_screen)

            pizza_group.draw(main_screen)
            coin_group.draw(main_screen)

            number_group.update()
            number_group.draw(main_screen)

            pygame.display.flip()
            CLOCK.tick(FPS)

    def auto_miner(self) -> None:
        self.coins = self.coins + self.auto_coins


def terminate() -> None:
    pygame.quit()
    sys.exit()


def start_screen() -> None:
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    intro_text = ["Clicky clicks".upper(), "",
                  "Правила игры",
                  "Вы можете зарабатывать очки нажатием на кусочек пиццы.",
                  "Вы можете купить автоматическую добычу очков при их достаточном количестве.",
                  "Вы можете купить улучшение для добычи очков нажатием на соответствующую кнопку.",
                  "Цель игры - набрать как можно больше очков.",
                  "Удачи!"]

    background = pygame.transform.scale(load_image('start_background.png'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(MONTSERRAT_BLACK, 30)
    text_coord = 50

    pygame.mixer.music.play(-1, 0.0)

    for line in intro_text:
        string_rendered = font.render(line, True, WHITE)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                return
        pygame.display.flip()
        CLOCK.tick(FPS)


def rectangle(display, color, x, y, w, h) -> None:
    pygame.draw.rect(display, color, (x, y, w, h))


if __name__ == '__main__':
    start_screen()

    pizza_group = pygame.sprite.Group()
    Button(pizza_group)

    chef_one_group = pygame.sprite.Group()
    Chef_one(chef_one_group)

    chef_two_group = pygame.sprite.Group()
    Chef_two(chef_two_group)

    coin_group = pygame.sprite.Group()
    Coin(coin_group)

    falling_pizza_group = pygame.sprite.Group()

    number_group = pygame.sprite.Group()

    main = Main()
    main.rendering()

    terminate()
