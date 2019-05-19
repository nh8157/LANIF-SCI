#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wangding

pygame : Snake
"""
# import module
def Game():
    import pygame, sys, random, time
    
    #pygame init
    pygame.init()
    
    #Set variables
    position_food = [50, 300]
    position_snake = [400, 200]
    body = [[400, 200], [500, 200],[600, 200]]
    speed = 5
    direction = 'LEFT'
    p_update = ''
    score = 0
    food = True
    over = True
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
    
    
    
    #Define the function for scores and gameover
    
    def showscore(choice=1):
        Surface_font = pygame.font.SysFont('arial', 50)
        Surface_score = Surface_font.render("Score  :  {0}".format(score), True, white)
        Srect = Surface_score.get_rect()
        if choice == 1:
            Srect.midtop = (100, 10)
        else:
            Srect.midtop = (320, 100)
        screen.blit(Surface_score, Srect)
        
    def gameover():
        print("Over!!!");
        final_font = pygame.font.SysFont('arial', 70)
        GOsurf = final_font.render("Game Over", True, red)
        GOrect = GOsurf.get_rect()
        GOrect.midtop = (320, 25)
        screen.blit(GOsurf, GOrect)
        showscore(0)
        pygame.display.flip()
        time.sleep(4)
        pygame.quit()
        exit()
    
    
    
    while over:
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                try:
                    pygame.quit()
                    exit()
                except:
                    sys.exit()
            
            #Change the direction of the snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    p_update = 'RIGHT'
                elif event.key == pygame.K_LEFT:
                    p_update = 'LEFT'
                elif event.key == pygame.K_UP:
                    p_update = 'UP'
                elif event.key == pygame.K_DOWN:
                    p_update = 'DOWN'
        
        #make sure it will not change direction in a line
        if p_update == 'RIGHT' and direction != 'LEFT':
            direction = p_update
        if p_update == 'LEFT' and direction != 'RIGHT':
            direction = p_update
        if p_update == 'UP' and direction != 'DOWN':
            direction = p_update
        if (p_update == 'DOWN' and direction != 'UP'):
            direction = p_update
            
        #Update the direction of the movement
        if direction == 'RIGHT':
            position_snake[0] += speed
        if direction == 'LEFT':
            position_snake[0] -= speed
        if direction == 'DOWN':
            position_snake[1] += speed
        if direction == 'UP':
            position_snake[1] -= speed
            
        #Update the snake's body
        body.insert(0, list(position_snake))
        #Snake eat food
        if position_snake == position_food:
            food = False
            score += 1
        else:
            body.pop()
            food = True
        #Food update
        if food == False:
            position_food = [random.randrange(1, width // 10) * speed, random.randrange(1, height // 10) * speed]
            food = True
            
        #Set the background
        #screen.fill(white)
        screen.blit(bg, (0, -3))
        pygame.display.update()
        #Draw the snake and food as rectangles
        for ps in body:
            pygame.draw.rect(screen, red, pygame.Rect(ps[0], ps[1], speed * 2, speed * 2))
        pygame.draw.rect(screen, green, pygame.Rect(position_food[0], position_food[1], speed * 2, speed * 2))
    
    
        #Set the bounds
        if position_snake[0] < 0 or position_snake[0] >= width:
            gameover()
            break;
        if position_snake[1] < 0 or position_snake[1] >= height:
            gameover()
            break;
            
        #Hit self
        for rect in body[1:]:
            if position_snake == rect:
                gameover()
        showscore()
        
        #Set the frequency and speed of the game
        pygame.display.flip()
        fpsController.tick(20)
