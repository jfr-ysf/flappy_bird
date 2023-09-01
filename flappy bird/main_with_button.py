import pygame as pg
from pygame.locals import *
from tkinter import *
import random
import os
import sys

pg.init()
pg.mixer.init()
width = 576
height = 980
FPS = 120
speed = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN=(9, 119, 17)
BLUE = (0, 0, 255)

sc = pg.display.set_mode((width, height))
clock = pg.time.Clock()
pg.display.set_caption('Flappy bird')
game_font=pg.font.SysFont('Impact', 40)

G = 0.25
b_mov = 0
fl_p = 0

floor_p = 0
bg = pg.image.load("bg1f.jpg").convert_alpha()
bg.set_colorkey(WHITE)
bg = pg.transform.scale2x(bg)
fl = pg.image.load("floor.jpg").convert_alpha()
fl.set_colorkey(WHITE)
fl = pg.transform.scale2x(fl)

bird_downflap = pg.transform.scale2x(pg.image.load('bird-downflap.png').convert_alpha())
bird_midflap = pg.transform.scale2x(pg.image.load('bird-midflap.png').convert_alpha())
bird_upflap = pg.transform.scale2x(pg.image.load('bird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
gh= bird_frames[bird_index]
gh_rect=gh.get_rect(center=(100, 490))
pipen = pg.image.load("pipe3.png").convert_alpha()
pipen.set_colorkey(WHITE)
pipen = pg.transform.scale2x(pipen)
pipe_list = []
pipe_height = [600, 500, 700]
SPAWNPIPE = pg.USEREVENT
game_active = True
pg.time.set_timer(SPAWNPIPE, 1200)
BIRDFLAP = pg.USEREVENT + 1
pg.time.set_timer(BIRDFLAP, 200)
score=0
high_score=0
def draw_buttons():
    btn1=Button(text='Again?', background='DARK_GREEN', 
        foreground='WHITE', highlightcolor='GREEN',  )

def draw_floor():
    sc.blit(fl, (fl_p, 800))
    sc.blit(fl, (fl_p + 576, 800))

def make_pipe():
    random_pipe_pos = random.choice(pipe_height)
    b_pipe = pipen.get_rect(midtop=(700, random_pipe_pos))
    t_pipe = pipen.get_rect(midbottom=(700, random_pipe_pos - 300))
    return b_pipe, t_pipe

def move_pipes(pipes):
    for pip in pipes:
            pip.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pip in pipes:
        if pip.bottom >= 980:
            sc.blit(pipen, pip)
        else:
            flip_pipe = pg.transform.flip(pipen, False, True)
            sc.blit(flip_pipe, pip)

def remove_pipes(pipes):
	for pip in pipes:
		if pip.centerx == -100:
			pipes.remove(pip)
	return pipes

def check_collissions(pipes):
    for pipe in pipes:
        if gh_rect.colliderect(pipe):
            return False
    if gh_rect.top <= -100 or gh_rect.bottom >= 800:
        return False

    return True

def rotate_bird(bird):
    n_bird=pg.transform.rotozoom(bird,-b_mov*3  ,1)
    return n_bird

def bird_animation():
    n_bird=bird_frames[bird_index]
    n_bird_rect=n_bird.get_rect(center=(100, gh_rect.centery))
    return n_bird, n_bird_rect

def score_d(game_state):
    if game_state=='a_game':
        score_s=game_font.render(str(int(score)), True, pg.Color('red'))
        score_rect=score_s.get_rect(center=(288, 200))
        sc.blit(score_s, score_rect)
    if game_state=='game_over':
        score_s = game_font.render(f'The score: {int(score)}', True, pg.Color('red'))
        score_rect = score_s.get_rect(center=(288, 200))
        sc.blit(score_s, score_rect)
        high_score_s = game_font.render(f'The highest score: {int(high_score)}', True, pg.Color('red'))
        high_score_rect = high_score_s.get_rect(center=(288, 300))
        sc.blit(high_score_s, high_score_rect)

def update_score(score, high_score):
    if score>high_score:
        high_score=score
    return high_score

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == SPAWNPIPE:
            pipe_list.extend(make_pipe())
        if event.type == BIRDFLAP:
            if bird_index<2:
                bird_index+=1
        else:
            bird_index=0
        gh, gh_rect=bird_animation()
    sc.blit(bg, (0, 0))
    fl_p -= 1
    draw_floor()
    if fl_p <= -576:
        fl_p = 0

    if game_active:
        pipe_list = move_pipes(pipe_list)
        pipe_list = remove_pipes(pipe_list)
        draw_pipes(pipe_list)
        b_mov += G
        rotated_bird=rotate_bird(gh)
        gh_rect.centery += b_mov
        sc.blit(rotated_bird, gh_rect)
        game_active=check_collissions(pipe_list)
        score+=0.01
        score_d('a_game')
    else:
        high_score=update_score(score, high_score)
        score_d('game_over')

    key = pg.key.get_pressed()
    if key[pg.K_SPACE] and game_active:
        b_mov = 0
        b_mov -= 6
    if game_active == False:
        game_active=True
        pipe_list.clear()
        gh_rect.center=(100, 490)
        b_mov=0
        score = 0
    pg.display.update()
    clock.tick(FPS)