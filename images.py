import pygame.transform
from pygame import image

# Import From Images Sub Folder
player_img = pygame.image.load('images\player1.png')
player_img = pygame.transform.scale(player_img, (10*4, 15*4))

enemy_img = pygame.image.load('images\enemy1.png')
enemy_img = pygame.transform.scale(enemy_img, (10*4, 15*4))

shadows = pygame.image.load("images\light_mask.png")
fow = pygame.image.load("images\dark_rect.png")

# Map Tiles Imported From Good Tileset Folder
floor_tile = pygame.image.load('good tileset/cross_florr.png')
floor_tile = pygame.transform.scale(floor_tile, (64, 64))

top_wall = pygame.image.load('good tileset/topwall.png')
top_wall = pygame.transform.scale(top_wall, (64, 64))

bottom_wall = pygame.image.load('good tileset/bot_wall.png')
bottom_wall = pygame.transform.scale(bottom_wall, (64, 64))

left_wall = pygame.image.load('good tileset/left_wall.png')
left_wall = pygame.transform.scale(left_wall, (64, 64))

right_wall = pygame.image.load('good tileset/right_wall.png')
right_wall = pygame.transform.scale(right_wall, (64, 64))

top_left_corner = pygame.image.load('good tileset/smooth_top_left_corner.png')
top_left_corner = pygame.transform.scale(top_left_corner, (64, 64))

top_right_corner = pygame.image.load('good tileset/smooth_top_right_corner.png')
top_right_corner = pygame.transform.scale(top_right_corner, (64, 64))

bot_left_corner = pygame.image.load('good tileset/bleft_corner_tip.png')
bot_left_corner = pygame.transform.scale(bot_left_corner, (64, 64))

bot_right_corner= pygame.image.load('good tileset/bright_corner_tip.png')
bot_right_corner = pygame.transform.scale(bot_right_corner, (64, 64))

top_left_scorner = pygame.image.load('good tileset/top_left_corner.png')
top_left_scorner = pygame.transform.scale(top_left_scorner, (64, 64))

top_right_scorner = pygame.image.load('good tileset/top_right_corner.png')
top_right_scorner = pygame.transform.scale(top_right_scorner, (64, 64))

bot_rcurve = pygame.image.load('good tileset/bot_rcurve.png')
bot_rcurve = pygame.transform.scale(bot_rcurve, (64, 64))

bot_lcurve = pygame.image.load('good tileset/bot_lcurve.png')
bot_lcurve = pygame.transform.scale(bot_lcurve, (64, 64))
