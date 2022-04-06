# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 09:25:13 2021

@author: jstrittmatter
"""

# +++Imports+++
import pygame
import os
import random
pygame.font.init()

# +++KONSTANTEN+++
WIDTH  =  800
HEIGHT = 1000
WIN    = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Wars")

# Farben
ORANGE  = (255, 140,   0)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
GREY    = (100, 100, 100)
BROWN   = (120,  70,  15)
BLUE    = (  0,   0, 150)
YELLOW  = (255, 255,   0)
FPS     = 60

GREEN_LASER_COLOR = (  0, 200,   0)
RED_LASER_COLOR = (237,  28,  36)

SMALL  =  75
MEDIUM = 150
LARGE  = 200

# Schiffe
TIE_FIGHTER       = pygame.image.load(os.path.join("Space Wars assets", "Tie-Fighter.png"))
TIE_HUNTER        = pygame.image.load(os.path.join("Space Wars assets", "Tie-Hunter.png"))
STAR_DESTROYER    = pygame.image.load(os.path.join("Space Wars assets", "Star-Destroyer.png"))
DEATHSTAR         = pygame.image.load(os.path.join("Space Wars assets", "Death-Star.png"))
MILLENNIUM_FALCON = pygame.image.load(os.path.join("Space Wars assets", "Millennium-Falcon.png"))
PLACEHOLDER       = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "placeholder.png")),(100,100))

# Laser
GREEN_LASER       = pygame.image.load(os.path.join("Space Wars assets", "Laser green.png"))
RED_LASER         = pygame.image.load(os.path.join("Space Wars assets", "Laser red.png"))
RED_LASER_BIG     = pygame.transform.scale(RED_LASER,(50,50))
# Explosionen
EXPLOSION_01      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion1.png")),(SMALL,SMALL))
EXPLOSION_02      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion2.png")),(SMALL,SMALL))
EXPLOSION_03      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion3.png")),(SMALL,SMALL))
EXPLOSION_04      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion4.png")),(SMALL,SMALL))
EXPLOSION_05      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion4.png")),(SMALL,SMALL))
EXPLOSION_06      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion6.png")),(SMALL,SMALL))
EXPLOSION_07      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion7.png")),(SMALL,SMALL))
EXPLOSION_08      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion8.png")),(SMALL,SMALL))
EXPLOSION_09      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion9.png")),(SMALL,SMALL))
EXPLOSION_10      = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Explosion10.png")),(SMALL,SMALL))

# Hintergrund
BG = pygame.transform.scale(pygame.image.load(os.path.join("Space Wars assets", "Hintergrund.png")),(WIDTH,HEIGHT))

# +++KLASSEN+++

class Laser:
    def __init__(self,x,y,img):
        self.x    = x
        self.y    = y
        self.img  = img
        self.mask = pygame.mask.from_surface(self.img.convert_alpha())
        
    def draw(self,window):
        window.blit(self.img,(self.x, self.y))
    
    def move(self,vel):
        self.y += vel
    
    def off_screen(self, height):
        return not self.y <= height and self.y >= 0
    
    def collision(self,obj):
        if self.img == GREEN_LASER:
            return collide_player(self, obj)
        else:
            return collide(self, obj)

class Ship:
    COOLDOWN = 60
    def __init__(self,x,y,health=10):
        self.x         = x
        self.y         = y
        self.health    = health
        self.ship_img  = PLACEHOLDER
        self.laser_img = PLACEHOLDER
        self.lasers    = []
        self.mask      = pygame.mask.from_surface(self.ship_img.convert_alpha())
        self.max_health= health
        self.attack    = 10         
        self.cooldown_counter = 0    
    
    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)
            
            
    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= self.attack
                self.lasers.remove(laser)           
    
    def get_width(self):
        return self.ship_img.get_width()  
    
    def get_height(self):
        return self.ship_img.get_height()
    
    def move(self, vel):
        self.y += vel
    
    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1
        
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1
    
   

class Player(Ship):
    COOLDOWN = 15
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = MILLENNIUM_FALCON
        self.laser_img= GREEN_LASER 
        self.score = 0
        self.final_score = None
    
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x+25,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1
            
    
    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= self.attack                      
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        if obj.health <= 0:  
                            self.score += obj.score_value                            
                            objs.remove(obj)
    
    def healthbar(self, window):
        pygame.draw.rect(window, RED,   (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, GREEN, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
        
class TieFighter(Ship):
    def __init__(self,x,y,health=10):
        super().__init__(x,y,health)
        self.ship_img = TIE_FIGHTER  
        self.score_value = 10
        

class TieHunter(Ship):
    COOLDOWN = 120
    def __init__(self,x,y,health=10):
        super().__init__(x,y,health)
        self.ship_img = TIE_HUNTER
        self.laser_img = RED_LASER
        self.score_value = 20
        
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x+10, self.y+50, self.laser_img)
            self.lasers.append(laser)
            laser = Laser(self.x+40, self.y+50, self.laser_img)
            self.lasers.append(laser)            
            self.cooldown_counter = 1
    
    def move_lasers(self,vel,obj):      
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= self.attack
                self.lasers.remove(laser)
        
class StarDestroyer(Ship):
    COOLDOWN = 180
    def __init__(self,x,y,health=30):
        super().__init__(x,y,health)
        self.ship_img = STAR_DESTROYER
        self.laser_img = RED_LASER_BIG
        self.score_value = 50
        self.hitbox = pygame.draw.rect(WIN, RED, (self.x+60,self.y+24,30,41))
        self.attack = 20
   
    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)
            
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x+25, self.y+25, self.laser_img)
            self.lasers.append(laser)
            laser = Laser(self.x+50, self.y+100, self.laser_img)
            self.lasers.append(laser)   
            laser = Laser(self.x+75, self.y+25, self.laser_img)
            self.lasers.append(laser)    
            self.cooldown_counter = 1
        
        
class Deathstar(Ship):
    def __init__(self,x,y,health=1000):
        super().__init__(x,y,health)
        self.ship_img = DEATHSTAR
        self.score_value = 1000
    
    def move(self,vel):
        if self.y + vel < 50:
            self.y += vel
        else:
            self.y = 50

class Explosion:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = EXPLOSION_01
        
    def draw(self, window):
        
        window.blit(self.img,(self.x,self.y))        
        counter = 0
        counter += 1
        
        if counter >= 2:
            self.img = EXPLOSION_02
        elif counter >= 3:
            self.img = EXPLOSION_03
        elif counter >= 4:
            self.img = EXPLOSION_04
        elif counter >= 5:
            self.img = EXPLOSION_05
        elif counter >= 6:
            self.img = EXPLOSION_06
        elif counter >= 7:
            self.img = EXPLOSION_07
        elif counter >= 8:
            self.img = EXPLOSION_08
        return False
            
        
    
        
        

# +++FUNKTIONEN+++      

def collide_player(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y -50
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None

def collide(obj1, obj2):   
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None

def collide_enemy(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y +25
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None   


# +++VARIABLEN+++
clock = pygame.time.Clock()
player = Player(350,800)

# +++HAUPTMENÜ+++
def main_menu():
    space_wars_font  = pygame.font.SysFont("comicsans", 120)
    instruction_font = pygame.font.SysFont("comicsans", 40)

    space_wars_label = space_wars_font.render("SPACE WARS",1,YELLOW)  
    instruction      =instruction_font.render('Use Arrow keys to move and "S" to shoot',1,WHITE)
    instruction2     = instruction_font.render('Press "S" to start',1,WHITE)    
    counter = 0
    
    run = True
    while run:
        counter += 1
        
        clock.tick(20)
        WIN.blit(BG,(0,0))
        WIN.blit(instruction,(WIDTH/2-(instruction.get_width()/2),400))
        if counter < 15:
            WIN.blit(instruction2,(WIDTH/2-(instruction2.get_width()/2),470))
        if counter >= 20:
            counter = 0
        
        WIN.blit(space_wars_label,(WIDTH/2-space_wars_label.get_width()/2,200))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                     
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            run = False
            game_loop()
        
        
    
# +++HAUPTSCHLEIFE+++

def game_loop():
    run   = True
    lost  = False
    lost_count = 0
    lives = 5
    level = 0
    fleet = []
    wave_length = 6
    player_vel = 10
    enemy_vel  = 1 
    laser_vel = 3
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 150)        

    
    player.score = 0
    

    
    def redraw_window():
        lives_label = main_font.render(f"LIVES: {lives}",1,ORANGE)
        health_label = main_font.render(f"SCORE: {player.score}",1,ORANGE)        
        
        WIN.blit(BG,(0,0))
        
        for enemy in fleet:
            enemy.draw(WIN)
        
        player.draw(WIN)

        WIN.blit(lives_label,(10,10))
        WIN.blit(health_label,(WIDTH-health_label.get_width()-10,10))
        
        if lost:
            lost_label = lost_font.render("GAME OVER",1,(200,  0,  0))
            WIN.blit(lost_label,(WIDTH/2-lost_label.get_width()/2,HEIGHT/2-lost_label.get_height()/2))            
        
        pygame.display.update()
# Hauptschleife
    while run:
        clock.tick(FPS)
        redraw_window()
        if lives <= 0 or player.health <= 0:
            lost = True

# Game over       
        if lost:
           
            if lost_count == 0:
                player.final_score = player.score
                player.ship_img = EXPLOSION_01           
            if lost_count == 4:
                player.ship_img = EXPLOSION_03
            if lost_count == 8:
                player.ship_img = EXPLOSION_04
            if lost_count == 12:
                player.ship_img = EXPLOSION_05              
            if lost_count == 16:
                player.ship_img = EXPLOSION_06
            if lost_count == 20:
                player.ship_img = EXPLOSION_07
            if lost_count == 24:
                player.ship_img = EXPLOSION_08
            lost_count += 1                
            if lost_count > FPS*3:
                run = False
                score_window()
            else:
                continue
# Gegner einfügen
        if len(fleet) == 0:
            level += 1
            wave_length += 3
    
            def spawn_tiefighter():
                for i in range(wave_length):
                    x = random.randrange(50,WIDTH-SMALL-50,SMALL)
                    y = random.randrange(-700-SMALL*level,-100,SMALL)                               
                    tiefighter = TieFighter(x,y)
                    
                    for enemy in fleet:
                        if enemy.x == tiefighter.x and enemy.y == tiefighter.y:
                            fleet.remove(enemy)
                    
                    fleet.append(tiefighter)
                            
            def spawn_tiehunter():
                if level >= 0:
                    for i in range(int(wave_length/3)):
                        x = random.randrange(50,WIDTH-SMALL-50,SMALL)
                        y = random.randrange(-700-SMALL*level,-100,SMALL)                      
                        tiehunter = TieHunter(x,y)
                        
                        for enemy in fleet:
                            if enemy.x == tiehunter.x and enemy.y == tiehunter.y:
                                fleet.remove(enemy)
                        
                        fleet.append(tiehunter)
            
            def spawn_stardestroyer():
                if level >= 0:
                    for i in range(int(wave_length/6)):
                        x = random.randrange(50,WIDTH-SMALL-50,MEDIUM)
                        y = random.randrange(-700-SMALL*level,-100,MEDIUM)                      
                        stardes = StarDestroyer(x,y)
                        
                        for enemy in fleet:
                            if enemy.x == stardes.x and enemy.y == stardes.y:
                                fleet.remove(enemy)
                            if enemy.x+SMALL+1 == stardes.x and enemy.y == stardes.y:
                                fleet.remove(enemy)
                            if enemy.x == stardes.x and enemy.y+SMALL+1 == stardes.y:
                                fleet.remove(enemy)
                            if enemy.x+SMALL+1 == stardes.x and enemy.y+SMALL+1 == stardes.y:
                                fleet.remove(enemy)
                        
                        fleet.append(stardes)                        
            
            spawn_tiefighter()
            spawn_tiehunter()
            spawn_stardestroyer()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
# Steuerung                
        keys = pygame.key.get_pressed()        
        if keys[pygame.K_LEFT]:
            player.x -= player_vel
                
        if keys[pygame.K_RIGHT]:
            player.x +=  player_vel
            
        if keys[pygame.K_UP]:
            player.y -= player_vel
            
        if keys[pygame.K_DOWN]:
            player.y +=  player_vel
            
        if keys[pygame.K_s]:
            player.shoot()
            
        if keys[pygame.K_ESCAPE]:
            main_menu()
        
# Kollision Rand
        if player.x > WIDTH - player.get_width():
            player.x = WIDTH - player.get_width()
                
        if player.y > HEIGHT - player.get_height():
            player.y = HEIGHT - player.get_height()
            
        if player.x < 0:
            player.x = 0
            
        if player.y < 0:
            player.y = 0
# Gegner           
        for enemy in fleet[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if enemy.laser_img == RED_LASER or enemy.laser_img == RED_LASER_BIG:            
                if enemy.y >= 0 and random.randrange(0, FPS*3) == 1:
                    enemy.shoot()
            
            if enemy.y + enemy.get_height() > HEIGHT+50:
                lives -= 1
                fleet.remove(enemy)

            if collide_enemy(enemy, player):
                player.health -= enemy.attack
                enemy.health -= player.attack
                if enemy.health >= 0:
                    player.score += enemy.score_value
                    fleet.remove(enemy)   

# Schießen        
        player.move_lasers(-laser_vel*5, fleet)

def score_window():
    space_wars_font  = pygame.font.SysFont("comicsans", 120)
    score_font       = pygame.font.SysFont("comicsans", 80)
    instruction_font = pygame.font.SysFont("comicsans", 40)

    space_wars_label = space_wars_font.render("SPACE WARS",1,YELLOW)  
    score_label      =score_font.render(f'FINAL SCORE:{player.final_score}',1,ORANGE)
    instruction      = instruction_font.render('Press "S" to restart or "ESC" to close',1,WHITE)
    run = True
    while run:
        
        clock.tick(20)
        WIN.blit(BG,(0,0))
        WIN.blit(score_label,(WIDTH/2-score_label.get_width()/2,400))
        WIN.blit(instruction,(WIDTH/2-instruction.get_width()/2,600))
        
        WIN.blit(space_wars_label,(WIDTH/2-space_wars_label.get_width()/2,200))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                     
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            run = False
            player.health = 100
            player.x = 350
            player.y = 800
            player.score = 0
            player.final_score = None
            player.ship_img = MILLENNIUM_FALCON
            game_loop()
        
        if keys[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            break
            exit()
        
        
        



main_menu()


pygame.quit()
exit()






