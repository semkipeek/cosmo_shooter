from pygame import *
import random
from time import time as timer
from time import sleep
backx = 700
backy = 500
kill = 0
lost = 0
reloaded = False
fired = 0
window = display.set_mode((backx, backy))
display.set_caption('CosmoShooter Optimised')
class GameSprite(sprite.Sprite):
    def __init__(self, pimage, x , y, speed, ysize, xsize):
        super().__init__()
        self.image = transform.scale(image.load(pimage), (xsize, ysize))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        global fired
        fired +=1
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 20, 10)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > backy:
            self.rect.y = 0
            self.rect.x = random.randint(80, 620)
            lost += 1
class Astro(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > backy:
            self.rect.y = 0
            self.rect.x = random.randint(80, 620)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
player = Player('rocket.png', 300, 400, 7, 100, 75)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(4):
    enemy = Enemy('ufo.png', random.randint(80,620), 0, random.randint(1, 2), 50, 75)
    monsters.add(enemy)
asteroids = sprite.Group()
for i in range(1):
    asteroid = Astro('asteroid.png', random.randint(80,620), 0, random.randint(7, 8), 50, 50)
    asteroids.add(asteroid)
clock = time.Clock()
FPS = 60
font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 70)
killtxt = font1.render('Killed: '+str(kill), True, (255, 255, 255))
losttxt = font1.render('Lost: '+str(lost), True, (255, 255, 255))
heath = 3
healthtxt = font1.render('Health: '+str(heath), True, (255, 255, 255))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
'''money = mixer.Sound('money.ogg')'''
fire_sound = mixer.Sound('fire.ogg')
run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if fired < 10 and reloaded == False:
                    fire_sound.play()
                    player.fire()
                if fired >= 10 and reloaded == False:
                    reloaded = True
                    time1 = timer()
    if finish == False:
        killtxt = font1.render('Killed: '+str(kill), True, (255, 255, 255))
        losttxt = font1.render('Lost: '+str(lost), True, (255, 255, 255))
        healthtxt = font1.render('Health: '+str(heath), True, (255, 255, 255))
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        window.blit(killtxt, (10, 10))
        window.blit(losttxt, (10, 40))
        window.blit(healthtxt, (10, 70))
        bullets.draw(window)
        bullets.update()
        spriteslist = sprite.groupcollide(monsters, bullets, True, True)
        for i in spriteslist:
            kill+=1
            enemy = Enemy('ufo.png', random.randint(80,620), 0, random.randint(1, 2), 50, 75)
            monsters.add(enemy)
        if kill > 5:
            finish = font2.render('You win!', True, (255, 255, 255))
            window.blit(finish, (250, 200))
            window.blit(killtxt, (10, 10))
            finish = True
        if sprite.spritecollide(player, asteroids, True, False):
            heath -= 1
            asteroid = Astro('asteroid.png', random.randint(80,620), 0, random.randint(6, 7), 50, 50)
            asteroids.add(asteroid)
        if lost > 9 or sprite.spritecollide(player, monsters, False) or heath <= 0:
            finish = font2.render('You lose!', True, (255, 255, 255))
            window.blit(finish, (250, 200))
            window.blit(losttxt, (10, 40))
            finish = True
        if reloaded == True:
            time2 = timer()
            if time2 - time1 < 1:
                reloadtxt = font1.render('Wait, reload...', True, (255, 0, 0))
                window.blit(reloadtxt, (10, 100))
            if time2 - time1 > 1:
                reloaded = False
                fired = 0
        display.update()
    else:
        finish = False
        heath = 3
        kill = 0
        lost = 0
        reloaded = False
        fired = 0
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        for i in asteroids:
            i.kill()
        time.delay(5000)
        for i in range(4):
            enemy = Enemy('ufo.png', random.randint(80,620), 0, random.randint(1, 2), 50, 75)
            monsters.add(enemy)
        for i in range(1):
            asteroid = Astro('asteroid.png', random.randint(80,620), 0, random.randint(7, 8), 50, 50)
            asteroids.add(asteroid)
    clock.tick(FPS)
