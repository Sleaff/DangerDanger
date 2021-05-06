import pygame, sys, random, math
from pygame.locals import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
VEL = 5

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DangerDanger")

# Surfaces
player_surface = pygame.transform.scale(
    pygame.image.load('assets/idle.png').convert_alpha(), (40, 50))
player_surface_mirror = pygame.transform.flip(
    player_surface, True, False)
player_walk_01 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk01.png').convert_alpha(), (40, 50))
player_walk_02 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk02.png').convert_alpha(), (40, 50))
player_walk_03 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk03.png').convert_alpha(), (40, 50))
player_walk_04 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk04.png').convert_alpha(), (40, 50))
player_walk_05 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk05.png').convert_alpha(), (40, 50))
player_walk_06 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk06.png').convert_alpha(), (40, 50))
player_walk_07 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk07.png').convert_alpha(), (40, 50))
player_walk_08 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk08.png').convert_alpha(), (40, 50))
player_walk_09 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk09.png').convert_alpha(), (40, 50))
player_walk_10 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk10.png').convert_alpha(), (40, 50))
player_walk_11 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk11.png').convert_alpha(), (40, 50))
player_walk_12 = pygame.transform.scale(
    pygame.image.load('assets/walk/walk12.png').convert_alpha(), (40, 50))
player_walk_frames = [player_walk_01, player_walk_02, player_walk_03, player_walk_04, 
                      player_walk_05, player_walk_06, player_walk_07, player_walk_08,
                      player_walk_09, player_walk_10, player_walk_11, player_walk_12]
player_walk_frames_mirror = []
for frame in player_walk_frames:
    mirror = pygame.transform.flip(frame, True, False)
    player_walk_frames_mirror.append(mirror)

enemy_01 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0001.png').convert_alpha(), (40, 50))
enemy_02 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0005.png').convert_alpha(), (40, 50))
enemy_03 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0010.png').convert_alpha(), (40, 50))
enemy_04 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0015.png').convert_alpha(), (40, 50))
enemy_05 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0020.png').convert_alpha(), (40, 50))
enemy_06 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0025.png').convert_alpha(), (40, 50))
enemy_07 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0030.png').convert_alpha(), (40, 50))
enemy_08 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0035.png').convert_alpha(), (40, 50))
enemy_09 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0040.png').convert_alpha(), (40, 50))
enemy_10 = pygame.transform.scale(
    pygame.image.load('assets/Enemy/ghostbob0045.png').convert_alpha(), (40, 50))
enemy_frames = [enemy_01, enemy_02, enemy_03, enemy_04, enemy_05, enemy_06, enemy_07, enemy_08, enemy_09, enemy_10]
enemy_frames_mirror = []
for frame in enemy_frames:
    mirror = pygame.transform.flip(frame, True, False)
    enemy_frames_mirror.append(mirror)

# global variables
width = 1000
height = 800
# bg_surface = pygame.transform.scale(pygame.image.load('assets/tiles02.jpg'), (width, height))
# bg_surface = pygame.transform.scale2x(pygame.image.load('assets/tiles01.png'))

