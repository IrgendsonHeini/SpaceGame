#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 09:25:13 2021

@author: Jan Strittmatter
"""

# +++IMPORTS+++
import pygame
import os
import random

class GameLogic:
    def __init__(self):
        self.lasers     = []
        self.explosions = []
        self.fleet      = []
        self.power_ups  = []
        self.lives      = 5
        self.infos       = []

gl = GameLogic()


pygame.init()
pygame.joystick.init()
joystick_list = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

class JoystickToken:
    def __init__(self):
        self.test = "test"
    
    def get_button(x):
        return False

try:
    joystick = joystick_list[0]
    joystick.init()
except:
    joystick = JoystickToken

# +++KONSTANTEN und VARIABLEN+++

WIDTH  = 1280
HEIGHT = 1024
FPS = 60
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Wars")

# Farben
ORANGE       = (255, 140,   0)
RED          = (255,   0,   0)
GREEN        = (  0, 200,   0)
BLACK        = (  0,   0,   0)
WHITE        = (255, 255, 255)
GREY         = (100, 100, 100)
BROWN        = (120,  70,  15)
BLUE         = (  0,   0, 150)
LIGHT_BLUE   = (  0,  75, 200)
YELLOW       = (255, 255,   0)
BRIGHT_GREEN = (  0, 240,   0)


GREEN_LASER_COLOR = (  0, 200,   0)
RED_LASER_COLOR = (237,  28,  36)

SMALL  =  75
MEDIUM = 150
LARGE  = 200

# kleine Helfer
load        = pygame.image.load
scale       = pygame.transform.scale
path        = os.path.join
main_folder = os.path.dirname(os.path.abspath(__file__))
assets      = "Space Wars assets"

# Laser
GREEN_LASER   = load(path(main_folder,assets, "Laser green.png"))
RED_LASER     = load(path(main_folder,assets, "Laser red.png"))
RED_LASER_BIG = scale(RED_LASER,(50,50))

# Explosionen Bilder (Animation)
EXPLOSION_01 = scale(load(path(main_folder,assets, "Explosion01.png")),(SMALL,SMALL))
EXPLOSION_02 = scale(load(path(main_folder,assets, "Explosion02.png")),(SMALL,SMALL))
EXPLOSION_03 = scale(load(path(main_folder,assets, "Explosion03.png")),(SMALL,SMALL))
EXPLOSION_04 = scale(load(path(main_folder,assets, "Explosion04.png")),(SMALL,SMALL))
EXPLOSION_05 = scale(load(path(main_folder,assets, "Explosion05.png")),(SMALL,SMALL))
EXPLOSION_06 = scale(load(path(main_folder,assets, "Explosion06.png")),(SMALL,SMALL))
EXPLOSION_07 = scale(load(path(main_folder,assets, "Explosion07.png")),(SMALL,SMALL))
EXPLOSION_08 = scale(load(path(main_folder,assets, "Explosion08.png")),(SMALL,SMALL))
EXPLOSION_09 = scale(load(path(main_folder,assets, "Explosion09.png")),(SMALL,SMALL))
EXPLOSION_10 = scale(load(path(main_folder,assets, "Explosion10.png")),(SMALL,SMALL))
EXPLOSIONS   = [EXPLOSION_01,
                EXPLOSION_02,
                EXPLOSION_03,
                EXPLOSION_04,
                EXPLOSION_05,
                EXPLOSION_06,
                EXPLOSION_07,
                EXPLOSION_08,                    
                EXPLOSION_09,
                EXPLOSION_10]                    

# Explosionen (Geräusche)
EXPLOSION_ENEMY  = pygame.mixer.Sound(path(main_folder,assets,"Explosion-Enemy.wav"))
EXPLOSION_PLAYER = pygame.mixer.Sound(path(main_folder,assets,"Explosion-Player.wav"))
EXPLOSION_ENEMY.set_volume(0.5)
EXPLOSION_PLAYER.set_volume(0.7)

# Deathstar (Animation)
DEATHRAY_01 = load(path(main_folder,assets, "Deathray-01.png"))
DEATHRAY_02 = load(path(main_folder,assets, "Deathray-02.png"))
DEATHRAY_03 = load(path(main_folder,assets, "Deathray-03.png"))
DEATHRAY_04 = load(path(main_folder,assets, "Deathray-04.png"))
DEATHRAY_05 = load(path(main_folder,assets, "Deathray-05.png"))
DEATHRAY_06 = load(path(main_folder,assets, "Deathray-06.png"))
DEATHRAY_07 = load(path(main_folder,assets, "Deathray-07.png"))
DEATHRAY_08 = load(path(main_folder,assets, "Deathray-08.png"))
DEATHRAY_09 = load(path(main_folder,assets, "Deathray-09.png"))
DEATHRAY_10 = load(path(main_folder,assets, "Deathray-10.png"))
DEATHRAY_11 = load(path(main_folder,assets, "Deathray-11.png"))
DEATHRAY_12 = load(path(main_folder,assets, "Deathray-12.png"))
DEATHRAY_13 = load(path(main_folder,assets, "Deathray-13.png"))
DEATHRAY_14 = load(path(main_folder,assets, "Deathray-14.png"))
DEATHRAY_15 = load(path(main_folder,assets, "Deathray-15.png"))
DEATHRAY    = [DEATHRAY_01,
               DEATHRAY_02,
               DEATHRAY_03,
               DEATHRAY_04,
               DEATHRAY_05,
               DEATHRAY_06,
               DEATHRAY_07,
               DEATHRAY_08,
               DEATHRAY_09,
               DEATHRAY_10,
               DEATHRAY_11,
               DEATHRAY_12,
               DEATHRAY_13,
               DEATHRAY_14,
               DEATHRAY_15]
            
# Hintergrund und Sonstiges

CURSOR       = load(path(main_folder,assets,"Cursor.png"))
JOYSTICK     = scale(load(path(main_folder,assets, "Pixel-Joystick.png")),(75,75))
YELLOWBUTTON = scale(load(path(main_folder,assets, "Pixel-Yellow-Button.png")),(75,75))
BLUEBUTTON   = scale(load(path(main_folder,assets, "Pixel-Blue-Button.png")),(75,75))
GREENBUTTON  = scale(load(path(main_folder,assets, "Pixel-Green-Button.png")),(75,75))
BG           = scale(load(path(main_folder,assets, "Hintergrund.jpg")),(WIDTH,HEIGHT))

# +++KLASSEN+++

class InstructionSprites():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = BG
        
    def draw(self):
        screen.blit(self.img,(self.x,self.y))

class Laser:
    def __init__(self,x,y,img,attack=10,vel=8):
        self.x    = x
        self.y    = y
        self.img  = img
        self.mask = pygame.mask.from_surface(self.img.convert_alpha())
        self.attack = attack
        self.vel = vel
        self.is_ship = False
    def draw(self):
        screen.blit(self.img,(self.x, self.y))
    
    def move(self,vel):
        self.y += self.vel
    
    def off_screen(self, height):
        return not self.y <= height and self.y >= 0
    
    def collision(self,obj):
        if self.img == GREEN_LASER:
            return collide(self, obj)
        else:
            return collide(self, obj)

class Ship:
    COOLDOWN = 60
    def __init__(self, x, y, hp = 10):
        self.x         = x
        self.y         = y
        self.hp        = hp
        self.ship_img  = load(path(main_folder,assets, "Millennium-Falcon.png"))
        self.laser_img = GREEN_LASER
        self.lasers    = []
        self.max_hp    = hp
        self.attack    = 10                   
        self.size      = 100
        self.score_value = 10
        self.cooldown_counter = 0 
        self.is_ship = True
    
    def draw(self):
        screen.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw()            
            
    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.hp -= self.attack
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
    COOLDOWN = FPS/5
    def __init__(self,x,y,hp=100):
        super().__init__(x,y,hp)
        self.ship_img    = load(path(main_folder,assets, "Millennium-Falcon.png"))
        self.ship_img_l  = load(path(main_folder,assets, "Millennium-Falcon-left.png"))
        self.ship_img_m  = load(path(main_folder,assets, "Millennium-Falcon.png"))
        self.ship_img_r  = load(path(main_folder,assets, "Millennium-Falcon-right.png"))
        self.laser_img   = GREEN_LASER 
        self.score       = 0
        self.final_score = None
        self.size        = 100
        self.mask        = pygame.mask.from_surface(self.ship_img.convert_alpha())
        self.invincible  = False
        self.krass_schießen = False
        self.vel = 10
   
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x+25,self.y,self.laser_img,vel = -15)
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
                        obj.hp -= self.attack                      
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        if obj.hp <= 0:  
                            self.score += obj.score_value  
                            explosion = Explosion(obj.x,obj.y,obj.size)
                            gl.explosions.append(explosion)
                            objs.remove(obj)
                            pygame.mixer.Sound.play(EXPLOSION_ENEMY)
    
    def hp_bar(self):
        pygame.draw.rect(screen,RED,  (self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(), 10))
        pygame.draw.rect(screen,BRIGHT_GREEN,(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width()*(self.hp/self.max_hp),10))

    def draw(self):
        super().draw()
        self.hp_bar()
        
        for explosion in gl.explosions:
            explosion.draw()
            if explosion.explosion_counter >= 9.5:
                gl.explosions.remove(explosion)

player = Player(WIDTH / 2 - 50,800)         

class TieFighter(Ship):
    def __init__(self,x,y,hp=10):
        super().__init__(x,y,hp)
        self.ship_img    = load(path(main_folder,assets, "Tie-Fighter.png")) 
        self.score_value = 10
        self.size        = 75
        self.mask        = pygame.mask.from_surface(self.ship_img.convert_alpha())
        
class TieHunter(Ship):
    def __init__(self,x,y,hp=10):
        super().__init__(x,y,hp)
        self.ship_img    = load(path(main_folder,assets, "Tie-Hunter.png"))
        self.laser_img   = RED_LASER
        self.score_value = 20
        self.size        = 75
        self.mask        = pygame.mask.from_surface(self.ship_img.convert_alpha())
        
    def move(self, vel):
        if self.y > - self.size:
            vel += 0.5
        self.y += vel        
        
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x+10, self.y+50, self.laser_img, attack = self.attack)
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
                obj.hp -= self.attack
                self.lasers.remove(laser)
        
class StarDestroyer(Ship):
    COOLDOWN = 120
    def __init__(self,x,y,hp=50):
        super().__init__(x,y,hp)
        self.ship_img    = load(path(main_folder,assets, "Star-Destroyer.png"))
        self.laser_img   = RED_LASER_BIG
        self.score_value = 80
        self.hitbox      = pygame.draw.rect(screen, RED, (self.x+60,self.y+24,30,41))
        self.attack      = 20
        self.size        = 150
        self.mask        = pygame.mask.from_surface(self.ship_img.convert_alpha())
        
    def move(self,vel):
       
        if self.y > -self.size:
            vel += -0.5
        self.y += vel
    
    def hp_bar(self):
        pygame.draw.rect(screen,RED,  (self.x+30,self.y-15,self.ship_img.get_width()-60, 10))
        pygame.draw.rect(screen,BRIGHT_GREEN,(self.x+30,self.y-15,(self.ship_img.get_width()-60)*(self.hp/self.max_hp),10))  
  
    def draw(self):
        screen.blit(self.ship_img,(self.x,self.y))
        self.hp_bar()
        for laser in self.lasers:
            laser.draw()
            
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x+25, self.y+25, self.laser_img, attack = self.attack)
            self.lasers.append(laser)
            laser = Laser(self.x+50, self.y+100, self.laser_img, attack = self.attack)
            self.lasers.append(laser)   
            laser = Laser(self.x+75, self.y+25, self.laser_img, attack = self.attack)
            self.lasers.append(laser)    
            self.cooldown_counter = 1
               
class Deathstar(Ship):
    counter = -90
    def __init__(self,x,y,hp=10000):
        super().__init__(x,y,hp)
        self.ship_img      = load(path(main_folder,assets, "Death-Star.png"))
        self.size          = 200
        self.target_x      = None
        self.target_y      = None        
        self.attack        = 100
        self.score_value   = 1000
        self.mask          = pygame.mask.from_surface(self.ship_img.convert_alpha())
        self.laser_img     = 'Big fat green laser!'
        self.targeting     = (player.x+50,player.y+50)
        self.counter       = -60
        self.spawn_counter = 0
    
    def move(self,vel):
        if self.y + vel < 50:
            self.y += vel
        else:
            self.y = 50           

    def hp_bar(self):
        pygame.draw.rect(screen,RED,         (self.x,self.y-15,self.ship_img.get_width(),                      15))
        pygame.draw.rect(screen,BRIGHT_GREEN,(self.x,self.y-15,self.ship_img.get_width()*(self.hp/self.max_hp),15))
    
    def draw(self):
        super().draw()
        self.hp_bar()
        if self.y == 50:
            self.counter += 0.25
        
        if int(self.counter) == 12:
            self.targeting = (player.x+50,player.y+50)
            self.target_x        = player.x
            self.target_y        = player.y

        if self.counter > 0 and self.counter <= 14.5:
            screen.blit(DEATHRAY[int(self.counter)],(self.x,self.y))
        
        if self.counter >= 15:
            screen.blit(DEATHRAY[14],(self.x,self.y))
            pygame.draw.line(screen,GREEN,(self.x+98,self.y+58),(self.target_x+50, self.target_y+50),4)
            explosion = Explosion(self.target_x,self.target_y,100)
            gl.fleet.append(explosion)              
        
        if self.counter >= 20:
            self.counter = -30
        
        self.spawn_counter += 1
        if self.spawn_counter > 60:
            self. spawn_counter = 0
            tiefighter = TieFighter(random.randrange(50,WIDTH-SMALL-50,SMALL),-100)
            tiefighter.score_value = 0
            gl.fleet.append(tiefighter)
    
    def shoot(self):    
        pass

class SlaveOne(Ship):
    COOLDOWN = 30
    def __init__(self,x,y,hp=50):
        super().__init__(x,y,hp)
        self.ship_img  = load(path(main_folder,assets, "Slave-I.png"))
        self.laser_img = RED_LASER
        self.attack    = 20
        self.mask      = pygame.mask.from_surface(self.ship_img.convert_alpha())
    
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x+25, self.y+70, self.laser_img,attack = self.attack)
            self.lasers.append(laser)
            laser = Laser(self.x+50, self.y+70, self.laser_img)
            self.lasers.append(laser)            
            self.cooldown_counter = 1

    def move(self,vel):
        self.y += vel

class ImperialShuttle(SlaveOne):
    def __init__(self,x,y,hp=30):
        super().__init__(x,y,hp) 
        self.ship_img    = load(path(main_folder,assets, "Imperial-Shuttle.png"))
        self.laser_img   = RED_LASER_BIG
        self.score_value = 50
        self.mask        = pygame.mask.from_surface(self.ship_img.convert_alpha())
        self.size = 100
    
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x, self.y+25, self.laser_img,attack = self.attack)
            self.lasers.append(laser) 
            laser = Laser(self.x+50, self.y+25, self.laser_img)
            self.lasers.append(laser)    
            self.cooldown_counter = 1
            
    def move(self, vel):
        if self.y > - self.size:
            vel += - 0.5
        self.y += vel 

class Explosion:
    def __init__(self,x,y,size=100):
        self.hp = 1
        self.x = x
        self.y = y
        self.size = size
        self.laser_img = None
        self.attack = 30
        self.img = EXPLOSIONS[0]
        self.mask        = pygame.mask.from_surface(self.img.convert_alpha())
        self.explosion_counter = 0
        self.is_ship = False
        self.score_value = 0
        
    def draw(self):              
        self.img = EXPLOSIONS[int(self.explosion_counter)]
        screen.blit(scale(self.img,(self.size,self.size)),(self.x,self.y))      
        self.explosion_counter += 0.5
        if self.explosion_counter >= 9.5:
            self.explosion_counter = 9.5
            return False
    
    def move(self,x):
        self.x += 0
        
    def move_lasers(x=0,y=0,z=0):
        pass
    
    def get_height(self):
        return self.size
    
    def get_width(self):
        return self.size

class InfoText:
    def __init__(self,text,x,y):
        self.text = text
        self.x = x
        self.y = y
        self.counter = FPS
        self.active = True
    
    def draw(self):
        font  = pygame.font.Font(path(main_folder,assets, "FGM.ttf"),20)
        label = font.render(self.text,1,GREEN)
        screen.blit(label,(self.x,self.y))
        self.counter -= 1
        if self.counter < 0:
            self.active = False

class PowerUps:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = None
        
    def move(self):
        self.y += 4
        
    def draw(self):
        screen.blit(self.img,(self.x,self.y))
    
    def get_width(self):
        return self.ship_img.get_width()  
    
    def get_height(self):
        return self.ship_img.get_height()

class R2D2(PowerUps):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img  = load(path(main_folder,assets, "R2-D2.png"))
        self.mask = pygame.mask.from_surface(self.img.convert_alpha())
    
    def bonus(self):
        player.hp += 30
        if player.hp > player.max_hp:
            player.hp = player.max_hp
        info = InfoText("HEALTH +",self.x,self.y)
        gl.infos.append(info)

class R5D4(PowerUps):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img  = load(path(main_folder,assets, "R5-D4.png"))
        self.mask = pygame.mask.from_surface(self.img.convert_alpha())
        
    def bonus(self):
        pass

class BB8(PowerUps):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.img  = load(path(main_folder,assets, "BB-8.png"))
        self.mask = pygame.mask.from_surface(self.img.convert_alpha())
    
    def bonus(self):
        gl.lives += 1
        info = InfoText("LIVES +",self.x,self.y)
        gl.infos.append(info)

# +++FUNKTIONEN+++      

def collide(obj1, obj2):  
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)  
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None  

def write(text,x,y,size=40,color=WHITE,time="infinite"):
    font  = pygame.font.Font(path(main_folder,assets, "FGM.ttf"),size)
    label = font.render(text,1,color) 
    if x == "center":
        x = WIDTH/2-label.get_width()/2
    if x == "right":
        x = WIDTH-label.get_width()-10
    if y == "center":
        y = HEIGHT/2-label.get_height()/2
    
    if time == "infinite":
        screen.blit(label,(x,y))
    else:
        timer = time*FPS
        timer -= 1
        if timer > 0:
            screen.blit(label,(x,y))
        

# +++VARIABLEN+++
clock = pygame.time.Clock()

# +++MUSIK+++
music = pygame.mixer.music
music.load(path(main_folder,assets,"background-music.wav"))
music.set_volume(0.3)
music.play(-1,0.0)

# +++HAUPTMENÜ+++
def main_menu():
    counter = 0
    
    active = True
    while active:
        counter += 1
        
        clock.tick(20)
        screen.blit(BG,(0,0))
        screen.blit(GREENBUTTON, (723,459))
        screen.blit(JOYSTICK,(565,372))
        screen.blit(YELLOWBUTTON,(429,459))       
        write("SPACE WARS","center",200,120,YELLOW)
        write('Use "   " to move',"center",400)
        write('Press "   " to shoot and "   " to pause',"center",470)
        write('created by',1137,HEIGHT-60,20)
        write('Jan Strittmatter',"right",HEIGHT-40,20)
                     
        if counter < 15:
            screen.blit(YELLOWBUTTON,(588,530))
            write('Press "   " to start',"center",540)
        
        if counter >= 20:
            counter = 0
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
        
        if not active:
            break            
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_l] or joystick.get_button(1):
            active = False
            game_loop()
        
        if  keys[pygame.K_q] or joystick.get_button(2):
            active = False
            pygame.quit()
                
# +++HAUPTSCHLEIFE+++

def game_loop():
    active = True
    lost = False
    lost_count = 0
    gl.lives = 5
    level = 0
    fleet_length = 4
    player.vel = 10
    enemy_vel  = 1
    laser_vel = 8       
    player.score = 0
    released = True    
    
    def redraw_window():      
        
        screen.blit(BG,(0,0))
      
        for pu in gl.power_ups:
            pu.draw()
        
        for enemy in gl.fleet:
            enemy.draw()
        
        for info in gl.infos:
            info.draw()
            if not info.active:
                gl.infos.remove(info)
                
        player.draw()
        
        player.move_lasers(-laser_vel*2, gl.fleet)
        
        write(f"LIVES: {gl.lives}",10,10,50,ORANGE)
        write(f"SCORE: {player.score}","right",10,50,ORANGE)
        
        if lost:           
            write("GAME OVER","center","center",140,RED)
        
        pygame.display.update()
# Hauptschleife
    while active:
        clock.tick(FPS)
        redraw_window()
        if gl.lives <= 0 or player.hp <= 0:
            lost = True

# Game over       
       
        if lost:
            music.pause()
           
            if lost_count == 0:
                player.final_score = player.score 
                pygame.mixer.Sound.play(EXPLOSION_PLAYER,0)                            
            
            if lost_count <= 9:    
                player.ship_img = EXPLOSIONS[int(lost_count)]
            
            lost_count += 0.3 
            if lost_count > 9:
                player.ship_img = EXPLOSIONS[9]
                           
            if lost_count > FPS:
                active = False
                score_window()
                if pygame.get_init() == False:
                    break
            else:
                continue
        
# Gegner einfügen
        
        if len(gl.fleet) == 0:
            level += 1
            fleet_length += 2
    
            def spawn_tiefighter():
                for i in range(fleet_length):
                    x = random.randrange(50,WIDTH-SMALL-50,SMALL)
                    y = random.randrange(-400-SMALL*level,-100,SMALL)                               
                    tiefighter = TieFighter(x,y)
                    
                    for enemy in gl.fleet:
                        if enemy.x == x and enemy.y == y:
                            gl.fleet.remove(enemy)                   
                    
                    gl.fleet.append(tiefighter)
                            
            def spawn_tiehunter():
                if level >= 7:
                    wave_length = int(fleet_length/4)
                    for i in range(wave_length):
                        x = random.randrange(50,WIDTH-SMALL-50,SMALL)
                        y = random.randrange(-400-SMALL*level,-100,SMALL)                      
                        tiehunter = TieHunter(x,y)
                        
                        for enemy in gl.fleet:
                            if enemy.x == x and enemy.y == y:
                                gl.fleet.remove(enemy)                           
                        
                        gl.fleet.append(tiehunter)
                    del gl.fleet[0:wave_length]
            
            def spawn_imperialshuttle():
                if level >= 4:
                    wave_length = int(fleet_length/5)
                    for i in range(wave_length):
                        x = random.randrange(50,WIDTH-100-50,100)
                        y = random.randrange(-300-50*level,-100,200)  
                        shuttle = ImperialShuttle(x,y)
                    
                        for enemy in gl.fleet:
                            if enemy.x == x and enemy.y == y:
                                gl.fleet.remove(enemy) 
                        
                        gl.fleet.append(shuttle)
                    del gl.fleet[0:wave_length]           
            
            def spawn_stardestroyer():
                if level >= 11:
                    wave_length = int(fleet_length/6)
                    for i in range(wave_length):
                        x = random.randrange(50,WIDTH-SMALL-50,MEDIUM)
                        y = random.randrange(-300-SMALL*level,-100,200)                      
                        stardes = StarDestroyer(x,y)
                        
                        for enemy in gl.fleet:
                            if enemy.x == x and enemy.y == y:
                                gl.fleet.remove(enemy)                                             
                        
                        gl.fleet.append(stardes)
                    del gl.fleet[0:wave_length]
                        
            def spawn_deathstar():
                if level == 10:
                    x = WIDTH/2-100
                    y = -300
                    deathstar = Deathstar(x,y,500)                       
                    gl.fleet.append(deathstar)     
            
            def spawn_slaveone():
                if level == 20:
                    for i in range(int(1)):
                        x = random.randrange(50,WIDTH-100-50,100)
                        y = random.randrange(-700-100*level,-100,100)                      
                        slaveone = SlaveOne(x,y)
                        
                        for enemy in gl.fleet:
                            if enemy.x == x and enemy.y == y:
                                gl.fleet.remove(enemy)                       
                        
                        gl.fleet.append(slaveone) 
            
            def spawn_powerups():

                choose = random.randrange(1,31)
                
                if choose <= 10:
                    x = random.randrange(0,WIDTH-50)
                    y = -100
                    pu = BB8(x,y)
                    gl.power_ups.append(pu)
                
                if choose >= 11 and choose <= 20:
                    x = random.randrange(0,WIDTH-50)
                    y = -100
                    pu = R5D4(x,y)
                    gl.power_ups.append(pu)
                
                if choose >= 21 and choose <=30:
                    x = random.randrange(0,WIDTH-50)
                    y = -100
                    pu = R2D2(x,y)
                    gl.power_ups.append(pu)
                    
            if len(gl.fleet) == 0:
                spawn_powerups()
            
            spawn_tiefighter()
            spawn_imperialshuttle()
            spawn_tiehunter()            
            spawn_stardestroyer()
            spawn_deathstar()
            spawn_slaveone()
            
        if not pygame.get_init():  
            active = False
            break        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
        if not active:
            break

# Steuerung Arcade              

        if pygame.joystick.get_count() > 0:
         
            if joystick.get_axis(0) < -0.5: #links
                player.x -= player.vel
                player.ship_img = player.ship_img_l
            
            if joystick.get_axis(0) > 0.5: #rechts
                player.x +=  player.vel
                player.ship_img = player.ship_img_r               

            if not joystick.get_axis(0) < -0.5 and not joystick.get_axis(0) > 0.5: #animation aus
                player.ship_img = player.ship_img_m
                
            if joystick.get_axis(0) < -0.5 and joystick.get_axis(0) > 0.5: #animation aus
                player.ship_img = player.ship_img_m  
                
            if joystick.get_axis(1) < -0.5: #hoch
                player.y -= player.vel
                
            if joystick.get_axis(1) > 0.5: #runter
                player.y +=  player.vel
                
            if not joystick.get_button(1):
               released = True  
            
            if joystick.get_button(1):
                if released:
                    player.shoot()
                    released = False
            
            if joystick.get_button(2):
                active = False
                pygame.quit()
            
            if joystick.get_button(3):
                pause_menu()
                if not pygame.get_init():
                    break               

# Steuerung Tastatur
        
        if pygame.joystick.get_count() == 0:

            keys = pygame.key.get_pressed()        
            
            if keys[pygame.K_a]: #links
                player.x -= player.vel
                player.ship_img = player.ship_img_l
                    
            if keys[pygame.K_d]: #rechts
                player.x +=  player.vel
                player.ship_img = player.ship_img_r
                
            if not keys[pygame.K_d] and not keys[pygame.K_a]: #animation aus
                player.ship_img = player.ship_img_m
                
            if keys[pygame.K_a] and keys[pygame.K_d]: #animation aus
                player.ship_img = player.ship_img_m
                           
            if keys[pygame.K_w]: #hoch
                player.y -= player.vel
                
            if keys[pygame.K_s]: #runter
                player.y +=  player.vel
                
            if not keys[pygame.K_l]: #schuss freigeben
                released = True
            
            if keys[pygame.K_l]: #schießen
                if released:
                    player.shoot()
                    released = False            
                
            if keys[pygame.K_p]: #pause
                pause_menu()
                if not pygame.get_init():
                    break
            
            if keys[pygame.K_z]:
                clock.tick(6)
                
            if keys[pygame.K_q]:
                active = False
                pygame.quit()
            
            if keys[pygame.K_b]:
                player.hp = 0
                gl.lives = 0
                lost = True

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
        for pu in gl.power_ups:            
            pu.move()
            if collide(pu,player):
                pu.bonus()
                gl.power_ups.remove(pu)
        
        for enemy in gl.fleet[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if enemy.laser_img == RED_LASER or enemy.laser_img == RED_LASER_BIG:        
                if enemy.y >= 0 and random.randrange(0, FPS*2) == 1:
                    enemy.shoot()                    
            
            if enemy.y + enemy.get_height() > HEIGHT+50:
                write("LIVES -1!",enemy.x,enemy.y-250)
                gl.fleet.remove(enemy)
                if enemy.is_ship:
                    gl.lives -= 1
                    
            if collide(enemy, player):
                player.hp -= enemy.attack
                enemy.hp -= player.attack               
                if enemy.hp >= 0:
                    player.score += enemy.score_value
                if enemy.is_ship:    
                    explosion = Explosion(enemy.x,enemy.y)
                    gl.explosions.append(explosion)
                    gl.fleet.remove(enemy) 
            
            try:
                if enemy.explosion_counter >= 9.5:
                    gl.fleet.remove(enemy)
            except AttributeError:
                pass

# +++PUNKTE FENSTER+++

def score_window():
    highscore_list   = []
    
    highscores = open(path(main_folder,assets, "highscores.txt"),'a')
    highscores.write(str(player.final_score) + "\n")
    highscores.close()
    highscores = open(path(main_folder,assets, "highscores.txt"),'r')
    score_list = highscores.readlines()
    
    for score in score_list:
        score = int(score.strip())
        highscore_list.append(score)
    
    highscore_list = sorted(highscore_list, reverse = True)
    del highscore_list[10:]
   
    def highscore():
        hl_index = 0        
        
        font = pygame.font.Font(path(main_folder,assets, "FGM.ttf"), 50)
                
        for score in highscore_list:                
            
            top_score = highscore_list[hl_index]            
            if score == player.final_score:
                label = font.render(f"{top_score}",1,LIGHT_BLUE)
            else:    
                label = font.render(f"{top_score}",1,ORANGE)           
            screen.blit(label,(WIDTH/2-label.get_width()+140,400 + hl_index*55))

            hl_index += 1
    
    active = True      
    while active:
        
        clock.tick(15)
        screen.blit(BG,(0,0))
        screen.blit(YELLOWBUTTON, (443,189))
        screen.blit(BLUEBUTTON, (724,189))
        
        write("SPACE WARS","center",50,120,YELLOW)
        write('Press "   " to restart or "   " to close',"center",200)
        write(f'FINAL SCORE:{player.final_score}',"center",250,80,ORANGE)
        write("HIGHSCORES:","center",350,50,ORANGE)
        
        highscore()         
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
        
        if not active:
            break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_l] or joystick.get_button(1):
            active = False
            player.hp = 100
            player.x = WIDTH / 2 - player.get_width() / 2
            player.y = 800
            player.score = 0
            player.final_score = None
            player.ship_img = player.ship_img_m
            music.unpause()
            gl.fleet = []
            gl.power_ups = []
            gl.infos = []
            game_loop()
        
        if  keys[pygame.K_q] or joystick.get_button(2):
            active = False
            pygame.quit()
            
        if keys[pygame.K_w]:
            pass
        if keys[pygame.K_s]:
            pass
        if keys[pygame.K_y]:
            pass
        if keys[pygame.K_x]:
            pass

# +++PAUSE+++        

def pause_menu():
    music.pause()
    
    active = True    
    while active:
        clock.tick(15)
        
        screen.blit(BG,(0,0))
              
        write('Press "   " to continue',"center",500)
        write("PAUSED","center",350,80,YELLOW)
        write('Press "   " to close',"center",570)
       
        screen.blit(YELLOWBUTTON, (554,489))
        screen.blit(BLUEBUTTON, (584,559))
        
        pygame.display.update()
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
                
        if not active:
            break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_l] or joystick.get_button(1):
            active = False
        
        if keys[pygame.K_q] or joystick.get_button(2):
            pygame.quit()
            active = False
      
    if pygame.get_init():
        music.unpause()

main_menu()

raise SystemExit