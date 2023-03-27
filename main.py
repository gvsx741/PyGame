import pygame
from random import randint


class Egg(pygame.sprite.Sprite):
    def __init__(self, x, speed, surf, score, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf  # граф. изобр.
        self.rect = self.image.get_rect(center=(x, -35))
        self.speed = speed #скорость спрайта
        self.score = score #кол-во очков за определенноё очко
        self.add(group)

    def update(self, *args):
        if self.rect.y < args[0]:
            self.rect.y += self.speed
        else:
            self.kill()


pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)
pygame.display.set_caption('Горностаєв В.С.')  # Заголовок окна
pygame.mixer.music.load("sounds/music.mp3") #добавил фоновую музыку
pygame.mixer.music.play(-1)

W, H = 1000, 570  # задаём размеры окна

sc = pygame.display.set_mode((W, H))

clock = pygame.time.Clock()
FPS = 60  # кол-во кадров в сек.

score = pygame.image.load('images/score_fon.png').convert_alpha()
f = pygame.font.SysFont('arial', 30)  # Шрифт и размер набранных очков

aim = pygame.image.load('images/aim.png').convert_alpha()  # загружаем прицел
t_rect = aim.get_rect(centerx=W // 2, bottom=H - 30)  # первоначальные координаты прицела

Eggs_data = ({'path': 'Egg1.png', 'score': 100}, {'path': 'Egg2.png', 'score': 150}, {'path': 'Egg3.png', 'score': 200})
Eggs_surf = [pygame.image.load('images/' + data['path']).convert_alpha() for data in Eggs_data]


def createEgg(group):
    indx = randint(0, len(Eggs_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)

    return Egg(x, speed, Eggs_surf[indx], Eggs_data[indx]['score'], group)


game_score = 0

def colliteEgg():  # функция для подсчёта очков и расчёт столкновений
    global game_score
    for Egg in Eggs: #ну а чуть ниже у нас проверка на нажатую кнопку и на столкновение
        if t_rect.collidepoint(Egg.rect.center) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game_score += Egg.score
            Egg.kill()


Eggs = pygame.sprite.Group()

bg = pygame.image.load('images/FERMA.png').convert()

createEgg(Eggs)  # создание падающих яиц

pygame.mouse.set_visible(False)  # убираем видимость мышки

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            createEgg(Eggs)

    pos = pygame.mouse.get_pos()  # тут мы задаём координаты прицела с помощью координат мышки
    t_rect.x = pos[0]
    t_rect.y = pos[1]

    colliteEgg()

    sc.blit(bg, (0, 0))
    sc.blit(score, (0, 0))
    sc_text = f.render(str(game_score), 1, (94, 138, 14))
    sc.blit(sc_text, (70, 10))

    Eggs.draw(sc)
    sc.blit(aim, t_rect)
    pygame.display.update()

    clock.tick(FPS)  # Ограничеваем скорость выполнения основного цыкла передавая значение
    # с макс. допустимой скоростью выполнения в сек.

    Eggs.update(H)
