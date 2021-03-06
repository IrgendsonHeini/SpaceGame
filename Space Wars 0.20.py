# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 09:25:13 2021

@author: jstrittmatter
"""

# +++IMPORTS+++
import pygame
import os
import random

pygame.init()
pygame.joystick.init()

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

# Schiffe
load                = pygame.image.load
scale               = pygame.transform.scale
path                = os.path.join
TIE_FIGHTER         = load(path("Space Wars assets", "Tie-Fighter.png"))
TIE_HUNTER          = load(path("Space Wars assets", "Tie-Hunter.png"))
STAR_DESTROYER      = load(path("Space Wars assets", "Star-Destroyer.png"))
DEATHSTAR           = load(path("Space Wars assets", "Death-Star.png"))
MILLENNIUM_FALCON   = load(path("Space Wars assets", "Millennium-Falcon.png"))
MILLENNIUM_FALCON_L = load(path("Space Wars assets", "Millennium-Falcon-left.png"))
MILLENNIUM_FALCON_R = load(path("Space Wars assets", "Millennium-Falcon-right.png"))
IMPERIAL_SHUTTLE    = load(path("Space Wars assets", "Imperial-Shuttle.png"))
SLAVE_I             = load(path("Space Wars assets", "Slave-I.png"))
TRAIL               = load(path("Space Wars assets", "trail.png"))
PLACEHOLDER         = scale(load(path("Space Wars assets", "placeholder.png")),(100,100))


# Laser
GREEN_LASER   = load(path("Space Wars assets", "Laser green.png"))
RED_LASER     = load(path("Space Wars assets", "Laser red.png"))
RED_LASER_BIG = scale(RED_LASER,(50,50))

# Explosionen Bilder (Animation)
EXPLOSION_01 = scale(load(path("Space Wars assets", "Explosion01.png")),(SMALL,SMALL))
EXPLOSION_02 = scale(load(path("Space Wars assets", "Explosion02.png")),(SMALL,SMALL))
EXPLOSION_03 = scale(load(path("Space Wars assets", "Explosion03.png")),(SMALL,SMALL))
EXPLOSION_04 = scale(load(path("Space Wars assets", "Explosion04.png")),(SMALL,SMALL))
EXPLOSION_05 = scale(load(path("Space Wars assets", "Explosion05.png")),(SMALL,SMALL))
EXPLOSION_06 = scale(load(path("Space Wars assets", "Explosion06.png")),(SMALL,SMALL))
EXPLOSION_07 = scale(load(path("Space Wars assets", "Explosion07.png")),(SMALL,SMALL))
EXPLOSION_08 = scale(load(path("Space Wars assets", "Explosion08.png")),(SMALL,SMALL))
EXPLOSION_09 = scale(load(path("Space Wars assets", "Explosion09.png")),(SMALL,SMALL))
EXPLOSION_10 = scale(load(path("Space Wars assets", "Explosion10.png")),(SMALL,SMALL))
EXPLOSION    = [EXPLOSION_01,
                EXPLOSION_02,
                EXPLOSION_03,
                EXPLOSION_04,
                EXPLOSION_05,
                EXPLOSION_06,
                EXPLOSION_07,
                EXPLOSION_08,                    
                EXPLOSION_09,
                EXPLOSION_10]                    

# Explosionen (Ger??usche)
EXPLOSION_ENEMY  = pygame.mixer.Sound("Space Wars assets/Explosion-Enemy.wav")
EXPLOSION_PLAYER = pygame.mixer.Sound("Space Wars assets/Explosion-Player.wav")
EXPLOSION_ENEMY.set_volume(0.5)
EXPLOSION_PLAYER.set_volume(0.7)

# Deathstar (Animation)
DEATHRAY_01 = load(path("Space Wars assets", "Deathray-01.png"))
DEATHRAY_02 = load(path("Space Wars assets", "Deathray-02.png"))
DEATHRAY_03 = load(path("Space Wars assets", "Deathray-03.png"))
DEATHRAY_04 = load(path("Space Wars assets", "Deathray-04.png"))
DEATHRAY_05 = load(path("Space Wars assets", "Deathray-05.png"))
DEATHRAY_06 = load(path("Space Wars assets", "Deathray-06.png"))
DEATHRAY_07 = load(path("Space Wars assets", "Deathray-07.png"))
DEATHRAY_08 = load(path("Space Wars assets", "Deathray-08.png"))
DEATHRAY_09 = load(path("Space Wars assets", "Deathray-09.png"))
DEATHRAY_10 = load(path("Space Wars assets", "Deathray-10.png"))
DEATHRAY_11 = load(path("Space Wars assets", "Deathray-11.png"))
DEATHRAY_12 = load(path("Space Wars assets", "Deathray-12.png"))
DEATHRAY_13 = load(path("Space Wars assets", "Deathray-13.png"))
DEATHRAY_14 = load(path("Space Wars assets", "Deathray-14.png"))
DEATHRAY_15 = load(path("Space Wars assets", "Deathray-15.png"))
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

JOYSTICK = scale(load(path("Space Wars assets", "Joystick.png")),(30,40))
YELLOWBUTTON = scale(load(path("Space Wars assets", "Yellow-Button.png")),(30,40))
BG = scale(load(path("Space Wars assets", "Hintergrund.jpg")),(WIDTH,HEIGHT))

# +++KLASSEN+++

class Laser:
    def __init__(self,x,y,img,attack=10,vel=8):
        self.x    = x
        self.y    = y
        self.img  = img
        self.mask = pygame.mask.from_surface(self.img.convert_alpha())
        self.attack = attack
        self.vel = vel
    def draw(self,window):
        window.blit(self.img,(self.x, self.y))
    
    def move(self,vel):
        self.y += self.vel
    
    def off_screen(self, height):
        return not self.y <= height and self.y >= 0
    
    def collision(self,obj):
        if self.img == GREEN_LASER:
            return collide(self, obj)
        else:
            return collide(self, obj)

class GameLogic:
    def __init__(self):
        self.lasers     = []
        self.explosions = []
        self.fleet      = []

class Ship:
    COOLDOWN = 60
    def __init__(self, x, y, hp = 10):
        self.x         = x
        self.y         = y
        self.hp        = hp
        self.ship_img  = PLACEHOLDER
        self.laser_img = PLACEHOLDER
        self.lasers    = []
        self.max_hp    = hp
        self.attack    = 10                   
        self.size      = 100
        self.score_value = 10
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

class DeathrayExplosion(Ship):
    counter = 0
    def __init__(self,x,y,hp = 1):
        self.ship_img = EXPLOSION
        self.attack = 30
        
    def move(self):
        self.y += 0
    
    def draw(self,x,y):
        screen.blit(self.ship_img[int(self.counter)],(x,y))       
        self.counter += 0.5
        if self.counter > 15:
            self.hp = 0
        

class Player(Ship):
    COOLDOWN = 8
    def __init__(self,x,y,hp=100):
        super().__init__(x,y,hp)
        self.ship_img    = MILLENNIUM_FALCON
        self.laser_img   = GREEN_LASER 
        self.score       = 0
        self.final_score = None
        self.size        = 100
        self.mask        = pygame.mask.from_surface(self.ship_img.convert_alpha())
    
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
    
    def hp_bar(self, window):
        pygame.draw.rect(window,RED,  (self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(), 10))
        pygame.draw.rect(window,BRIGHT_GREEN,(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width()*(self.hp/self.max_hp),10))

    def draw(self, window):
        super().draw(window)
        self.hp_bar(window)
        
        for explosion in gl.explosions:
            explosion.draw(screen)
            if explosion.counter >= 10:
                gl.explosions.remove(explosion)
        
class TieFighter(Ship):
    def __init__(self,x,y,hp=10):
        super().__init__(x,y,hp)
        self.ship_img    = TIE_FIGHTER  
        self.score_value = 10
        self.size        = 75
        self.mask        = pygame.mask.from_surface(self.ship_img.convert_alpha())
        
class TieHunter(Ship):
    def __init__(self,x,y,hp=10):
        super().__init__(x,y,hp)
        self.ship_img    = TIE_HUNTER
        self.laser_img   = RED_LASER
        self.score_value = 20
        self.size        = 75
        self.mask      = pygame.mask.from_surface(self.ship_img.convert_alpha())
        
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
        self.ship_img    = STAR_DESTROYER
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
   
    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)
            
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
    def __init__(self,x,y,hp=1000):
        super().__init__(x,y,hp)
        self.ship_img    = DEATHSTAR
        self.size        = 200
        self.target_x    = None
        self.target_y    = None        
        self.attack      = 100
        self.score_value = 1000
        self.mask        = pygame.mask.from_surface(self.ship_img.convert_alpha())
        self.laser_img   = "Big fat green laser!"
        self.target_location = (player.x+50,player.y+50)
    
    def move(self,vel):
        if self.y + vel < 50:
            self.y += vel
        else:
            self.y = 50           

    def hp_bar(self, window):
        pygame.draw.rect(window,RED,         (self.x,self.y-15,self.ship_img.get_width(),                      15))
        pygame.draw.rect(window,BRIGHT_GREEN,(self.x,self.y-15,self.ship_img.get_width()*(self.hp/self.max_hp),15))
    
    def draw(self, window):
        super().draw(window)
        self.hp_bar(window)
    
    def shoot(self):    
        self.counter += 0.25
        
        if self.counter == 13:
            self.target_location = (player.x+50,player.y+50)
            self.target_x        = player.x
            self.target_y        = player.y
        
        if self.counter > 0 and self.counter <= 14.5:
            screen.blit(DEATHRAY[int(self.counter)],(self.x,self.y))
        
        if self.counter >= 15:
            screen.blit(DEATHRAY[14],(self.x,self.y))
            pygame.draw.line(screen,GREEN,(self.x+98,self.y+58),self.target_location,4)
            explosion = DeathrayExplosion(self.target_x, self.target_y,1)
            gl.fleet.append(explosion)   
            
        
        if self.counter >= 20:
            self.counter = -30

class Slave_I(Ship):
    COOLDOWN = 30
    def __init__(self,x,y,hp=50):
        super().__init__(x,y,hp)
        self.ship_img  = SLAVE_I
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
            
class ImperialShuttle(Slave_I):
    def __init__(self,x,y,hp=30):
        super().__init__(x,y,hp) 
        self.ship_img    = IMPERIAL_SHUTTLE
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
    def __init__(self,x,y,size=75):
        self.x = x
        self.y = y
        self.size = size  
        self.attack = 30
        self.img = EXPLOSION
        self.counter = 0
        
    def draw(self, window):              
        window.blit(scale(self.img[int(self.counter)],(self.size,self.size)),(self.x,self.y))      
        self.counter += 0.5
        if self.counter >= 10:
            return False
    
    def move(self):
        pass

# +++FUNKTIONEN+++      

def collide(obj1, obj2):  
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y  
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None  

# +++VARIABLEN+++
clock = pygame.time.Clock()
player = Player(WIDTH / 2 - 50,800)
gl = GameLogic()

# +++MUSIK+++
music = pygame.mixer.music
music.load("Space Wars assets/background-music.wav")
music.set_volume(0.3)
music.play(-1,0.0)

# +++HAUPTMEN??+++
def main_menu():
    space_wars_font  = pygame.font.SysFont("franklingothicmedium", 120)
    instruction_font = pygame.font.SysFont("franklingothicmedium", 40)

    space_wars_label = space_wars_font.render("SPACE WARS",1,YELLOW)  
    instruction      = instruction_font.render('Use "   " to move and "   " to shoot',1,WHITE)
    instruction2     = instruction_font.render('Press "   " to start',1,WHITE)    
    counter = 0
    
    active = True
    while active:
        counter += 1
        
        clock.tick(20)
        screen.blit(BG,(0,0))
        screen.blit(instruction,(WIDTH/2-(instruction.get_width()/2),400))
        
        screen.blit(JOYSTICK,(440,405))
        screen.blit(YELLOWBUTTON,(735,405))
        
        if counter < 15:
            screen.blit(instruction2,(WIDTH/2-(instruction2.get_width()/2),470))
            screen.blit(YELLOWBUTTON,(610,475))
        
        if counter >= 20:
            counter = 0
        
        screen.blit(space_wars_label,(WIDTH/2-space_wars_label.get_width()/2,200))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
        if not active:
            break            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            active = False
            game_loop()
                
# +++HAUPTSCHLEIFE+++

def game_loop():
    active = True
    lost = False
    lost_count = 0
    lives = 5
    level = 0
    fleet_length = 4
    player_vel = 10
    enemy_vel  = 1
    laser_vel = 8
    main_font = pygame.font.SysFont("franklingothicmedium", 50)
    lost_font = pygame.font.SysFont("franklingothicmedium", 140)           
    player.score = 0
    released = True    
    
    def redraw_window():
            
        lives_label = main_font.render(f"LIVES: {lives}",1,ORANGE)
        score_label = main_font.render(f"SCORE: {player.score}",1,ORANGE)        
        
        screen.blit(BG,(0,0))
        
        for enemy in gl.fleet:
            enemy.draw(screen)
    
        player.draw(screen)
        
        player.move_lasers(-laser_vel*2, gl.fleet)
        
        screen.blit(lives_label,(10,10))
        screen.blit(score_label,(WIDTH-score_label.get_width()-10,10))
        
        if lost:
            lost_label = lost_font.render("GAME OVER",1,(200,  0,  0))
            screen.blit(lost_label,(WIDTH/2-lost_label.get_width()/2,HEIGHT/2-lost_label.get_height()/2))            
        
        pygame.display.update()
# Hauptschleife
    while active:
        clock.tick(FPS)
        redraw_window()
        if lives <= 0 or player.hp <= 0:
            lost = True

# Game over       
       
        if lost:
            music.pause()
           
            if lost_count == 0:
                player.final_score = player.score
                player.ship_img = EXPLOSION[0]  
                pygame.mixer.Sound.play(EXPLOSION_PLAYER,0)                            
            
            if lost_count == 3:
                player.ship_img = EXPLOSION[1]
            if lost_count == 6:
                player.ship_img = EXPLOSION[2]
            if lost_count == 9:
                player.ship_img = EXPLOSION[3]            
            if lost_count == 12:
                player.ship_img = EXPLOSION[4]
            if lost_count == 15:
                player.ship_img = EXPLOSION[5]
            if lost_count == 18:
                player.ship_img = EXPLOSION[6]
            if lost_count == 21:
                player.ship_img = EXPLOSION[7]
            if lost_count == 24:
                player.ship_img = EXPLOSION[8]
            if lost_count == 27:
                player.ship_img = EXPLOSION[9]
            
            lost_count += 1                
            if lost_count > FPS*3:
                active = False
                score_window()
            else:
                continue
        
# Gegner einf??gen
        
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
                if level >= 13:
                    wave_length = int(fleet_length/6)
                    for i in range(wave_length):
                        x = random.randrange(50,WIDTH-SMALL-50,MEDIUM)
                        y = random.randrange(-300-SMALL*level,-100,MEDIUM)                      
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
                    deathstar = Deathstar(x,y,100)                       
                    gl.fleet.append(deathstar)     
            
            def spawn_slavei():
                if level >= 0:
                    for i in range(int(1)):
                        x = random.randrange(50,WIDTH-100-50,100)
                        y = random.randrange(-700-100*level,-100,100)                      
                        slavei = Slave_I(x,y)
                        
                        for enemy in gl.fleet:
                            if enemy.x == x and enemy.y == y:
                                gl.fleet.remove(enemy)                       
                        
                        gl.fleet.append(slavei) 
                                            
            spawn_tiefighter()
            spawn_imperialshuttle()
            spawn_tiehunter()            
            spawn_stardestroyer()
            #spawn_deathstar()
            #spawn_slavei()
            
        if not pygame.get_init():  
            active = False
            break        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
        if not active:
            break

# Steuerung                

        keys = pygame.key.get_pressed()        
        
        if keys[pygame.K_LEFT]:
            player.x -= player_vel
            player.ship_img = MILLENNIUM_FALCON_L
                
        if keys[pygame.K_RIGHT]:
            player.x +=  player_vel
            player.ship_img = MILLENNIUM_FALCON_R
            
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            player.ship_img = MILLENNIUM_FALCON
            
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            player.ship_img = MILLENNIUM_FALCON
                       
        if keys[pygame.K_UP]:
            player.y -= player_vel
            
        if keys[pygame.K_DOWN]:
            player.y +=  player_vel
            
        if not keys[pygame.K_s]:
            released = True
        
        if keys[pygame.K_s]:
            if released:
                player.shoot()
                released = False            
            
        if keys[pygame.K_ESCAPE]:
            pause_menu()
            if not pygame.get_init():
                break
        if keys[pygame.K_z]:
            clock.tick(6)
        
        if keys[pygame.K_b]:
            player.hp = 0
            lives = 0
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
        
        for enemy in gl.fleet[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if enemy.laser_img == RED_LASER or enemy.laser_img == RED_LASER_BIG:            
                if enemy.y >= 0 and random.randrange(0, FPS*2) == 1:
                    enemy.shoot()                    
            
            if enemy.y + enemy.get_height() > HEIGHT+50:
                lives -= 1
                gl.fleet.remove(enemy)

            if collide(enemy, player):
                player.hp -= enemy.attack
                enemy.hp -= player.attack               
                if enemy.hp >= 0:
                    player.score += enemy.score_value
                    explosion = Explosion(enemy.x,enemy.y)
                    gl.explosions.append(explosion)
                    gl.fleet.remove(enemy)   

# +++PUNKTE FENSTER+++

def score_window():
    highscore_list   = []
    space_wars_font  = pygame.font.SysFont("franklingothicmedium", 120)
    score_font       = pygame.font.SysFont("franklingothicmedium",  80)
    instruction_font = pygame.font.SysFont("franklingothicmedium",  40)
    highscore_font   = pygame.font.SysFont("franklingothicmedium",  50)

    space_wars_label = space_wars_font.render("SPACE WARS",1,YELLOW)  
    score_label      = score_font.render(f'FINAL SCORE:{player.final_score}',1,ORANGE)

    instruction      = instruction_font.render('Press "S" to restart or "ESC" to close',1,WHITE)
    
    highscores = open('C:/Users/jstrittmatter/.spyder-py3/Space Wars assets/highscores.txt','a')
    highscores.write(str(player.final_score) + "\n")
    highscores.close()
    highscores = open('C:/Users/jstrittmatter/.spyder-py3/Space Wars assets/highscores.txt','r')
    score_list = highscores.readlines()
    
    for score in score_list:
        score = int(score.strip())
        highscore_list.append(score)
    
    highscore_list = sorted(highscore_list, reverse = True)
    del highscore_list[10:]
    
    highscore_label = highscore_font.render("HIGHSCORES:",1,ORANGE)
   
    def highscore():
        hl_index = 0        
        
        font = pygame.font.SysFont("franklingothicmedium", 50)
                
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
        screen.blit(score_label, (WIDTH / 2 - score_label.get_width() / 2, 250))
        screen.blit(instruction,(WIDTH/2-instruction.get_width()/2,200))        
        screen.blit(highscore_label, (WIDTH / 2 - highscore_label.get_width() / 2, 350))
        
        highscore()         
        
        screen.blit(space_wars_label, (WIDTH / 2 - space_wars_label.get_width() / 2, 50))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
        
        if not active:
            break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            active = False
            player.hp = 100
            player.x = WIDTH / 2 - player.get_width() / 2
            player.y = 800
            player.score = 0
            player.final_score = None
            player.ship_img = MILLENNIUM_FALCON
            music.unpause()
            game_loop()
        
        if keys[pygame.K_ESCAPE]:
            active = False
            pygame.quit()

# +++PAUSE+++        

def pause_menu():
    music.pause()
    
    instruction_font = pygame.font.SysFont("franklingothicmedium", 40)
    paused = pygame.font.SysFont("franklingothicmedium",80).render("PAUSED",1,YELLOW)
    instruction = instruction_font.render('Press "YELLOW" to continue',1,WHITE)
    
    active = True    
    while active:
        clock.tick(15)
        screen.blit(BG,(0,0))
        screen.blit(paused, (WIDTH / 2 - paused.get_width() / 2, 400))
        screen.blit(instruction, (WIDTH / 2 - instruction.get_width() / 2, 500))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
                
        if not active:
            break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            active = False
    if pygame.get_init():
        music.unpause()

main_menu()