class Player(object):
    def __init__(self, x, y, surface, mirror_surface, frames, mirror_frames):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.vel = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.direction = 0      # 0  = right, 1 = left
        self.index = 0
        self.surface = surface
        self.mirror_surface = mirror_surface
        self.frames = frames
        self.mirror_frames = mirror_frames
        self.attack_speed = 1000    # 1 sec
        self.health = 10
        self.immune_time = 2000   # 2 seconds
        self.last_collision_time = pygame.time.get_ticks()
        self.level = 1
        self.exp = 0
        self.next_level = 10
        
    def exp_gain(self):
        self.exp += 1
        if self.exp >= self.next_level:
            self.level += 1
            self.exp = abs(self.next_level - self.exp)
            self.next_level = int(self.next_level*1.5)
            print(f"level up - {self.level}")
            return True
        print(f"current exp - {self.exp}")
        print(f"needed exp - {self.next_level}")
        return False
        
    def immune(self):
        return self.last_collision_time > pygame.time.get_ticks() - 3000
    
    def collide(self, damage):
        if self.immune(): return
        self.health -= damage
        self.last_collision_time = pygame.time.get_ticks()

    def draw(self, screen):
        if not (self.up or self.down or self.left or self.right):
            if self.direction == 0:
                self.rect = self.surface.get_rect(center = (self.x, self.y))
                screen.blit(self.surface, self.rect)
            else:
                self.rect = self.mirror_surface.get_rect(center = (self.x, self.y))
                screen.blit(self.mirror_surface, self.rect)
        elif self.direction == 1:
            self.rect = self.mirror_frames[self.index].get_rect(center = (self.x, self.y))
            screen.blit(self.mirror_frames[self.index], self.rect)
        else:
            self.rect = self.frames[self.index].get_rect(center = (self.x, self.y))
            screen.blit(self.frames[self.index], self.rect)

    def movement(self, key_pressed):
        if key_pressed[pygame.K_w] and self.y >= 30:
            self.y -= self.vel
            self.up = True
            self.down = False
        elif key_pressed[pygame.K_s] and self.y <= height - self.height + 20 :
            self.y += self.vel
            self.down = True
            self.up = False
        else:
            self.up = False
            self.down = False
        if key_pressed[pygame.K_a] and self.x >= 30:
            self.x -= self.vel
            self.direction = 1
            self.left = True
            self.right = False
        elif key_pressed[pygame.K_d] and self.x <= width - self.width + 10:
            self.x += self.vel
            self.direction = 0
            self.right = True
            self.left = False
        else:
            self.left = False
            self.right = False
        
    def change_attack_speed(self, AUTO_SHOOT, amount):
        self.attack_speed = int(self.attack_speed * amount)
        pygame.time.set_timer(AUTO_SHOOT, self.attack_speed)
                

class Enemy(object):
    def __init__(self, x, y, frames, mirror_frames):
        # super().__init__(x, y, frames, mirror_frames)
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.vel = VEL
        self.speed = 3
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.direction = 0      # 0  = right, 1 = left
        self.index = 0
        self.frames = frames
        self.mirror_frames = mirror_frames
        self.health = 1
        self.rect = self.frames[self.index].get_rect(center = (self.x, self.y))
        self.damage = 1

    def draw(self, screen):
        if self.direction == 1:
            self.rect = self.mirror_frames[self.index].get_rect(center = (self.x, self.y))
            screen.blit(self.mirror_frames[self.index], self.rect)
        else:
            self.rect = self.frames[self.index].get_rect(center = (self.x, self.y))
            screen.blit(self.frames[self.index], self.rect)

    def movement(self, key_pressed):
        if key_pressed[pygame.K_w]:
            self.y += self.vel
        elif key_pressed[pygame.K_s]:
            self.y -= self.vel
        if key_pressed[pygame.K_a]:
            self.x += self.vel
        elif key_pressed[pygame.K_d]:
            self.x -= self.vel
    
    def move_to_player(self, player):
        angle = math.atan2(player.y - self.y, player.x - self.x)
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed
        self.x = self.x + dx
        self.y = self.y + dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.x < player.x:
            self.direction = 0
            # self.x += self.speed
        if self.x > player.x:
            self.direction = 1
            # self.x -= self.speed
        # if self.y < player.y:
        #     self.y += self.speed
        # if self.y > player.y:
        #     self.y -= self.speed
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, enemy_x, enemy_y):
        pygame.sprite.Sprite.__init__(self)
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        # self.rect = self.image.get_rect(center = (self.x, self.y))
        self.speed = 14
        self.angle = math.atan2(enemy_y - self.y, enemy_x - self.x)
        self.degree = (180 / math.pi) * -self.angle
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.enemy_x = enemy_x      # rename target
        self.enemy_y = enemy_y      # rename target
        self.vel = VEL
        self.width = 20
        self.height = 5
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('assets/bullet4.png').convert_alpha(), (
                self.width,self.height)), self.degree)
        # self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center = (self.x, self.y))
        # self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        # bullet = pygame.Rect(int(self.x), int(self.y), 10, 10)
        # pygame.draw.rect(screen, (250,0,0), self.rect)
        # pygame.transform.rotate(self.image, self.degree)
        # pygame.draw.ellipse(self.surface, (250,0,0), self.rect)
        screen.blit(self.image, self.rect)
        
    def movement(self, key_pressed):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if key_pressed[pygame.K_w]:
            self.y += self.vel
            self.enemy_y += self.vel
        elif key_pressed[pygame.K_s]:
            self.y -= self.vel
            self.enemy_y -= self.vel
        if key_pressed[pygame.K_a]:
            self.x += self.vel
            self.enemy_x += self.vel
        elif key_pressed[pygame.K_d]:
            self.x -= self.vel
            self.enemy_x -= self.vel

