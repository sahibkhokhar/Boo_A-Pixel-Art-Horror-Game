import sys
import pygame as pg
from images import *
import random as r
import json

pygame.init()
clock = pg.time.Clock()
vec = pg.math.Vector2

screen = pg.display.set_mode((1280, 720))
tile_rects = []
file = open("levels.json", "r")
content = file.read()
map_gen = json.loads(content)
print(r.choice(map_gen['spawn_loc']))

def render_tiles():
    global tile_rects
    tile_rects = []
    y= 0
    for row in map_gen['level']:
        x = 0
        for tile in row:
            '''
            0: Floor
            1: Top Wall
            2: Left Wall
            3: Right Wall
            4: Bot Wall
            5: Top Left Corner
            6: Top Right Corner
            7: Bot Left Corner
            8: Bot Right Corner
            9: Top Right Sharp Corner
            10: Top Left Sharp Corner
            11: Bot Wall Left Curved
            12: Bot Wall Right Curved
            '''
            if tile == 0:   # floor
                screen.blit(floor_tile, (x*64, y*64))
            elif tile == 1:   # top wall
                screen.blit(top_wall, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 2:   # left wall
                screen.blit(left_wall, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 3:   # right wall
                screen.blit(right_wall, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 4:   # bot wall
                screen.blit(bottom_wall, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 5:   # top left corner
                screen.blit(top_left_corner, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 6:   # top right corner
                screen.blit(top_right_corner, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 7:   # bot left corner
                screen.blit(bot_left_corner, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 8:   # bot right corner
                screen.blit(bot_right_corner, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 9:   # bot right corner
                screen.blit(top_right_scorner, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 10:   # bot right corner
                screen.blit(top_left_scorner, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 11:   # bot right corner
                screen.blit(bot_rcurve, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            elif tile == 12:   # bot right corner
                screen.blit(bot_lcurve, (x*64, y*64))
                tile_rects.append(pygame.Rect(x*64, y*64, 64, 64))
            x+=1
        y+= 1

class player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # player movement
        self.image = player_img.convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = map_gen['player_loc']
        self.speed = [0, 0]
        self.rebound_rect = None
        self.hp = 3
        self.attack = False

        # Fog Of War
        self.dark = True
        self.fog = pg.Surface((1280, 720))
        self.fog.fill(pg.Color('#33142b'))
        self.light_mask = shadows
        self.light_mask = pg.transform.scale(self.light_mask, (200, 200))
        self.light_rect = self.light_mask.get_rect()

    def render_fog(self):
        self.fog.fill(pg.Color('#000000'))
        self.light_rect.center = self.rect.center
        self.fog.blit(self.light_mask, self.light_rect)
        screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_RGB_MULT)

    def collision_test(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def colliders(self):
        hit_list = self.collision_test(tile_rects)
        for i in hit_list:
            if self.speed[0] > 0:
                self.rect.right = self.rebound_rect.right
            if self.speed[0] < 0:
                self.rect.left = self.rebound_rect.left
            if self.speed[1] > 0:
                self.rect.bottom = self.rebound_rect.bottom
            if self.speed[1] < 0:
                self.rect.top = self.rebound_rect.top

    def Attack(self):
        if self.attack:
            if enemy.rect.centerx <= self.rect.centerx+90 or enemy.rect.centerx <= self.rect.centerx-90:
                if enemy.rect.centery <= self.rect.centery + 90 or enemy.rect.centery <= self.rect.centery - 90:
                        print('Hit')

    def update(self):
        self.speed = [0, 0]
        self.rebound_rect = self.rect.copy()
        key_state = pg.key.get_pressed()
        if key_state[pg.K_a]:
            self.speed[0] = -3
        elif key_state[pg.K_d]:
            self.speed[0] = 3
        if key_state[pg.K_w]:
            self.speed[1] = -3
        elif key_state[pg.K_s]:
            self.speed[1] = 3
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if key_state[pg.K_SPACE]:
            self.attack = True
        elif not key_state[pg.K_SPACE]:
            self.attack = False


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.visible = False
        self.image = enemy_img.convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = r.choice(map_gen['spawn_loc'])
        self.speed = [0, 0]
        self.rebound_rect = None
        self.r_speed = r.random()

    def update(self):         # follow player function
        self.speed = [0, 0]
        self.rebound_rect = self.rect.copy()
        if not player.rect.x + 200 <= self.rect.x or not player.rect.x - 200 <= self.rect.x:
            if not player.rect.y + 200 <= self.rect.y or not player.rect.y - 200 <= self.rect.y:
                if not self.rect.colliderect(player.rect):
                    self.visible = True
                    if self.rect.x > player.rect.x:
                        self.speed[0] = 2
                        self.rect.x -= self.speed[0]
                    elif self.rect.x < player.rect.x:
                        self.speed[0] = 2
                        self.rect.x += self.speed[0]
                    if self.rect.y > player.rect.y:
                        self.speed[1] = 2
                        self.rect.y -= self.speed[1]
                    elif self.rect.y < player.rect.y:
                        self.speed[1] = 2
                        self.rect.y += self.speed[1]
                else:
                    pass
                    # player takes damage

all_sprites = pg.sprite.Group()
enemy_sprite = pg.sprite.Group()
for i in range(r.randint(2, map_gen['enemy_amount'])):
    enemy = Enemy()
    enemy_sprite.add(enemy)

player = player()
all_sprites.add(player)
def main():
    while True:
        screen.fill(pg.Color('#33142b'))
        render_tiles()
        player.colliders()
        player.Attack()
        all_sprites.update()
        all_sprites.draw(screen)
        enemy_sprite.draw(screen)
        enemy_sprite.update()
        player.render_fog()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                file.close()
                pg.quit()
                sys.exit()
        pg.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
