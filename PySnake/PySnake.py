import pygame
import sys
import random

LEFT = (-1, 0)
RIGHT = (1, 0)
DOWN = (0, 1)
UP = (0, -1)
STILL = (0, 0)

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
        self.head = self.segments[0]
        self.tail = self.segments[len(self.segments) - 1]

    def dead(self):
        dead = False
        print(self.head.x, self.head.y)
        for s in self.segments[1:]:
            if self.head.x == s.x and self.head.y == s.y:
                return True
        if self.head.x < 0 or self.head.x > cols or self.head.y < 0 or self.head.y > rows:
            return True
        return False

    def eat(self, pill):
        x, y, w, h = pill
        x, y = pixelsToCoords(x, y)
        if x == self.head.x and y == self.head.y:
            print("GNAM")
            newX = self.tail.prevX
            newY = self.tail.prevY
            s = Segment(newX, newY, self.tail.index + 1)
            self.segments.append(s)
            self.size += 1
            self.tail = s
            return True
        else:
            return False

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

def pixelsToCoords(x, y):
    r = x / segment_size
    c = y / segment_size
    return r, c

def getPill():
    pill = None
    while not pill:
        x = random.randint(0, cols - 1)
        y = random.randint(0, rows - 1)
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

snake = Snake(5, screen)
direction = UP

pill = getPill()

while not done:
    clock.tick(30)
    #direction = (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if direction != DOWN:
                    direction = UP
            if event.key == pygame.K_DOWN:
                if direction != UP:
                    direction = DOWN
            if event.key == pygame.K_LEFT:
                if direction != RIGHT:
                    direction = LEFT
            if event.key == pygame.K_RIGHT:
                if direction != LEFT:
                    direction = RIGHT

    screen.fill(pygame.color.THECOLORS['black'])
    
    if direction != STILL:
        snake.move(direction)
    
    if snake.dead():
        done = True

    #snake.debug()
    pygame.draw.rect(screen, pygame.color.THECOLORS['pink'], pill)
    snake.draw()

    if snake.eat(pill):
        pill = getPill()

    pygame.display.flip()