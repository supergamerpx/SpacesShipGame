import pygame
import sys
import random
import time


class Player(pygame.sprite.Sprite):
    
    def __init__(self, PlayerPosition):
        
        pygame.sprite.Sprite.__init__(self)

        DEFAULT_IMAGE_SIZE = (150, 150)
        
        self.Playerimage = pygame.transform.smoothscale(pygame.image.load("Graphics/MilitaryJet.png"),DEFAULT_IMAGE_SIZE).convert_alpha()
        
        self.CurrentPlayerPosition = PlayerPosition
        
        self.rect = self.Playerimage.get_rect(topleft = self.CurrentPlayerPosition)
 
    def DisplayImage(self,screen,NewPlayerPosition):
        
        self.CurrentPlayer = screen.blit(self.Playerimage, self.rect)
        
        self.rect = self.Playerimage.get_rect(topleft = self.CurrentPlayerPosition)

        
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self,name,yposition):
        
        pygame.sprite.Sprite.__init__(self)
        
        DEFAULT_IMAGE_SIZE = (100, 100)
        
        self.Name = str(name)
        
        self.Time_of_creation = time.time()
        
        self.EnemyPosition = [800,random.randint(0,yposition)]
        
        self.Enemyimage = pygame.transform.scale(pygame.image.load("Graphics/Enemy.png"),DEFAULT_IMAGE_SIZE).convert_alpha()
        
        self.rect = self.Enemyimage.get_rect(topleft = self.EnemyPosition)
        
        
    def DisplayEnemyImage(self,screen):
                
        self.CurrentEnemy = screen.blit(self.Enemyimage,self.rect)
        
        self.rect = self.Enemyimage.get_rect(topleft = self.EnemyPosition)

                    
class GameText(object):
    
    def __init__(self, text, screen, position, color):
        
        self.Position = position
        
        self.Text_Font = pygame.font.SysFont("monospace",20)
        
        self.Text = self.Text_Font.render(str(text),True, str(color))
        
        self.rect = self.Text.get_rect(midtop = self.Position)
        
        self.CurrentText = screen.blit(self.Text, self.rect.topleft)
        
class Explosion(object):
    
    def __init__(self,explosionPosition):
        

        DEFAULT_IMAGE_SIZE = (150, 150)
        
        self.Explosionimage = pygame.transform.smoothscale(pygame.image.load("Graphics/explosion.png"),DEFAULT_IMAGE_SIZE).convert_alpha()
        
        self.ExplosionPosition = explosionPosition
        
        self.rect = self.Explosionimage.get_rect(topleft = self.ExplosionPosition)
        
        self.sfx = pygame.mixer.Sound("Sound effect/BigExplosionSoundEffect.mp3")
        
        self.StartOfExplosion = 0

        
    def DisplayExplosionImage(self,screen):
        
        self.CurrentExplosion = screen.blit(self.Explosionimage,self.rect)
        
        self.rect = self.Explosionimage.get_rect(midleft = self.ExplosionPosition)
        
    def PlaySoundEffect(self):
        
        self.sfx.play()
        
        pass

class Missile(pygame.sprite.Sprite):
    
    def __init__(self,missilePosition):
        
        pygame.sprite.Sprite.__init__(self)
        
        DEFAULT_IMAGE_SIZE = (100, 100)

        self.Missileimage = pygame.transform.smoothscale(pygame.image.load("Graphics/Missile.png"),DEFAULT_IMAGE_SIZE).convert_alpha()
        
        self.MissilePosition = missilePosition

        self.rect = self.Missileimage.get_rect(midleft = self.MissilePosition)
        
    def DisplayMissileImage(self,screen):
        
        self.CurrentMissile = screen.blit(self.Missileimage,self.rect)
        
        self.rect = self.Missileimage.get_rect(midleft = self.MissilePosition)


        
