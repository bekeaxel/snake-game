import pygame, sys, random

"""
simple snake game 
"""

GREEN = (119, 217, 89)
BLACK = (0, 0, 0)
RED = (196, 53, 0)
win_dim = (500, 400)
cube_size = 20

class Cube:
    def __init__(self, x, y, color):
        self.pos = (x, y)
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.rect(window, self.color, (self.pos[0], self.pos[1], cube_size, cube_size))

    def is_unvalid(self):
        return self.x < 0 or self.x >= win_dim[0] or self.y < 0 or self.y >= win_dim[1]
       
    def equal_pos(self, other):
        return self.pos == other.pos
        
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = (1, 0)
        self.color = GREEN
        self.body = [Cube(self.x - 2 * cube_size, self.y, self.color), Cube(self.x - cube_size, self.y, self.color), Cube(self.x, self.y, self.color)]
        self.score = 0
    
    def set_dir(self, dir_x, dir_y):
        self.dir = (dir_x, dir_y)

    def move(self):
        self.grow()
        self.body.pop(0)
        
    def eat(self):
        if self.head().equal_pos(apple.cube):
            self.score += 1
            apple.move()
            self.grow()

    def is_dead(self):
        collision = False
        for cube in self.body[:len(self.body) - 1]:
            if cube.equal_pos(self.head()):
                collision = True        
        return self.head().is_unvalid() or collision
       
    def grow(self):
        self.body.append(Cube(self.dir[0] * cube_size + self.head().pos[0], self.dir[1] * cube_size + self.head().pos[1], GREEN))
    
    def head(self):
        return self.body[len(self.body) - 1]

    def draw(self):
        for cube in self.body:
            cube.draw()
        self.draw_eyes()

    def draw_eyes(self):
        if self.dir == (1,0) or self.dir == (-1,0):
            pygame.draw.circle(window, (255, 255, 255), (self.head().x + cube_size / 2, self.head().y + cube_size / 3), 4)
            pygame.draw.circle(window, (255, 255, 255), (self.head().x + cube_size / 2, self.head().y + cube_size * 2 / 3), 4)
            pygame.draw.circle(window, (0,0,0), (self.head().x + cube_size / 2, self.head().y + cube_size / 3), 1)
            pygame.draw.circle(window, (0,0,0), (self.head().x + cube_size / 2, self.head().y + cube_size * 2 / 3), 1)
        else:
            pygame.draw.circle(window, (255, 255, 255), (self.head().x + cube_size / 3, self.head().y + cube_size / 2), 4)
            pygame.draw.circle(window, (255, 255, 255), (self.head().x + cube_size * 2 / 3, self.head().y + cube_size / 2), 4)
            pygame.draw.circle(window, (0,0,0), (self.head().x + cube_size / 3, self.head().y + cube_size / 2), 1)
            pygame.draw.circle(window, (0,0,0), (self.head().x + cube_size * 2 / 3, self.head().y + cube_size / 2), 1)
    def update(self):
        self.move()
        self.eat()
        return self.is_dead()

class Apple:
    def __init__(self, x, y):
        self.cube = Cube(x, y, RED)

    def random_x_pos(self):
        return random.randint(0, int((win_dim[0] / cube_size - 1))) * cube_size

    def random_y_pos(self):
        return random.randint(0, int((win_dim[1] / cube_size - 1))) * cube_size

    def update(self):
        if random.random() < 0.004:
            self.move()
    
    def draw(self):
        self.cube.draw()

    def move(self):
        self.cube = Cube(self.random_x_pos(), self.random_y_pos(), RED) 
        self.draw()

def quit():
    pygame.quit()
    sys.exit()

def draw_score():
    score_label = font.render("Score: " + str(snake.score) , 1, (255, 255, 255))
    window.blit(score_label, (win_dim[0] - 120, 0))

def load_game_over():
    game_over_label = font.render('Game over!', 1, (0,0,255))
    play_again_label = font.render('press enter to play again...', 1, (0,0,255))
    window.blit(game_over_label, (win_dim[0] / 2 - 100, win_dim[1] / 2 - 50))
    window.blit(play_again_label, (win_dim[0] / 2 - 100, win_dim[1] / 2 - 30))
    pygame.display.update()
    play = True
    while play:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            main()
    quit()        

def redraw_screen(): 
    window.fill((0,0,0))
    snake.draw()
    apple.draw()
    draw_grid()
    draw_score()

def draw_grid(): 
    for col in range(int(win_dim[0] / 20)):
        pygame.draw.line(window, (0, 0, 0), (col * 20, 0), (col * 20, win_dim[1]))        
    for row in range(int(win_dim[1] / 20)):
        pygame.draw.line(window, (0, 0, 0), (0, row * 20), (win_dim[0], row * 20)) 
    pygame.draw.line(window, (0, 0, 0), (win_dim[0] - 1, 0), (win_dim[0] - 1, win_dim[1]))
    pygame.draw.line(window, (0, 0, 0), (0, win_dim[1] - 1), (win_dim[0], win_dim[1] - 1))
    
def main():
    global snake, window, apple, font, clock
    pygame.init()
    pygame.display.set_caption('Snake')
    font = pygame.font.SysFont("Comic Sans MS", 24)
    window = pygame.display.set_mode(win_dim)
    clock = pygame.time.Clock()
    snake = Player(100, 100)
    apple = Apple(200, 200)
    running = True
    pygame.display.update()

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            snake.set_dir(1, 0)
        elif keys[pygame.K_LEFT]:
            snake.set_dir(-1, 0)
        elif keys[pygame.K_UP]:
            snake.set_dir(0, -1)
        elif keys[pygame.K_DOWN]:
            snake.set_dir(0, 1)

        if snake.update():
            load_game_over()
        apple.update()
        redraw_screen()
        pygame.display.update()
        #print(snake.score)

    quit()

main()