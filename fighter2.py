import pygame
import random
class Fighter():
    def __init__(self,player,x,y,flip, data,sprite_sheet, animation_steps,sound):
        self.player=player
        self.size=data[0]
        self.image_scale=data[1]
        self.offset= data[2]
        self.flip=flip
        self.animation_list=self.load_images(sprite_sheet, animation_steps)
        self.action= 0 # 0: attack1, 1:attack2, 2:death, 3:jump, 4:hit, 5:idle, 6:run  
        self.frame_index= 0
        self.images=self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect=pygame.Rect((x,y,80,180))
        self.vel_y =0
        self.running=False
        self.jump = False
        self.attacking=False
        self.attack_type=0
        self.attack_cooldown=0
        self.attack_sound= sound
        self.health=20
        self.alive=True
        self.hit =False
        self.clock=pygame.time.Clock()
        # self.wiz1_animation_steps=[11, 8, 3, 7, 7, 4, 11]
        self.rect.center = (x, y)
        # self.rect = self.image.get_rect()
        
    def load_images(self, sprite_sheet, animation_steps):
        #extract images form spritesheeet
        animation_list=[]
        for y, animation in enumerate(animation_steps):
            temp_img_list=[]
            for x in range(animation):
                temp_image=sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_image,(self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        
        return animation_list
     
    def move(self,screen_width,screen_height,surface,target, round_over):
        SPEED=10
        GRAVITY=2
        dx=0
        dy=0
        self.running=False
        self.attack_type=0
        
        last_updated_time=3000
        pygame.time.get_ticks()
        
        #init time variables
        AI_ATTACK_timer = 0  
        AI_JUMP_timer = 0   
        AI_MOVE_timer=0
        current_time = pygame.time.get_ticks()
    
        #get keypress
        key=pygame.key.get_pressed()
        
        #movements will only be performed if not attackin
        if self.attacking==False and self.alive == True and round_over==False:
            
            
            if self.player==1:
            # movement
                if key[pygame.K_LEFT]:
                    dx= -SPEED
                    self.running=True
                if key[pygame.K_RIGHT]:
                    dx= SPEED
                    self.running=True
                    #jumping    
                if key[pygame.K_UP] and self.jump==False:
                    self.vel_y = -30
                    self.jump=True 
                    #attack
                if key[pygame.K_a] or key[pygame.K_s] :
                    self.attack(target)
                    if key[pygame.K_a]:
                        self.attack_type=1
                    if key[pygame.K_s]:
                        self.attack_type=2
                        
                        
            if self.player==2:
                if pygame.time.get_ticks()  - last_updated_time >=2000:
                    SPEED=3
                    self.running=True
                   
                    List=list(range(1,101))
                    rlist=random.choice(List)
                    print(rlist)
                    if rlist == 11:
                        self.jump = True
                        self.vel_y=-30
                        # self.running=False
                    # if rlist == 22:
                    #     self.attack_type=2
                    #     self.attack(target,surface)
                    # self.running=False
                            
                    dx=-SPEED
                    print("running")
                    last_updated_time=pygame.time.get_ticks()
                    print(pygame.time.get_ticks(), last_updated_time)
                    if target.rect.centerx > self.rect.centerx:
                        self.running=True
                        self.flip=False 
                        dx=SPEED
                        print("target rect", target.rect.centerx)
                        print("rect", self.rect.centerx)
                        # if target.rect.centerx > self.rect.centerx:
                        #     dx=0
                        if target.rect.centerx - self.rect.centerx <=10:
                            self.running=False
                            dx=0
                            num=[1,2]
                            rnum=random.choice(num)
                            print("1st",rnum)
                            if rnum ==1:
                                self.attack_type=1
                                self.attack(target)
                                self.attack_cooldown=10
                            elif rnum == 2:
                                self.attack_type=2
                                self.attack(target)
                                self.attack_cooldown=10
                
            #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
            
        #ensure player stays onscreen
        
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
            
        if self.rect.bottom +dy > screen_height - 110:
            self.vel_y=0
            self.jump=False
            dy= screen_height -110 -self.rect.bottom
            
            #ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip=False
        else:
            self.flip=True
        #update player position
        
    #apply attack cooldown 
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.rect.x +=dx
        self.rect.y +=dy
        
    def update(self):
        if self.health==0:
            self.health =0
            self.alive=False
            self.update_action(6) 
        elif self.hit == True:
             self.update_action(5)
        elif self.attacking==True:
            if self.attack_type ==1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
                
        elif self.jump==True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)
        # check what action the player is performing
        
        animation_cooldown = 50
        self.images=self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time=pygame.time.get_ticks()
         #check if the animatin has finished         
        if self.frame_index >= len(self.animation_list[self.action]):
            #if player s dead end animation
            if self.alive == False:
                self.frame_index= len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action==4:
                    self.attacking=False
                    self.attack_cooldown=20    
                if self.action ==5:
                    self.hit = False
                    # if the player was in the middle of attack
                    self.attacking=False
                    self.attack_cooldown=20
                 
    def attack(self,target):
        if self.attack_cooldown==0:
            #exe attack sound
            
            self.attacking =True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx-(2 * self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -=10
                target.hit=True
            # pygame.draw.rect(surface,(0,255,0),attacking_rect)
        
     
    def update_action(self, new_action):
        #check new action is different then new one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
        
    def draw(self, surface):
        img=pygame.transform.flip(self.images, self.flip, False)
        # pygame.draw.rect(surface, (255,0,0),self.rect)
        surface.blit(img,(self.rect.x-(self.offset[0] - self.image_scale), self.rect.y- (self.offset[1] - self.image_scale)))
        




# 11, 8, 3, 7, 7, 4, 11