class PickUp(object):
    """ pickup_type 1 = exp """
    def __init__(self, x, y, radius, pickup_type=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.pickup_type = pickup_type
        self.surface = pygame.Surface((self.radius, self.radius))
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        # self.rect = pygame.draw.circle(self.surface, (250,0,0), (self.x, self.y), self.radius)
        
    def draw(self, screen):
        # screen.blit(self.surface, self.rect)
        pygame.draw.ellipse(screen, (0,0,250), self.rect)

class Background(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = VEL
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.bg_surface = pygame.image.load('assets/tiles04.png').convert()     # image size of bg_surface needs to be same size as screen size, else have to be scaled
        self.tiles = [[self.bg_surface, self.bg_surface],
                     [self.bg_surface, self.bg_surface]]
        
    def draw(self, screen):
        """ Moves background to fit the movement. Once bg_surface goes out-of-bounds, 
        positions of each surface will be set back to starting position +/(-) velocity """
        if self.x > self.width:
            self.x = self.width / 2 + self.vel  
        if self.x < 0:
            self.x = self.width / 2 - self.vel
        if self.y > self.height:
            self.y = 0 + self.vel
        if self.y  < 0:
            self.y = self.height - self.vel

        screen.blit(self.tiles[0][0], (self.x - self.width, self.y - self.height))
        screen.blit(self.tiles[0][1], (self.x, self.y - self.height))
        screen.blit(self.tiles[1][0], (self.x - self.width, self.y))
        screen.blit(self.tiles[1][1], (self.x, self.y))

    def movement(self, key_pressed):
        if key_pressed[pygame.K_w]:
            self.y += self.vel
        elif key_pressed[pygame.K_s]:
            self.y -= self.vel
        if key_pressed[pygame.K_a]:
            self.x += self.vel
        elif key_pressed[pygame.K_d]:
            self.x -= self.vel

class Game(object):
    def __init__(self, arg):
        self.arg = arg
        self.clock = pygame.time.Clock()
        self.x = width / 2
        self.y = height / 2

    def draw_screen(self, player, bg, enemies, bullets, pickup):
        bg.draw(screen)
        player.draw(screen)
        # enemy.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        pickup.draw(screen)
        pygame.display.update()

    def main(self, screen):
        player = Player(width / 2, height / 2, player_surface, player_surface_mirror,
                        player_walk_frames, player_walk_frames_mirror)
        bg = Background(width / 2, height / 2)
        # enemy = Enemy(50 , height / 2, enemy_frames, enemy_frames_mirror)
        enemies = []     # create enemy list and make it work
        # for i in range(5):
        #     enemies.append(Enemy(random.randint(0, width) , random.randint(0, height), enemy_frames, enemy_frames_mirror))
        bullets = []
        pickup = PickUp(100, 100, 50, pickup_type=1)
        

        PLAYER_WALK_ANIMATION = pygame.USEREVENT
        pygame.time.set_timer(PLAYER_WALK_ANIMATION, 50)

        ENEMY_ANIMATION = pygame.USEREVENT + 1
        pygame.time.set_timer(ENEMY_ANIMATION, 150)
        
        AUTO_SHOOT = pygame.USEREVENT + 2
        pygame.time.set_timer(AUTO_SHOOT, player.attack_speed)
        
        enemy_spawn_speed = 1000
        SPAWN_ENEMY = pygame.USEREVENT + 3
        pygame.time.set_timer(SPAWN_ENEMY, 1000)

        """ Main Game Loop """
        while True:
            self.clock.tick(60)
            self.draw_screen(player, bg, enemies, bullets, pickup)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        player.change_attack_speed(AUTO_SHOOT, 0.8)
                    if event.key == pygame.K_2:
                        player.change_attack_speed(AUTO_SHOOT, 1.2)
                    if event.key == pygame.K_3:
                        enemy_spawn_speed = int(enemy_spawn_speed * 0.8)
                        pygame.time.set_timer(SPAWN_ENEMY, enemy_spawn_speed)
                    if event.key == pygame.K_4:
                        enemy_spawn_speed = int(enemy_spawn_speed * 1.2)
                        pygame.time.set_timer(SPAWN_ENEMY, enemy_spawn_speed)
                    
                if event.type == PLAYER_WALK_ANIMATION:
                    if player.index < 11:
                        player.index += 1
                    else:
                        player.index = 0
                        
                if event.type == ENEMY_ANIMATION:
                    for enemy in enemies:
                        if enemy.index < 9:
                            enemy.index += 1
                        else:
                            enemy.index = 0
                            
                if event.type == AUTO_SHOOT:
                    if enemies:
                        temp = enemies[0]
                        for enemy in enemies:
                            enemy_dist = math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2)
                            temp_dist = math.sqrt((temp.x - player.x)**2 + (temp.y - player.y)**2)
                            if temp_dist > enemy_dist:
                                temp = enemy
                        bullets.append(Bullet(temp.x, temp.y))
                    for bullet in bullets:
                        if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                            bullets.remove(bullet)
                            
                if event.type == SPAWN_ENEMY:
                    spawn_x = random.randint(-50, SCREEN_WIDTH + 50)
                    spawn_y = random.randint(-50, SCREEN_HEIGHT + 50)
                    spawn_points = [(0,0),(SCREEN_WIDTH,SCREEN_HEIGHT),(0, SCREEN_HEIGHT),(SCREEN_WIDTH, 0),
                                    (0, SCREEN_HEIGHT / 2),(SCREEN_WIDTH / 2, 0),(SCREEN_WIDTH / 2, SCREEN_HEIGHT),(SCREEN_WIDTH, SCREEN_HEIGHT / 2),
                                    (0, SCREEN_HEIGHT / 4),(SCREEN_WIDTH / 4, 0),(SCREEN_WIDTH / 4, SCREEN_HEIGHT),(SCREEN_WIDTH, SCREEN_HEIGHT / 4), 
                                    (0, SCREEN_HEIGHT / 8),(SCREEN_WIDTH / 8, 0),(SCREEN_WIDTH / 8, SCREEN_HEIGHT),(SCREEN_WIDTH, SCREEN_HEIGHT / 8)]
                    spawn = random.choice(spawn_points)
                    enemies.append(Enemy(spawn[0], spawn[1], enemy_frames, enemy_frames_mirror))
                

            key_pressed = pygame.key.get_pressed()     # Movement
            player.movement(key_pressed)
            bg.movement(key_pressed)

            # handle enemies
            for enemy in enemies:
                enemy.movement(key_pressed)
                enemy.move_to_player(player)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                if enemy.rect.colliderect(player):
                    player.collide(enemy.damage)
                    print(player.health)
                    
            # handle bullets
            for bullet in bullets:
                bullet.movement(key_pressed)
                
                for enemy in enemies:
                    if bullet.rect.colliderect(enemy):      # if bullet hit enemy       
                        enemy.health -= 1
                        bullets.remove(bullet)
                        player.exp_gain()
                        break       # makes sure i don't try to remove bullet that has already been removed


if __name__ == "__main__":
    Game(0).main(screen)