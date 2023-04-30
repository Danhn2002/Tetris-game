import pygame
import random

pygame.font.init()
# GLOBALS VARS
s_width = 1000
s_height = 620
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600   # meaning 600 // 20 = 30 height per block
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

pygame.mixer.init()
sound = pygame.mixer.Sound('sound/Start.mp3')
sound1 = pygame.mixer.Sound('sound/ingame.flac')
sound2 = pygame.mixer.Sound('sound/GameOver.mp3')

# SHAPE FORMATS
S = [['.......',
      '.......',
      '.......',
      '...00..',
      '..00...',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '...0...',
      '...00..',
      '....0..',
      '.......',
      '.......']]
Z = [['.......',
      '.......',
      '.......',
      '..00...',
      '...00..',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '...0...',
      '..00...',
      '..0....',
      '.......',
      '.......']]
I = [['.......',
      '...0...',
      '...0...',
      '...0...',
      '...0...',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '.0000..',
      '.......',
      '.......',
      '.......',
      '.......']]
O = [['.......',
      '.......',
      '...00..',
      '...00..',
      '.......',
      '.......',
      '.......']]
J = [['.......',
      '.......',
      '..0....',
      '..000..',
      '.......',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '...00..',
      '...0...',
      '...0...',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '.......',
      '..000..',
      '....0..',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '...0...',
      '...0...',
      '..00...',
      '.......',
      '.......']]
L = [['.......',
      '.......',
      '....0..',
      '..000..',
      '.......',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '...0...',
      '...0...',
      '...00..',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '.......',
      '..000..',
      '..0....',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '..00...',
      '...0...',
      '...0...',
      '.......',
      '.......']]
T = [['.......',
      '.......',
      '...0...',
      '..000..',
      '.......',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '...0...',
      '...00..',
      '...0...',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '.......',
      '..000..',
      '...0...',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '...0...',
      '..00...',
      '...0...',
      '.......',
      '.......']]
K = [['.......',
      '.0...0.',
      '000.000',
      '.00000.',
      '..000..',
      '...0...',
      '......'],
     ['..0....',
      '.000...',
      '..000..',
      '...000.',
      '..000..',
      '.000...',
      '..0....'],
     ['.......',
      '...0...',
      '..000..',
      '.00000.',
      '000.000',
      '.0...0.',
      '.......'],
     ['....0..',
      '...000.',
      '..000..',
      '.000...',
      '..000..',
      '...000.',
      '....0..'],
      ['.......',
      '.......',
      '.......',
      '...0...',
      '.......',
      '.......',
      '.......']]
M = [['.......',
      '...0...',
      '..000..',
      '.00000.',
      '..000..',
      '...0...',
      '.......'],
     ['.......',
      '.......',
      '...0...',
      '..000..',
      '...0...',
      '.......',
      '.......'],
     ['.......',
      '.......',
      '.......',
      '...0...',
      '.......',
      '.......',
      '.......']]
shapes = [S, Z, I, O, J, L, T, K, M]
shape_colors = [(0, 255, 0), (255, 255, 153), (0, 255, 255), (244, 169, 96), (255, 178, 102), (50, 50, 255), (255, 255, 102), (255, 153, 204),(153,51,255)]
clock = pygame.time.Clock()


