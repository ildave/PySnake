import pygame
import sys
import random

LEFT = (-1, 0)
RIGHT = (1, 0)
DOWN = (0, 1)
UP = (0, -1)

class Segment():
    def __init__(self, x, y, i):
        self.index = i
        self.x = x
        self.y = y
        self.prevX = self.x
        self.prevY = self.y

    def getRect(self):
        x, y = cooordsToPixel(self.x, self.y)
        return x, y, segment_size, segment_size

class Snake():
    def __init__(self, size, screen):
        self.screen = screen
        self.segments = []
        self.size = size
        for i in range(0, size):
            segment = Segment(10, 10 + i, i)
            self.segments.append(segment)
            print (10 + i)
        self.head = self.segments[0]


    def draw(self):
        for s in self.segments:
            if s.index == 0:
                pygame.draw.rect(self.screen, pygame.color.THECOLORS['blue'], s.getRect())
            else:
                pygame.draw.rect(self.screen, pygame.color.THECOLORS['red'], s.getRect())


    def move(self, direction):
        self.head.prevX = self.head.x
        self.head.prevY = self.head.y
        hor, vert = direction
        self.head.x += hor
        self.head.y += vert
        for i in range(1, len(self.segments)):
            s = self.segments[i]
            predecessor = self.segments[i - 1]
            s.prevX = s.x
            s.prevY = s.y
            s.x = predecessor.prevX
            s.y = predecessor.prevY

    def debug(self):
        for i in range(0, len(self.segments)):
            print(i, self.segments[i].x, self.segments[i].y)


def cooordsToPixel(r, c):
    x = r * segment_size
    y = c * segment_size
    return x, y

def getPill():
    pill = None
    while not pill:
        x = random.randint(0, rows)
        y = random.randint(0, cols)
        for s in snake.segments:
            if s.x == x and s.y == y:
                break
        c, r = cooordsToPixel(x, y)
        pill = c, r, segment_size, segment_size
    return pill


size = width, height = 800, 600
segment_size = 20
rows = height / segment_size
cols = width / segment_size

screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

snake = Snake(4, screen)
direction = UP

pill = getPill()

while not done:
    clock.tick(10)
    #direction = (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = UP
            if event.key == pygame.K_DOWN:
                direction = DOWN
            if event.key == pygame.K_LEFT:
                direction = LEFT
            if event.key == pygame.K_RIGHT:
                direction = RIGHT
    print(direction)

    screen.fill(pygame.color.THECOLORS['black'])
    if direction != (0, 0):
        snake.move(direction)
    snake.debug()
    pygame.draw.rect(screen, pygame.color.THECOLORS['pink'], pill)
    snake.draw()

    pygame.display.flip()