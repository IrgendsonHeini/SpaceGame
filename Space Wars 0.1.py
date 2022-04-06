# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 09:25:13 2021

@author: jstrittmatter
"""

import pygame
import os
import time
import random
pygame.font.init()
# +++KONSTANTEN+++
WIDTH  =  800
HEIGHT = 1000
WIN    = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Wars")

# Farben
ORANGE  = (255, 140,   0)
RED     = (200,   0,   0)
GREEN   = (  0, 255,   0)
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
GREY    = (100, 100, 100)
BROWN   = (120,  70,  15)
BLUE    = (  0,   0, 150)
bg      = (  7,  14,  30)
FPS     = 60

# Schiffe
TIE_FIGHTER                = pygame.transform.scale(pygame.image.load(os.path.join("Bilder", "Tie-Fighter.png")),(75,75))
TIE_HUNTER                  = pygame.transform.scale(pygame.image.load(os.path.join("Bilder", "Tie-Jäger.png")),(75,75))
STAR_DESTROYER             = pygame.transform.scale(pygame.image.load(os.path.join("Bilder", "Star-Destroyer.png")),(150,150))
DEATHSTAR                  = pygame.transform.scale(pygame.image.load(os.path.join("Bilder", "Death-Star.png")),(200,200))
MILLENNIUM_FALCON          = pygame.transform.scale(pygame.image.load(os.path.join("Bilder", "Millennium-Falcon.png")),(100,100))
placeholder                = pygame.transform.scale(pygame.image.load(os.path.join("Bilder", "placeholder.png")),(100,100))
# Laser
GREEN_LASER                = pygame.transform.scale(pygame.image.load(os.path.join("Bilder", "Laser green.png")),(50,50))
RED_LASER                  = pygame.transform.scale(pygame.image.load(os.path.join("Bilder", "Laser red.png")),(50,50))

# Hintergrund
BG = pygame.transform.scale(pygame.image.load(os.path.join("Bilder", "Hintergrund.png")),(WIDTH,HEIGHT))

# +++KLASSEN+++
class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self,window):
        window.blit(self.img,(self.x+25, self.y))
    
    def move(self,vel):
        self.y += vel
    
    def off_screen(self, height):
        return not self.y <= height and self.y >= 0
    
    def collision(self,obj):
        return collide(self, obj)        

class Ship:
    COOLDOWN = int(FPS/2)
    def __init__(self,x,y,health=100):
        self.x         = x
        self.y         = y
        self.health    = health
        self.ship_img  = placeholder
        self.laser_img = placeholder
        self.lasers    = []
        self.mask      = pygame.mask.from_surface(self.ship_img)
        self.max_health= health
        self.cool_down_counter = 0
        
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
                obj.health -= 10
                self.lasers.remove(laser)           
    
    def get_width(self):
        return self.ship_img.get_width()  
    
    def get_height(self):
        return self.ship_img.get_height()
    
    def move(self, vel):
        self.y += vel
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Player(Ship):
    COOLDOWN = int(FPS / 3)
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = MILLENNIUM_FALCON
        self.laser_img= GREEN_LASER  
    
    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        
                        try:
                            self.lasers.remove(laser)
                        except ValueError:
                            pass
class TieFighter(Ship):
    def __init__(self,x,y,health=10):
        super().__init__(x,y,health)
        self.ship_img = TIE_FIGHTER   

class TieHunter(Ship):
    def __init__(self,x,y,health=10):
        super().__init__(x,y,health)
        self.ship_img = TIE_HUNTER
        self.laser_img = RED_LASER
        
class StarDestroyer(Ship):
    def __init__(self,x,y,health=30):
        super().__init__(x,y,health)
        self.ship_img = STAR_DESTROYER
        self.laser_img = RED_LASER
        
class Deathstar(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = DEATHSTAR
        
        

        
  
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None

#Hauptschleife

def main():
    run   = True
    lost  = False
    lost_count = 0   
    lives = 5
    level = 0
    enemies = []
    wave_lenght = 0   
    player_vel = 10
    enemy_vel  = 2 
    laser_vel = 20
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 100)        

    player = Player(450,800)
    clock = pygame.time.Clock()
    

    
    def redraw_window():
        lives_label = main_font.render(f"LEBEN: {lives}",1,ORANGE)
        level_label = main_font.render(f"LEVEL: {level}",1,ORANGE)       
        
        WIN.blit(BG,(0,0))
        
        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)
        


        WIN.blit(lives_label,(10,10))
        WIN.blit(level_label,(WIDTH-200,10))
        
        if lost:
            lost_label = lost_font.render("GAME OVER",1,RED)
            WIN.blit(lost_label,(WIDTH/2-lost_label.get_width()/2,HEIGHT/2-lost_label.get_height()/2))            
        
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
            
        """if lost:
            if lost_count > FPS*3:
                run = False
            else:
                continue"""
        
        if len(enemies) == 0:
            level += 1
            wave_lenght += 5
            for i in range(wave_lenght):
                enemy = TieFighter(random.randrange(50,WIDTH-150),random.randrange(-1500,-100))
                enemies.append(enemy)

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
# Kollision Rand
        if player.x > WIDTH - player.get_width():
            player.x = WIDTH - player.get_width()
                
        if player.y > HEIGHT - player.get_height():
            player.y = HEIGHT - player.get_height()
            
        if player.x < 0:
            player.x = 0
            
        if player.y < 0:
            player.y = 0
# Gegner erstellen           
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if enemy.y + enemy.get_height() > HEIGHT+50:
                lives -= 1
                enemies.remove(enemy)
# Schießen        
        player.move_lasers(-laser_vel, enemies)
        
        





main()
pygame.quit()






