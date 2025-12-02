import pygame
from random import randint
pygame.init()

Width, Height = 800, 600
fps = 60

window = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 25)
bigfont = pygame.font.Font(None, 80)

class target:
    def __init__(self):
        self.px, self.py = randint(0, Width - 30), -100
        self.speed = 3
        self.rect = pygame.Rect(self.px, self.py, 30, 30)
        targets.append(self)

    def update(self):
        global health
        self.py += self.speed
        self.rect.y = int(self.py)

        if self.rect.top > Height: 
            targets.remove(self)
            health -= 1
            return

    def draw(self):
        pygame.draw.rect(window, pygame.Color('red'), self.rect)

class bullet:
    def __init__(self, x, y, speed):
        self.px, self.py = x, y
        self.speed = speed
        bullets.append(self)

    def update(self):
        global scores, bonus_active, bonus_timer
        self.py -= self.speed
        if self.py < 0:
            bullets.remove(self)
            return
        
        for target in targets:
            if target.rect.collidepoint(self.px, self.py):
                targets.remove(target)
                bullets.remove(self)
                if bonus_active:
                 scores += 2
                else:  
                 scores += 1
                return
            
        for orb in bonus_orbs:
            if orb.rect.collidepoint(self.px, self.py):
                bonus_orbs.remove(orb)
                bullets.remove(self)
                bonus_active = True
                bonus_timer = 300
                return
            
    def draw(self):
        pygame.draw.circle(window, pygame.Color('yellow'), (self.px, self.py), 2)

class BonusOrb:
    def __init__(self):
        self.px, self.py = randint(50, Width - 50), randint(50, Height - 200)
        self.rect = pygame.Rect(self.px - 15, self.px - 15, 30, 30)
        bonus_orbs.append(self)

    def draw(self):
        pygame.draw.circle(window, pygame.Color('cyan'), (self.px, self.py), 15)


gunPX, gunPY = Width //2, Height - 30

bullets = []
targets = []
bonus_orbs = []

timer = 60
scores = 0
health = 3

bonus_active = False
bonus_timer = 0

def draw_game_over():
    window.fill((0, 0, 0))
    text = bigfont.render("GAME OVER!", True, pygame.Color('red'))
    score_text = font.render(f"Final score: {scores}", True, pygame.Color('white'))
    window.blit(text, (Width// 2 - text.get_width()// 2, Height// 2 - 80))
    window.blit(score_text, (Width// 2 - score_text.get_width()// 2, Height// 2 + 10))
    pygame.display.update()
    pygame.time.delay(2500)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    if health <= 0:
        draw_game_over()
        play = False
        continue

    mousePX, mousePY = pygame.mouse.get_pos()
    b1, b2, b3 = pygame.mouse.get_pressed()

    gunPX += (mousePX - gunPX) * 0.1

    if b1: b = bullet(gunPX, gunPY, 5)

    if timer > 0: timer -= 1
    else:
        t = target()
        timer = randint(10, 30)

    if randint(1, 500) == 1 and len(bonus_orbs) < 1:
        BonusOrb()

    if bonus_active:
        bonus_timer -= 1
        if bonus_timer <= 0:
            bonus_active = False


    for b in bullets:
        b.update()
    for t in targets:
        t.update()

    window.fill(pygame.Color('black'))

    pygame.draw.circle(window, pygame.Color('grey'), (gunPX, gunPY), 10)
    pygame.draw.line(window, pygame.Color('grey'), (gunPX, gunPY), (gunPX, gunPY - 20), 5)

    for b in bullets:
        b.draw()
    for t in targets:
        t.draw()
    for orb in bonus_orbs:
        orb.draw()

    if bonus_active:
        bonus_text = font.render("2x SCORE ACTIVE!", True, pygame.Color('cyan'))
        window.blit(bonus_text, (Width//2 - bonus_text.get_width()// 2, 10))

    health_text = font.render(f"Health: {health}", True, pygame.Color('green'))
    window.blit(health_text, (10, 40))
    text = font.render('Scores: ' + str(scores), 1, pygame.Color('white'))
    window.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(fps)

pygame.quit