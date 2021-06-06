# This is a sample Python script.
import random
import sys
import time
import pygame



from pygame.locals import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
WIDTH = 768
HEIGHT = 608

class Game:
    def __init__(self):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.fill((8, 196, 130))
        self.apple = Apple(self.surface)
        self.snake = Snake(self.surface, 1, self.apple)
        self.snake.draw()
        self.Time = 0
        self.pause = True
        self.speed = 0
        self.diff = True


    def play(self):
        self.snake.walk()
        self.apple.draw()

        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.apple.apple_placement()
            self.snake.increment_length()

            # self collision

        for i in range(3,self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception('Game over')

    #apple collision
    def collision(self,x1,y1,x2,y2):
        if abs(x1-x2) < 8 and abs(y1-y2) < 8:
            return True
        return False

    def show_game_over(self):
        self.surface.fill((0,0,0))
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game over! your score is: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(line1, (WIDTH/2 - 190,HEIGHT/2-150))
        line2 = font.render(f"press enter to play again", True, (255, 255, 255))
        self.surface.blit(line2, (WIDTH / 2 - 190, HEIGHT / 2 -100))
        line3 = font.render(f"press space to change settings", True, (255, 255, 255))
        self.surface.blit(line3, (WIDTH / 2 - 190, HEIGHT / 2 -50 ))
        pygame.display.update()

    def choose_difficulty(self):
        self.surface.fill((0,0,0))
        font = pygame.font.SysFont('arial', 30)
        difficulty = font.render(f'choose difficulty', True, (255, 255, 255))
        self.surface.blit(difficulty, (WIDTH/2 - 140,HEIGHT/2-150))
        pygame.display.update()
        self.menu()

        ###
    def menu(self):
        """ This is the menu that waits you to click the s key to start """
        b1 = self.button((150, 220), "easy")
        b2 = self.button((285, 220), "normal")
        b3 = self.button((470, 220), "hard")
        b4 = self.button((150, 320), "boundaries?",(160,0,0))
        while True:
            if self.pause:
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if b1.collidepoint(pygame.mouse.get_pos()):
                            self.pause=False
                            self.speed = 0.25
                            break
                        elif b2.collidepoint(pygame.mouse.get_pos()):
                            self.pause=False
                            self.speed = 0.15
                            break
                        elif b3.collidepoint(pygame.mouse.get_pos()):
                            self.pause=False
                            self.speed = 0.07
                            break
                        elif b4.collidepoint(pygame.mouse.get_pos()):
                            if self.snake.boundaries == True:
                                self.snake.boundaries = False
                                b4 = self.button((150, 320), "boundaries?",(0,233,0))
                                self.width = WIDTH
                                self.height = HEIGHT
                                self.surface = pygame.display.set_mode((self.width, self.height))
                                self.menu()
                            else:
                                b4 = self.button((150, 320), "boundaries?",(160,0,0))
                                self.width = WIDTH + 64
                                self.height = HEIGHT + 64
                                self.surface = pygame.display.set_mode((self.width, self.height))
                                self.snake.boundaries = True
                                self.menu()
                pygame.display.update()
            else:
                break

    def button(self,position, text,color=(228,213,232)):
        font = pygame.font.SysFont("Arial", 50)
        text_render = font.render(text, 1, color)
        x, y, w, h = text_render.get_rect()
        x, y = position
        pygame.draw.line(self.surface, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(self.surface, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
        pygame.draw.line(self.surface, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
        pygame.draw.rect(self.surface, (100, 100, 100), (x, y, w, h))
        return self.surface.blit(text_render, (x, y))

    def reset(self):
        boud = self.snake.boundaries
        speed = self.speed
        self.apple = Apple(self.surface)
        self.snake = Snake(self.surface, 1,self.apple)
        self.snake.boundaries = boud
        self.speed = speed



    def run(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.pause = False
                        if event.key == pygame.K_SPACE:
                            self.diff = True
                        if event.key == pygame.K_DOWN and self.snake.direction !='up':
                            self.snake.move_down()
                            break
                        elif event.key == pygame.K_UP and self.snake.direction !='down':
                            self.snake.move_up()
                            break
                        elif event.key == pygame.K_LEFT and self.snake.direction !='right':
                            self.snake.move_left()
                            break
                        elif event.key == pygame.K_RIGHT and self.snake.direction !='left':
                            self.snake.move_right()
                            break

            try:
                if not self.pause:
                    self.play()

            except:
                self.show_game_over()
                self.pause = True
                self.reset()
                self.diff = False

            if self.pause and self.diff:
                self.choose_difficulty()
            #change apple position
            # self.Time += 1
            # if self.Time%75 == 0:
            #     self.apple.apple_placement()

            time.sleep(self.speed)

SIZE = 32
class Snake:
    def __init__(self, parent_screen, length,apple):
        self.parent_screen = parent_screen
        self.snakeIMG = [SIZE]*length
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.snakeX_change = 0
        self.snakeY_change = 0
        self.direction = ' '
        self.length = length
        self.boundaries = False
        self.apple = apple


    def draw(self):
        self.parent_screen.fill((8, 196, 130))
        if self.direction == 'left':
            self.snakeIMG[0] = pygame.image.load('brickhead_left.png')
        elif self.direction == 'right':
            self.snakeIMG[0] = pygame.image.load('brickhead_right - Copy (2).png')
        elif self.direction == 'up':
            self.snakeIMG[0] = pygame.image.load('brickhead_up.png')
        else:
            self.snakeIMG[0] = pygame.image.load('brickhead_down.png')

        if not self.boundaries:
            if self.x[0] < 0:
                self.x[0] = WIDTH
            elif self.x[0] > WIDTH:
                self.x[0] = 0
            if self.y[0] < 0:
                self.y[0] = HEIGHT
            elif self.y[0] > HEIGHT:
                self.y[0] = 0
        else:
            pygame.draw.line(self.parent_screen, (255, 0, 0), (0, 0), (WIDTH+64, 0), 55)
            pygame.draw.line(self.parent_screen, (255, 0, 0), (0, 0), (0, HEIGHT+64), 55)
            pygame.draw.line(self.parent_screen, (255, 0, 0), (WIDTH + 64, 0), (WIDTH + 64, HEIGHT+64), 55)
            pygame.draw.line(self.parent_screen, (255, 0, 0), (0, HEIGHT+32), (WIDTH+32, HEIGHT+32), 55)
            pygame.display.update()
            if self.x[0] < 32:
                raise Exception('Game over')
            elif self.x[0] >= WIDTH + 32:
                raise Exception('Game over')
            if self.y[0] < 32:
                raise Exception('Game over')
            elif self.y[0] >= HEIGHT:
                raise Exception('Game over')

        self.parent_screen.blit(self.snakeIMG[0], (self.x[0], self.y[0]))
        for i in range(self.length - 1,0,-1):
            self.snakeIMG[i] = pygame.image.load('brick.png')
            self.parent_screen.blit(self.snakeIMG[i], (self.x[i], self.y[i]))

        self.show_score()
        self.apple.draw()
        pygame.display.update()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        elif self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        self.draw()

    def increment_length(self):
        self.length += 1
        self.x.append(0)
        self.y.append(0)
        self.snakeIMG.append(0)

    def show_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"score: {self.length - 1}", True, (0, 0, 0))
        self.parent_screen.blit(score, (10, 10))

class Apple:
    def __init__(self,parent_screen):
        self.num_of_apples = 0
        self.image = pygame.image.load('apple.png')
        self.parent_screen = parent_screen
        self.x = 0
        self.y = 0
        self.apple_placement()

    def apple_placement(self):
        self.x = random.randint(1,((WIDTH-32)/32))*32
        self.y = random.randint(1, ((HEIGHT-32)/32))*32
        #self.image = pygame.image.load('apple.png')

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

game = Game()
game.run()


# width = 800
# height = 600
# screen = pygame.display.set_mode((width, height))
#
# background = pygame.image.load('background.png')
#
#
# #snake body
# snake_body_X_change = []
# snake_bod_y_change = []
# snake_body_X = []
# snake_body_img = []
# snake_body_Y = []
# snake_body_img.append(pygame.image.load('snakehead.png'))
# snake_body_X.append(0)
# snake_body_Y.append(0)
#
#
#
# #snakehead
# snakeimg = pygame.image.load('snakehead.png')
# snakeX = 20
# snakeY = 20
# snakeX_change = 0
# snakeY_change = 0
#
# def snake(x, y):
#     screen.blit(snakeimg, (x, y))
#
# #fruits
# fruitX = []
# fruitimg = []
# fruitY = []
# fruitimg.append(pygame.image.load('fruits.png'))
# fruitX.append(random.randint(0, width - 32))
# fruitY.append(random.randint(0, height - 32))
#
# def add_snake_piece(x,y):
#     snakeimg.append(pygame.image.load('snakehead.png'))
#     snakeX.append(x)
#     snakeY.append(y)
#
# def snake(x, y):
#     screen.blit(snakeimg, (x, y))
#
# def snake_body(i,x, y):
#     screen.blit(snake_body_img[i], (x, y))
#
# def add_fruit():
#     fruitimg.append(pygame.image.load('fruits.png'))
#     fruitX.append(random.randint(0, width - 32))
#     fruitY.append(random.randint(0, height - 32))
#     global num_of_fruits
#     num_of_fruits +=1
#
# def fruit(i,x,y):
#     screen.blit(fruitimg[i],(x,y))
#
# width = 700
# height = 600
#
# screen = pygame.display.set_mode((width,height))
# clock = pygame.time.Clock()
#
# snake_length = 1
# num_of_fruits = 1
# going_left = False
# going_right = False
# going_up = False
# going_down = False
# summon_fruit = 0
# while True:
#     screen.blit(background, (0, 0))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#         if event.type == pygame.KEYDOWN and not going_down and not going_up:
#             if event.key == pygame.K_DOWN:
#                 snakeY_change = 3
#                 going_left = False
#                 going_right = False
#                 going_down = True
#
#         if event.type == pygame.KEYDOWN and not going_up and not going_down:
#             if event.key == pygame.K_UP:
#                 snakeY_change  = -3
#                 going_left = False
#                 going_right = False
#                 going_up= True
#
#         if event.type == pygame.KEYDOWN and not going_right and not going_left:
#             if event.key == pygame.K_LEFT:
#                 snakeX_change = -3
#                 going_left = True
#                 going_up = False
#                 going_down = False
#         if event.type == pygame.KEYDOWN and not going_right and not going_left:
#             if event.key == pygame.K_RIGHT:
#                 snakeX_change = 3
#                 going_right = True
#                 going_up = False
#                 going_down = False
#
#     for i in range(snake_length):
#         snake_body_X[i] = snakeX +32
#         snake_body_Y[i] = snakeY+32
#         snake_body(i,snake_body_X[i],snake_body_Y[i])
#
#
#     if going_left or going_right:
#         snakeX = snakeX + snakeX_change
#     elif going_up or going_down:
#         snakeY = snakeY + snakeY_change
#
#
#     for i in range(num_of_fruits):
#         if abs(snakeX-fruitX[i]) <16 and abs(snakeY-fruitY[i]) < 16:
#             fruitY[i] = height + 50
#         fruit(i,fruitX[i],fruitY[i])
#     snake(snakeX, snakeY)
#     for i in range(snake_length):
#         snake_body(i,snake_body_X[i],snake_body_Y[i])
#
#
#
#     pygame.display.update()
#     summon_fruit += 1
#     if summon_fruit%200 == 0:
#         add_fruit()
#     clock.tick(60)





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
