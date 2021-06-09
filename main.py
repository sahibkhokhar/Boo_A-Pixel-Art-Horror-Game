import json
import os
import random as r
import sys

import pygame as pg
import pygame.mixer
from pygame import mixer

from images import *

pygame.mixer.pre_init(44100, -16, 2, 2048 * 4)
pygame.init()
clock = pg.time.Clock()

screen = pg.display.set_mode((1280, 720))
tile_rects = []
file = open("levels.json", "r")
content = file.read()
map_gen = json.loads(content)

mixer.music.load(os.path.join("audio", "sad.ogg"))
mixer.music.set_volume(.3)
spotted_sound = mixer.Sound("audio/ghostbreath.wav")
mixer.music.play(-1)

class MapRender:
    def __init__(self):
        self.tile_rects = []
        self.door_rect = None
        self.current_level = 0

    def render_tiles(self):
        y = 0
        for row in map_gen[self.current_level]['level']:
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
                if tile == 0:  # floor
                    screen.blit(floor_tile, (x * 64, y * 64))
                elif tile == 1:  # top wall
                    screen.blit(top_wall, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 2:  # left wall
                    screen.blit(left_wall, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 3:  # right wall
                    screen.blit(right_wall, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 4:  # bot wall
                    screen.blit(bottom_wall, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 5:  # top left corner
                    screen.blit(top_left_corner, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 6:  # top right corner
                    screen.blit(top_right_corner, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 7:  # bot left corner
                    screen.blit(bot_left_corner, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 8:  # bot right corner
                    screen.blit(bot_right_corner, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 9:  # bot right corner
                    screen.blit(top_right_scorner, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 10:  # bot right corner
                    screen.blit(top_left_scorner, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 11:  # bot right corner
                    screen.blit(bot_rcurve, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 12:  # bot right corner
                    screen.blit(bot_lcurve, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                elif tile == 13:  # bot right corner
                    screen.blit(top_door, (x * 64, y * 64))
                    self.tile_rects.append(pygame.Rect(x * 64, y * 64, 64, 64))
                    self.door_rect = (pygame.Rect(x * 64, y * 64, 64, 70))
                x += 1
            y += 1

class player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # player movement
        self.image = player_img.convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = map_gen[map_render.current_level]['player_loc']
        self.speed = [0, 0]
        self.rebound_rect = None
        self.hp = 1
        self.attack = False
        self.has_key = False

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
        hit_list = self.collision_test(map_render.tile_rects)
        for tile in hit_list:
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
            for enemy in enemies:
                if enemy.rect.centerx <= self.rect.centerx + 90 or enemy.rect.centerx <= self.rect.centerx - 90:
                    if enemy.rect.centery <= self.rect.centery + 90 or enemy.rect.centery <= self.rect.centery - 90:
                        enemy.dead = True

    def die(self):
        if self.hp <= 0:
            del self

    def level_up(self):
        if self.rect.colliderect(map_render.door_rect):
            if self.has_key:
                print('NEXT LEVEL!')
                map_render.current_level += 1
                map_render.tile_rects.clear()
                player.__init__()
                enemy.__init__()
                key.__init__()
            else:
                print('NEED KEY!')

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
        self.image = enemy_img.convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = r.choice(map_gen[map_render.current_level]['spawn_loc'])
        self.speed = [0, 0]
        self.rebound_rect = None
        self.hp = 1
        self.screem = False
        self.dead = False

    def die(self):
        if self.hp <= 0:
            self.kill()

    def update(self):  # follow player function
        self.speed = [0, 0]
        if not player.rect.x + 300 <= self.rect.x or not player.rect.x - 300 <= self.rect.x:
            if not player.rect.y + 300 <= self.rect.y or not player.rect.y - 300 <= self.rect.y:
                if not self.screem:
                    spotted_sound.play()
                    self.screem = True
                if not self.rect.colliderect(player.rect):
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
                    player.kill()


class Key(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = keyy
        self.rect = self.image.get_rect()
        self.rect.center = map_gen[map_render.current_level]["key_loc"]
        self.simage = mini_key

    def update(self):
        if self.rect.colliderect(player.rect):
            player.has_key = True
        if player.has_key:
            self.image = self.simage
            self.rect.x = player.rect.x + 10
            self.rect.y = player.rect.y + 25


enemies = []
all_sprites = pg.sprite.Group()
map_render = MapRender()
player = player()
key = Key()
for i in range(r.randint(2, len(map_gen[map_render.current_level]['spawn_loc']))):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.append(enemy)
all_sprites.add(player)
all_sprites.add(key)


def main():
    while True:
        print(key.rect)
        for enemy in enemies:
            if enemy.dead:
                all_sprites.remove(enemy)

        screen.fill(pg.Color('#33142b'))
        map_render.render_tiles()
        player.colliders()
        player.Attack()
        enemy.die()
        player.die()
        player.level_up()
        all_sprites.update()
        all_sprites.draw(screen)
        # player.render_fog()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                file.close()
                pg.quit()
                sys.exit()
        pg.display.update()
        clock.tick()

if __name__ == '__main__':
    main()