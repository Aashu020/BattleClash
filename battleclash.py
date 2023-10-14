import pygame
from fighter2 import Fighter

from pygame import mixer

pygame.init()

screen_width=1000
screen_height=600

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('BattleClash')

#set framerate
clock=pygame.time.Clock()
FPS=60

#define color
YELLOW=(255,255,0)
RED=(255,0,0)
WHITE=(255,255,255)

#define variables
intro_count=3
score=[0,0]
round_over=False
last_count_update=pygame.time.get_ticks()
ROUND_OVER_COOLDOWN=2000
game_active=True

#define fighter variable
hero1_size=162
hero1_scale=4
hero1_offset=[263,208]
hero1_data=[hero1_size,hero1_scale,hero1_offset]
wiz1_size= 250
wiz1_scale=3
wiz1_offset=[340,310]
wiz1_data=[wiz1_size,wiz1_scale,wiz1_offset]

bg_image=pygame.image.load("C:/Users/acer/OneDrive/Documents/arif/logform/additonalsfeatures/b.jpg").convert_alpha()

#Load images
hero1_sheet= pygame.image.load("C:/Users/acer/OneDrive/Documents/arif/logform/battleclash/warrior.png").convert_alpha()
wiz1_sheet= pygame.image.load("C:/Users/acer/OneDrive/Documents/arif/logform/additonalsfeatures/wizard.png").convert_alpha()
             

#steps in animation
hero1_animation_steps=[10, 8, 1, 7, 7, 3, 7]
wiz1_animation_steps=[8, 8, 1, 8, 8,3 , 7]

#load music
pygame.mixer.music.load("c:/Users/acer/OneDrive/Documents/arif/logform/battleclash/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0.0, 5000) 
sword_fx=pygame.mixer.Sound("c:/Users/acer/OneDrive/Documents/arif/logform/battleclash/sword.wav")
sword_fx.set_volume(0.75)
magic_fx=pygame.mixer.Sound("c:/Users/acer/OneDrive/Documents/arif/logform/battleclash/magic.wav")
magic_fx.set_volume(0.75)


#define font
count_font=pygame.font.Font("c:/Users/acer/OneDrive/Documents/arif/logform/battleclash/turok.ttf", 100)
score_font=pygame.font.Font("c:/Users/acer/OneDrive/Documents/arif/logform/battleclash/turok.ttf", 50)

def draw_bg():
    scaled_bg=pygame.transform.scale(bg_image,(screen_width,screen_height))
    screen.blit(scaled_bg,(0,0))

def draw_health_bar(health, x, y):
    ratio=health / 100
    pygame.draw.rect(screen,WHITE,(x-2,y-2, 404,34))
    pygame.draw.rect(screen,RED,(x,y, 400,30))
    pygame.draw.rect(screen,YELLOW,(x,y, 400 * ratio, 30))
    
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))

fighter_1=Fighter(1,250,400,False,hero1_data, hero1_sheet, hero1_animation_steps,sword_fx)
fighter_2=Fighter(2,650,400,True,wiz1_data,wiz1_sheet, wiz1_animation_steps,magic_fx)
# keys= pygame.key.get_pressed()zzzz
run=True
while run:
    # print(screen_width)
    for event in pygame.event.get():
        
        
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN: 
            keys= pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and game_active==True:
                game_active=False
                # print('sp')
                draw_bg()
                draw_text("Press V to Resume and v to Quit ", score_font, RED, 400,150)
    if game_active:
        clock.tick(FPS)        
        draw_bg()
        draw_health_bar(fighter_1.health,20,20)
        draw_health_bar(fighter_2.health,580,20)
        draw_text("P1: "+ str(score[0]), score_font, RED, 20,60)
        draw_text("P2: "+ str(score[1]), score_font, RED, 580,60)
        if intro_count <=0:     
           
            fighter_1.move(screen_width,screen_height,screen,fighter_2,round_over)
            fighter_2.move(screen_width,screen_height,screen,fighter_1,round_over)
        else:
            
            draw_text(str(intro_count),count_font,RED,screen_height/1.3,screen_height/3.5)
            
            if(pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
                print(intro_count)
        
        fighter_1.update()
        fighter_2.update()           
        fighter_1.draw(screen)
        fighter_2.draw(screen)    
        
        if round_over==False:
            if fighter_1.alive==False:
                round_over_time=pygame.time.get_ticks()
                round_over=False
                draw_bg()
                # print("p1")
                draw_text("Player B won ", score_font, YELLOW, 400,150)
                draw_text("Press b to Continue and v to Quit", score_font, YELLOW, 200,250) 
                if keys[pygame.K_b]:
                    score[1] +=1
                    game_active=True
                    round_over=True
                if keys[pygame.K_v]:
                    run=False
            
            elif fighter_2.alive==False:
                draw_bg()
                draw_text("Player A won ", score_font, YELLOW, 400,150)
                draw_text("Press b to continue and v to Quit", score_font, YELLOW, 200,250) 
                if keys[pygame.K_b]:                    
                    score[0] +=1                   
                    game_active=True  
                    round_over=True
                    round_over_time=pygame.time.get_ticks()                   
                    # intro_count=3
                if keys[pygame.K_v]:
                    run=False                
        else:             
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over=False
                intro_count= 3               
                fighter_1=Fighter(1,250,400,False,hero1_data, hero1_sheet, hero1_animation_steps,sword_fx)
                fighter_2=Fighter(2,600,400,True,wiz1_data,wiz1_sheet, wiz1_animation_steps,magic_fx)  
    else:
        draw_bg()
        draw_text("Paused", score_font, YELLOW, 400,150)
        draw_text("Press b to Resume and v to Quit", score_font, YELLOW, 190,250)       
        if keys[pygame.K_b]:            
            game_active=True  
        if keys[pygame.K_v]:
            run=False
    pygame.display.update()    
pygame.quit()