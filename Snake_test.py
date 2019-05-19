#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 21:51:03 2019

@author: wangding
"""

import pygame
import random
import time
from network import Network


size = width, height = 720, 450
screen = pygame.display.set_mode(size)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

class Snake():
    def __init__(self, position, body, speed, direction, p_update, score):
            self.position = position
            self.body = body
            self.speed = speed
            self.direction = direction
            self.p_update = p_update
            self.score = score
    
    
    
    #make sure it will not change direction in a line
    def direction_check(self):
        if self.p_update == 'RIGHT' and self.direction != 'LEFT':
            self.direction = self.p_update
        if self.p_update == 'LEFT' and self.direction != 'RIGHT':
            self.direction = self.p_update
        if self.p_update == 'UP' and self.direction != 'DOWN':
            self.direction = self.p_update
        if self.p_update == 'DOWN' and self.direction != 'UP':
            self.direction = self.p_update

    #Update the direction of the movement
    def direction_update(self):
        if self.direction == 'RIGHT':
            self.position[0] += self.speed
        elif self.direction == 'LEFT':
            self.position[0] -= self.speed
        elif self.direction == 'DOWN':
            self.position[1] += self.speed
        elif self.direction == 'UP':
            self.position[1] -= self.speed
        else:
            pass

    #Update the snake's body
    def body_update(self):
        self.body.insert(0, list(self.position))
        self.body.pop()

    #Draw the snake as rectangles
    def body_draw(self, color):
        for ps in self.body:
            pygame.draw.rect(screen, color, pygame.Rect(ps[0], ps[1], self.speed * 2, self.speed * 2))

    #Set the bounds
    '''def bounds_set(self):
        if self.position[0] < 0 or self.position[0] >= width:
            gameover()
        if self.position[1] < 0 or self.position[1] >= height:
            gameover()'''

    #Hit self
    '''def self_hit(self):
        for rect in self.body[1:]:
            if self.position == rect:
                gameover()'''
class Game():
    def __init__(self):
        self.net = Network()
        self.snake_1 = Snake([400, 200], [[400, 200], [500, 200],[600, 200]], 5, 'LEFT', '', 0)
        self.snake_2 = Snake([400, 300], [[400, 300], [500, 300],[600, 300]], 5, '', '', 0)
        
    def get_snake1(self):
        return self.snake_1
    
    def ger_snake2(self):
        return self.snake_2
    def run(self):
        #init variable
        position_food = [50, 300]
        #pygame init
        pygame.init()
        
        #Load the bgm
        pygame.mixer.music.load("/Users/wangding/Desktop/Final_chat/game_data/snake_bgm.wav")
        pygame.mixer.music.play()
        
        #init different colors
        white = pygame.Color(255, 255, 255)
        red = pygame.Color(255, 0, 0)
        green = pygame.Color(0, 255, 0)
        
        # FPS controller and init clock
        fpsController = pygame.time.Clock()
        
        
        #Set the window
        size = width, height = 720, 450
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("王丁的贪吃蛇")
        bg = pygame.image.load("/Users/wangding/Desktop/Final_chat/game_data/snake_background.jpg")
        
        while True:
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
                #Change the direction of the snake
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.snake_1.p_update = 'RIGHT'
                    elif event.key == pygame.K_LEFT:
                        self.snake_1.p_update = 'LEFT'
                    elif event.key == pygame.K_UP:
                        self.snake_1.p_update = 'UP'
                    elif event.key == pygame.K_DOWN:
                        self.snake_1.p_update = 'DOWN'
                        
            self.snake_2.position[0], self.snake_2.position[1] = self.parse_data(self.send_data())
            print(self.snake_1.position, self.snake_2.position)
    
        
        
            #make sure it will not change direction in a line
            self.snake_1.direction_check()
            self.snake_2.direction_check()
            #Update the direction of the movement
            self.snake_1.direction_update()
            self.snake_2.direction_update()
            #Update the snake's body
            self.snake_1.body_update()
            self.snake_2.body_update()
            
            if self.snake_1.position == position_food:
                position_food = [random.randrange(1, width // 10) * self.snake_1.speed, random.randrange(1, height // 10) * self.snake_1.speed]
                self.snake_1.score += 1
            else:
                self.snake_1.body.pop()
        
            #Snake eat food
            if self.snake_2.position == position_food:
                position_food = [random.randrange(1, width // 10) * self.snake_1.speed, random.randrange(1, height // 10) * self.snake_1.speed]
                self.snake_2.score += 1
            else:
                self.snake_2.body.pop()
        
        
        
        
            screen.blit(bg, (0, -3))
            pygame.display.update()
            #Draw the snake and food as rectangles
            self.snake_1.body_draw(red)
            self.snake_2.body_draw(green)
            pygame.draw.rect(screen, white, pygame.Rect(position_food[0], position_food[1], self.snake_1.speed * 2, self.snake_1.speed * 2))
            #Set the bounds
            self.snake_1.bounds_set()
            self.snake_2.bounds_set()
            #Hit self
            self.snake_1.self_hit()
            self.snake_2.self_hit()
        
            #Hit other player
            for i in self.snake_1.body:
                if i == self.snake_2.position:
                    gameover()
        
            for i in self.snake_2.body:
                if i == self.snake_1.position:
                    gameover()
        
        
        
            showscore()
        
        
            #Set the frequency and speed of the game
            pygame.display.flip()
            fpsController.tick(20)
        
        
    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.snake_1.position[0]) + "," + str(self.snake_1.position[1])
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0

        
'''def showscore(choice=1):
    Surface_font = pygame.font.SysFont('arial', 50)
    Surface_score = Surface_font.render("P1 Score  :  {0}".format(1), True, white)
    Srect = Surface_score.get_rect()
    if choice == 1:
        Srect.midtop = (150, 10)
    else:
        Srect.midtop = (320, 100)
    screen.blit(Surface_score, Srect)

    Surface_font = pygame.font.SysFont('arial', 50)
    Surface_score = Surface_font.render("P2 Score  :  {0}".format(1), True, white)
    Srect = Surface_score.get_rect()
    if choice == 1:
        Srect.midtop = (600, 10)
    else:
        Srect.midtop = (320, 150)
    screen.blit(Surface_score, Srect)

def gameover():
    final_font = pygame.font.SysFont('arial', 70)
    GOsurf = final_font.render("Game Over", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 25)
    screen.blit(GOsurf, GOrect)
    showscore(0)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    time.sleep(10)
    exit()'''
        
g = Game()
g.run()
    