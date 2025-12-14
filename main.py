import pygame
import random
from math import hypot
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

#
HOST= 'localhost'
PORT = 8080
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((HOST, PORT))
my_data = list(map(int, sock.recv(1024).decode().strip().split(',') ))
my_id = my_data[0]
list_ball = my_data[1:]
sock.setblocking(False)
#

pygame.init()# підключає модулі


SIZE = (1000,700)
FPS = 60
WHITE = (255, 255, 255)# кортеж
GREEN = (0,255,0)
#
running = True
all_players = []
lose = False
f = pygame.font.SysFont('Monospace', 45)
#
def  receive_data():
    global all_players, running, lose
    while running:
        try:
            data = sock.recv(4096).decode().strip()
            if data == 'LOSE':
                lose  = True
            elif data:
                parts = data.strip('|').split('|')
                all_players = [list(map(int, p.split(','))) for p in parts if len(p.split(','))==4]
        except:
            pass
Thread(target=receive_data, daemon=True).start()
#

screen = pygame.display.set_mode(SIZE)# створення екрана з заданими параметрами
clock = pygame.time.Clock()#таймер

class Eat:
    def __init__(self, x,y,r,c):
        self.x = x 
        self.y = y
        self.radius = r
        self.color = c
    
    def check_collision(self, player_x, player_y, player_r):
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

#list_ball = [0,0,20]
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
    
    for eat in to_remove:
        eats.remove(eat)

    if not lose:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:list_ball[1] -= 15
        if keys[pygame.K_s]:list_ball[1] += 15
        if keys[pygame.K_a]:list_ball[0] -= 15
        if keys[pygame.K_d]:list_ball[0] += 15
        
        try:
            msg = f'{my_id}, {list_ball[0], list_ball[1], list_ball[2]}'
            sock.send(msg.encode())
        except:
            pass

    if lose:
        t = f.render('U Lose!', True, (240, 10,10))
        x = SIZE[0]//2 - t.get_width()//2
        y = SIZE[1]//2 - t.get_height()//2
        screen.blit(t, (x,y))

    
    for e in pygame.event.get():#перебираємо усі події
        if e.type == pygame.QUIT:#якщо під час гри людина клікнула на хрестик
            running = False
    pygame.display.update()#оновлення екрану
    clock.tick(FPS)# частота оновлення екрану


quit()#закрити екран
