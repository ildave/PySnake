import pygame
import sys
import random

class Game():
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    UP = (0, -1)
    STILL = (0, 0)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        self.done = False
        
        self.segment_size = 20
        self.rows = self.height / self.segment_size
        self.cols = self.width / self.segment_size

        self.snake = Snake(5, self)
        self.direction = self.UP

        self.score = 0
        self.speed = 5

        self.getPill()

    def getPill(self):
        pill = None
        while not pill:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            for s in self.snake.segments:
                if s.x == x and s.y == y:
                    break
            c, r = self.cooordsToPixel(x, y)
            pill = c, r, self.segment_size, self.segment_size
        self.pill = pill

    def cooordsToPixel(self, r, c):
        x = r * self.segment_size
        y = c * self.segment_size
        return x, y

    def pixelsToCoords(self, x, y):
        r = x / self.segment_size
        c = y / self.segment_size
        return r, c

    def resetScreen(self):
        self.screen.fill(pygame.color.THECOLORS['black'])

    def drawPill(self):
        pygame.draw.rect(self.screen, pygame.color.THECOLORS['pink'], self.pill)

    def drawScore(self):
        textsurface = self.font.render('Score: ' + str(self.score), False, pygame.color.THECOLORS['white'])
        self.screen.blit(textsurface, (10, 10))

    def draw(self):
        self.resetScreen()
        self.drawPill()
        self.snake.draw()
        self.drawScore()

        pygame.display.flip()

    def manageInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.direction != self.DOWN:
                        self.direction = self.UP
                if event.key == pygame.K_DOWN:
                    if self.direction != self.UP:
                        self.direction = self.DOWN
                if event.key == pygame.K_LEFT:
                    if self.direction != self.RIGHT:
                        self.direction = self.LEFT
                if event.key == pygame.K_RIGHT:
                    if self.direction != self.LEFT:
                        self.direction = self.RIGHT

    def update(self):
        if self.direction != self.STILL:
            self.snake.move(self.direction)
    
        if self.snake.isDead:
            self.done = True

        if self.snake.eat(self.pill):
         self.getPill()
         self.updatePoints()

    def updatePoints(self):
        self.score += self.snake.size - self.snake.startingSize


class Segment():
    def __init__(self, x, y, i, game):
        self.game = game
        self.index = i
        self.x = x
        self.y = y
        self.prevX = self.x
        self.prevY = self.y

    def getRect(self):
        x, y = self.game.cooordsToPixel(self.x, self.y)
        return x, y, self.game.segment_size, self.game.segment_size

class Snake():
    def __init__(self, size, game):
        self.game = game
        self.screen = self.game.screen
        self.segments = []
        self.size = size
        self.startingSize = self.size
        for i in range(0, size):
            segment = Segment(10, 10 + i, i, self.game)
            self.segments.append(segment)
        self.head = self.segments[0]
        self.tail = self.segments[len(self.segments) - 1]
        self.isDead = False

    def willDie(self, x, y):
        for s in self.segments[1:]:
            if x == s.x and y == s.y:
                self.isDead = True
        if x < 0 or x > self.game.cols or y < 0 or y > self.game.rows:
            self.isDead = True

    def eat(self, pill):
        x, y, w, h = pill
        x, y = self.game.pixelsToCoords(x, y)
        if x == self.head.x and y == self.head.y:
            newX = self.tail.prevX
            newY = self.tail.prevY
            s = Segment(newX, newY, self.tail.index + 1, self.game)
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
        hor, vert = direction
        potX = self.head.x + hor
        potY = self.head.y + vert
        self.willDie(potX, potY)

        if not self.isDead:
            self.head.prevX = self.head.x
            self.head.prevY = self.head.y
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


def main():
    game = Game(800, 600)

    while not game.done:
        game.clock.tick(game.speed)
        game.manageInput()
        game.update()
        game.draw()

if __name__ == "__main__":
    main()

    