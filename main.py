import pygame
import random
from math import hypot

pygame.init()# підключає модулі


SIZE = (1000,700)
FPS = 60
WHITE = (255, 255, 255)# кортеж
GREEN = (0,255,0)

screen = pygame.display.set_mode(SIZE)# створення екрана з заданими параметрами
clock = pygame.time.Clock()#таймер

class Eat:
    def __init__(self, x,y,r,c):
        self.x = x 
        self.y = y
        self.radius = r
        self.color = c
    
    def check_collision(self, player_x, player_y, player_r):#перевірка взаємодії гравця з їжею
        dx = self.x - player_x
        dy = self.y - player_y
        return hypot(dx, dy) <= self.radius + player_r

eats = [Eat(random.randint(-2000,SIZE[0] + 2000),#x
            random.randint(-2000,SIZE[1] + 2000),#y
            10,#radius
            (random.randint(0,255),#red
             random.randint(0,255),#green
             random.randint(0,255)#blut
             )) for _ in range(300)]

list_ball = [0,0,20]
running = True
while running:
    screen.fill(WHITE)#зафарбувати екран
    to_remove = []
    for eat in eats:
        if eat.check_collision(list_ball[0], list_ball[1],list_ball[2]):
            to_remove.append(eat)
            list_ball[2] += int(eat.radius * 0.2)
        else:
            sx = int((eat.x - list_ball[0] + SIZE[0]//2))
            sy = int((eat.y - list_ball[1]) + SIZE[1] // 2)
            pygame.draw.circle(screen, eat.color, (sx,sy), eat.radius)

    scale = max(0.3 , min(50/list_ball[2], 1.5))
    pygame.draw.circle(screen, GREEN, (SIZE[0] //2, SIZE[1] //2), int(list_ball[2] * scale))#намалювали гравця
    
    for eat in to_remove:# видаляємо їжу, що з'їли
        eats.remove(eat)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:list_ball[1] -= 15
    if keys[pygame.K_s]:list_ball[1] += 15
    if keys[pygame.K_a]:list_ball[0] -= 15
    if keys[pygame.K_d]:list_ball[0] += 15

    
    for e in pygame.event.get():#перебираємо усі події
        if e.type == pygame.QUIT:#якщо під час гри людина клікнула на хрестик
            running = False
    pygame.display.update()#оновлення екрану
    clock.tick(FPS)# частота оновлення екрану


quit()#закрити екран