class Game(object):
    
    def __init__(self):
        
        pygame.init()

        self.clock = pygame.time.Clock()
        
        self.screen_width= 800
        
        self.screen_height= 700
        
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        
        pygame.display.set_caption("SpaceShipGame")
        
        self.backgroundimage = pygame.image.load("Graphics/Sky.jpg")
        
        self.backgroundimage_pos = [0,0]
        
        self.CurrentEnemies = []
        
        self.CurrentMissiles = []
        
        self.CurrentExplosions = []
              
        self.movement = [False,False,False,False]
        
        global CurrentPlayer
        
        CurrentPlayer = Player([0,250])
        
        self.MaxnumofEnemies = 3
        
        self.LastTime_OfMovementOfTheEnemy = 0
        
        self.LastTime_OfSpawnEnemy = 0
        
        self.LastTime_OfMissile = 0
        
        self.EnemyGroup = pygame.sprite.Group()
        
        self.PlayerGroup = pygame.sprite.Group()
        
        self.MissileGroup = pygame.sprite.Group()
                
        self.PlayerGroup.add(CurrentPlayer)
        
        self.CooldownOfSpawningOfEnemies = 3
        
        self.CooldownOfSpawningOfMissile = 1
        
        self.Timethatexplosionshouldexpire = 1
        
        self.SpeedOfEnemies = 1
        
        self.SpeedOfMissiles = 3
        
        self.GameIsActive = True
        

    def run(self):
        
        while self.GameIsActive:
            
            self.screen.blit(self.backgroundimage, self.backgroundimage_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[2] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[3] = True
                    if event.key == pygame.K_SPACE:
                        
                        if int(time.time()) - int(self.LastTime_OfMissile) >= self.CooldownOfSpawningOfMissile:
                        
                            CurrentMissile = Missile(list(CurrentPlayer.rect.midright))
                        
                            self.CurrentMissiles.append(CurrentMissile)
                        
                            self.MissileGroup.add(CurrentMissile)
                        
                            self.LastTime_OfMissile = time.time()
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[2] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[3] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
    
                
            CurrentGameText = GameText("Survive the waves of rocks.", self.screen, (self.screen_width/2,self.screen_width/28), "Black")
            
            CurrentPlayer.CurrentPlayerPosition[1] += (self.movement[1] - self.movement[0]) * 5
            
            CurrentPlayer.CurrentPlayerPosition[0] += (self.movement[2] - self.movement[3]) * 5
            
            CurrentPlayer.DisplayImage(self.screen,CurrentPlayer.CurrentPlayerPosition)
                                
            # Spawns the enemies
            if len(self.CurrentEnemies) < int(self.MaxnumofEnemies) and int(self.LastTime_OfSpawnEnemy) == 0 or int(time.time()) - int(self.LastTime_OfSpawnEnemy) >= self.CooldownOfSpawningOfEnemies:
                
                CurrentEnemy = Enemy("Rocks", self.screen_height)
                CurrentEnemy.DisplayEnemyImage(self.screen)
                
                self.CurrentEnemies.append(CurrentEnemy)
                
                self.LastTime_OfSpawnEnemy = time.time()
                
                self.EnemyGroup.add(CurrentEnemy)
                    
            # I dont need that if statement
            # Moves the enemies
            if int(time.time()) - int(self.LastTime_OfMovementOfTheEnemy) >= 0:
                
                for i in self.CurrentEnemies:
                    
                    i.EnemyPosition[0] -= self.SpeedOfEnemies
                    
                    i.DisplayEnemyImage(self.screen)
                    
                    self.LastTime_OfMovementOfTheEnemy = time.time()
                    
                    if i.EnemyPosition[0] <= 0:
                        
                        self.CurrentEnemies.remove(i)
                        
                        self.EnemyGroup.remove(i)
                        
                        i.kill()
                        
            # This will move the missile
            for missile in self.CurrentMissiles:
                
                missile.MissilePosition[0] += self.SpeedOfMissiles
                
                missile.DisplayMissileImage(self.screen)
                
                if missile.MissilePosition[0] >= self.screen_height:
                    self.MissileGroup.remove(missile)
                    
                    self.CurrentMissiles.remove(missile)
                    
                    missile.kill()
            
            # I'll probl use rect next time.
            if CurrentPlayer.CurrentPlayerPosition[0] <= 0:
                
                CurrentPlayer.CurrentPlayerPosition[0] += 10
            
            if CurrentPlayer.CurrentPlayerPosition[0] >= self.screen_height:
                
                CurrentPlayer.CurrentPlayerPosition[0] -= 10
                
            if CurrentPlayer.CurrentPlayerPosition[1] >= 635:
                
                CurrentPlayer.CurrentPlayerPosition[1] -= 10
                
            if CurrentPlayer.CurrentPlayerPosition[1] <= -60:
                
                 CurrentPlayer.CurrentPlayerPosition[1] += 10
                    
            
            # Check if the CurrentExplosions should expire or not
            for explosion in self.CurrentExplosions:
                
                if int(time.time()) - int(explosion.StartOfExplosion) < int(self.Timethatexplosionshouldexpire):
                    
                    explosion.DisplayExplosionImage(self.screen)
                    
                elif int(time.time()) - int(explosion.StartOfExplosion) >= int(self.Timethatexplosionshouldexpire):
                    
                    self.CurrentExplosions.remove(explosion)
                    
                    
                    
            MissileInContactWithEnemy = pygame.sprite.groupcollide(self.MissileGroup, self.EnemyGroup, False, False)
                
            if MissileInContactWithEnemy:
                
                for missileandrock in MissileInContactWithEnemy.items():
                    
                    CurrentExplosion = Explosion(missileandrock[0].MissilePosition)
                    
                    CurrentExplosion.StartOfExplosion = time.time()
                                        
                    CurrentExplosion.DisplayExplosionImage(self.screen)
                    
                    CurrentExplosion.PlaySoundEffect()
                    
                    self.CurrentExplosions.append(CurrentExplosion)
                    
                    self.MissileGroup.remove(missileandrock[0])
                    
                    self.CurrentMissiles.remove(missileandrock[0])
                    
                    missileandrock[0].kill()
                    
                    self.EnemyGroup.remove(missileandrock[1][0])
                    
                    self.CurrentEnemies.remove(missileandrock[1][0])
                    
                    missileandrock[1][0].kill()
            
            # What would happen if player hits an enemy, it would be the end...
            if pygame.sprite.groupcollide(self.PlayerGroup, self.EnemyGroup, True, True):
                                
                CurrentExplosionsImage = Explosion(CurrentPlayer.CurrentPlayerPosition)
                
                CurrentExplosionsImage.DisplayExplosionImage(self.screen)
                
                CurrentExplosionsImage.PlaySoundEffect()
                
                self.GameIsActive = False
                
            pygame.display.flip()
            
            self.clock.tick(60)

Game().run()


# End of game!
print("You lost the game ....")