# index 0 - 6 represent shape
class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # *
    grid = [[(50,142,213) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (50,142,213)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (0,0,0), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (0,0,0), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (50,142,213) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
   
    font = pygame.font.SysFont('comicsans', 35)
    label = font.render('Next Shape', 1, (255,255,255))
    sx = top_left_x + play_width + 68
    sy = top_left_y + play_height/2 - 230
    format = shape.shape[shape.rotation % len(shape.shape)]


    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('C:\Python\Tetris nâng cao\scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score=0, last_score = 0, fall_speed=0):
    surface.fill((255, 255, 255))
    image1 = pygame.image.load('image/back.webp')
    image1 = pygame.transform.scale(image1, (s_width,s_height))
    surface.blit(image1,(top_left_x-350,top_left_y-20))
    pygame.font.init()
    # current score
    sx = top_left_x + play_width + 100
    sy = top_left_y + play_height/2 - 100
    image0 = pygame.image.load('image/score.png')
    image0 = pygame.transform.scale(image0, (200,100))
    surface.blit(image0,(sx - 29, sy + 100))
    font = pygame.font.SysFont('comicsans', 50)
    label = font.render('' + str(score), 1, (255,255,255))
    surface.blit(label, (sx + 60 , sy + 115))
    #higt-score
    image2 = pygame.image.load('image/hight-score.png')
    image2 = pygame.transform.scale(image2, (200,100))
    surface.blit(image2,(sx - 29, sy + 200))
    # last score
    label = font.render('' + last_score, 1, (255,255,255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 40
    surface.blit(label, (sx + 90, sy + 230))
    #level
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('' + str(int(fall_speed)), 1, (255,255,255))
    sx = top_left_x - 270
    sy = top_left_y + 300
    surface.blit(label, (top_left_x-120,top_left_y+290))
    image3 = pygame.image.load('image/speed.webp')
    image3 = pygame.transform.scale(image3, (170, 170))
    surface.blit(image3, (top_left_x-320,top_left_y+250))


    #draw image
    image = pygame.image.load('image/meme.png')
    image = pygame.transform.scale(image, (300, 300))
    surface.blit(image, (top_left_x - 320 ,top_left_y - 20 ))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    draw_grid(surface, grid)


def main(screen): 
    sound.stop()
    sound1.play(loops=10)
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.8
    fall_speed1 = 0
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                        pygame.display.update()
                    pygame.display.update()
                
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        pygame.display.update()
                    pygame.display.update()
                
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                        pygame.display.update()
                    pygame.display.update()
                
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                        pygame.display.update()
                    pygame.display.update()
                
                if event.key == pygame.K_SPACE:
                    # Move piece down until it cannot move further
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                        pygame.display.update()
                    current_piece.y -= 1
                    pygame.display.update()
                
                if event.key == pygame.K_1:
                    fall_speed = 0.7
                    fall_speed1 = 0.5
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        pygame.display.update()
                    pygame.display.update()
                
                if event.key == pygame.K_2:
                    fall_speed = 0.6
                    fall_speed1 = 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        pygame.display.update()
                    pygame.display.update()
                
                if event.key == pygame.K_3:
                    fall_speed1 = 1.5
                    fall_speed = 0.5
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        pygame.display.update()
                    pygame.display.update()
                
                if event.key == pygame.K_4:
                    fall_speed1 = 2
                    fall_speed = 0.4
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        pygame.display.update()
                    pygame.display.update()
                
                if event.key == pygame.K_5:
                    fall_speed1 = 2.5
                    fall_speed = 0.3
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        pygame.display.update()
                    pygame.display.update()
                
                if event.key == pygame.K_6:
                    fall_speed1 = 3
                    fall_speed = 0.2
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        pygame.display.update()
                    pygame.display.update()
                    
                if event.key == pygame.K_7:
                    fall_speed1 = 3.5
                    fall_speed = 0.1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        pygame.display.update()
                    pygame.display.update()

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(screen, grid, score, last_score, fall_speed1*2)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        if check_lost(locked_positions):
            screen.fill((255,255,255))
            sound1.stop()
            image4 = pygame.image.load('image/gameover.jpg')
            image4 = pygame.transform.scale(image4, (300, 300))
            screen.blit(image4, (350,200))
            pygame.display.update()
            sound2.play()
            pygame.time.delay(5000)
            run = False
            update_score(score)
        pygame.display.update()

def main_menu(screen): 
    run = True
    while run:
        screen.fill((255,255,255))
        draw_text_middle(screen, 'Press Any Key To Play', 40, (0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(screen)
        clock.tick(120)
    pygame.display.quit()
sound.play()
screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(screen)