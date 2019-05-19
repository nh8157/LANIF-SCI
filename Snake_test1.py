#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 22:26:51 2019

@author: wangding
"""

import pygame
from network import Network


class Player():
    width = height = 50

    def __init__(self, startx, starty, body, speed, direction, p_update, score):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = (255,0,0)
        self.body = body
        self.speed = speed
        self.direction = direction
        self.p_update = p_update
        self.score = score
        self.canvas = Canvas(self.width, self.height, "Testing...")
        
    def body_draw(self, color):
        for ps in self.body:
            pygame.draw.rect(self.canvas.screen, self.color, pygame.Rect(self.x, self.y, self.speed * 2, self.speed * 2))
    #Set the bounds
    def bounds_set(self):
        if self.x < 0 or self.x >= width:
            gameover()
        if self.y < 0 or self.y >= height:
            gameover()

    #Hit self
    def self_hit(self):
        for rect in self.body[1:]:
            if [self.x, self.y] == rect:
                gameover()

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(400, 200, [[400, 200], [500, 200],[600, 200]], 5, 'LEFT', '', 0)
        self.player2 = Player(400, 300, [[400, 300], [500, 300],[600, 300]], 5, 'RIGHT', '', 0)
        self.canvas = Canvas(self.width, self.height, "Testing...")

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            #self.canvas.draw_background()
            self.player.body_draw((255, 0, 0))
            self.player2.body_draw((255, 0, 0))
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))

g = Game(720, 450)
g.run()
        

