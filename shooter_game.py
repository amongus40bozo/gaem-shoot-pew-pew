#Создай собственный Шутер!
from random import randint
from pygame import *
speed = 1
player = 'rocket.png'
shoot = 'bullet.png'
enemy = 'ufo.png'
asteroid = 'asteroid.png'
class GameSprites(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(65, 65)) 
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprites):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(shoot, self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class Enemy(GameSprites):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprites):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0          

class Bullet(GameSprites):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((700, 500))
display.set_caption('peepee poopoo.')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

player = Player(player, 600, 400, 4)

enemys = sprite.Group()
for i in range(1, 6):
    enemy1 = Enemy(enemy, randint(80, win_width - 80), -40, 1)
    enemys.add(enemy1)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid1 = Asteroid(asteroid, randint(80, win_width - 80), -40, 1)
    asteroids.add(asteroid1)

bullets = sprite.Group()

mixer.init()
mixer.music.load('win2.mp3')
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Comic Sans MS', 36)

score = 0
lost = 0

win = font2.render('YOU WIN!!! OOOO', True, (0, 180, 0))
lose = font2.render('YOU LOST!!! AAAAAA', True, (180, 0, 0))

finish = False

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
    if not finish:
        window.blit(background,(0,0))
        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        player.update()
        enemys.update()
        bullets.update()
        asteroids.update()

        player.reset()
        enemys.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(bullets, enemys, True, True)
        for c in collides:
            score = score + 1
            enemy1 = Enemy(enemy, randint(80, win_width - 80), -40, 1)
            enemys.add(enemy1)

        if sprite.spritecollide(player, enemys, False) or lost >= 3:
            finish = True
            window.blit(lose, (200, 200))
            mixer.music.stop()
            mixer.music.load('lost.mp3')
            mixer.music.play()

        if sprite.spritecollide(player, asteroids, False) or lost >= 3:
            finish = True
            window.blit(lose, (200, 200))
            mixer.music.stop()
            mixer.music.load('lost.mp3')
            mixer.music.play()            

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))
            mixer.music.stop()
            mixer.music.load('musci.mp3')
            mixer.music.play()

        display.update()
time.delay(50)