#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wangding

pygame : Snake
"""
def Snake():
    # import module
    import pygame, random, time
    
    #def a class Snake
    class Snake:
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
            if self.direction == 'LEFT':
                self.position[0] -= self.speed
            if self.direction == 'DOWN':
                self.position[1] += self.speed
            if self.direction == 'UP':
                self.position[1] -= self.speed
    
        #Update the snake's body
        def body_update(self):
            self.body.insert(0, list(self.position))
            #self.body.pop()
    
        #Draw the snake as rectangles
        def body_draw(self, color):
            for ps in self.body:
                pygame.draw.rect(screen, color, pygame.Rect(ps[0], ps[1], self.speed * 2, self.speed * 2))
    
        #Set the bounds
        def bounds_set(self):
            if self.position[0] < 0 or self.position[0] >= width:
                gameover()
            if self.position[1] < 0 or self.position[1] >= height:
                gameover()
    
        #Hit self
        def self_hit(self):
            for rect in self.body[1:]:
                if self.position == rect:
                    gameover()
    #pygame init
    pygame.init()
    
    #Load the bgm
    pygame.mixer.music.load("/Users/wangding/Desktop/Final_chat/game_data/snake_bgm.wav")
    pygame.mixer.music.play()
    
    #Set variables
    position_food = [50, 300]
    food_1 = True
    food_2 = True
    
    #init different colors
    black = pygame.Color(0, 0, 0)
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
    
    #Init two players
    snake_1 = Snake([400, 200], [[400, 200], [500, 200],[600, 200]], 5, 'LEFT', '', 0)
    snake_2 = Snake([400, 300], [[400, 300], [500, 300],[600, 300]], 5, 'RIGHT', '', 0)
    
    #Define the function for scores and gameover
    
    def showscore(choice=1):
        Surface_font = pygame.font.SysFont('arial', 50)
        Surface_score = Surface_font.render("P1 Score  :  {0}".format(snake_1.score), True, white)
        Srect = Surface_score.get_rect()
        if choice == 1:
            Srect.midtop = (150, 10)
        else:
            Srect.midtop = (320, 100)
        screen.blit(Surface_score, Srect)
    
        Surface_font = pygame.font.SysFont('arial', 50)
        Surface_score = Surface_font.render("P2 Score  :  {0}".format(snake_2.score), True, white)
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
        exit()
        
    
    while True:
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
            #Change the direction of the snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake_1.p_update = 'RIGHT'
                elif event.key == pygame.K_LEFT:
                    snake_1.p_update = 'LEFT'
                elif event.key == pygame.K_UP:
                    snake_1.p_update = 'UP'
                elif event.key == pygame.K_DOWN:
                    snake_1.p_update = 'DOWN'
    
                if event.key == pygame.K_d:
                    snake_2.p_update = 'RIGHT'
                elif event.key == pygame.K_a:
                    snake_2.p_update = 'LEFT'
                elif event.key == pygame.K_w:
                    snake_2.p_update = 'UP'
                elif event.key == pygame.K_s:
                    snake_2.p_update = 'DOWN'
    
    
        #make sure it will not change direction in a line
        snake_1.direction_check()
        snake_2.direction_check()
        #Update the direction of the movement
        snake_1.direction_update()
        snake_2.direction_update()
        #Update the snake's body
        snake_1.body_update()
        snake_2.body_update()
        if snake_1.position == position_food:
            position_food = [random.randrange(1, width // 10) * snake_1.speed, random.randrange(1, height // 10) * snake_1.speed]
            snake_1.score += 1
        else:
            snake_1.body.pop()
    
        #Snake eat food
        if snake_2.position == position_food:
            position_food = [random.randrange(1, width // 10) * snake_1.speed, random.randrange(1, height // 10) * snake_1.speed]
            snake_2.score += 1
        else:
            snake_2.body.pop()
    
    
    
    
        screen.blit(bg, (0, -3))
        pygame.display.update()
        #Draw the snake and food as rectangles
        snake_1.body_draw(red)
        snake_2.body_draw(green)
        pygame.draw.rect(screen, white, pygame.Rect(position_food[0], position_food[1], snake_1.speed * 2, snake_1.speed * 2))
        #Set the bounds
        snake_1.bounds_set()
        snake_2.bounds_set()
        #Hit self
        snake_1.self_hit()
        snake_2.self_hit()
    
        #Hit other player
        for i in snake_1.body:
            if i == snake_2.position:
                gameover()
    
        for i in snake_2.body:
            if i == snake_1.position:
                gameover()
    
    
    
        showscore()
    
    
        #Set the frequency and speed of the game
        pygame.display.flip()
        fpsController.tick(20)
