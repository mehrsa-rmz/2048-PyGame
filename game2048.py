import pygame 
import random

pygame.init()

# initial set up
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 48)

# game colors
colors = {0: (173, 173, 211),
          2: (225, 210, 246),
          4: (226, 195, 243),
          8: (157, 135, 229),
          16: (120, 114, 230),
          32: (109, 130, 233),
          64: (75, 97, 231),
          128: (24, 168, 110),
          256: (21, 143, 94),
          512: (18, 162, 148),
          1024: (14, 128, 117),
          2048: (19, 65, 149),
          'light text': (243, 244, 249),
          'dark text': (92, 88, 132),
          'screen': (217, 235, 247),
          'bg': (190, 201, 250),
          'start_title': (142, 110, 138),
          'light_text_s': (236, 246, 255)}

# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
game_won = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score.txt', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high
first_loop = True

# sound effects
win_sfx = pygame.mixer.Sound("win.wav")
lose_sfx = pygame.mixer.Sound("lose.wav")
movement_sfx = pygame.mixer.Sound("swoosh.wav")

# color changing text
col_spd = 10
minimum = 50
maximum = 250

# flash effect
col_dir_flash = [1, 1, 1]
def_col_flash = [100, 100, 100]
def col_change_flash(col, dir):
    for i in range(3):
        col[i] += col_spd * dir[i]
        if col[i] >= maximum:
            col[i] = minimum
        elif col[i] <= minimum:
            col[i] = maximum

#gradient effect
col_dir_gradient = [[-1, -1, -1], [-1, -1, -1]]
def_col_gradient = [[120, 120, 240], [140, 140, 240]]

def col_change_gradient(col, dir):
    for i in range(3):
        col[i] += col_spd * dir[i]
        if col[i] >= maximum or col[i] <= minimum:
            dir[i] *= -1
    
# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [100, 20, 800, 800], 0, 20)
    score_text = font.render(f'Score: {score}', True, colors['dark text'])
    high_score_text = font.render(f'High Score: {high_score}', True, colors['dark text'])
    screen.blit(score_text, (100, 840))
    screen.blit(high_score_text, (460, 840))
    pass

# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value >= 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = 'black'
            pygame.draw.rect(screen, color, [j * 190 + 140, i * 190 + 60, 150, 150], 0, 10)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 96 - (10 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 190 + 214, i * 190 + 134))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, colors['light text'], [j * 190 + 140, i * 190 + 60, 150, 150], 4, 10)

# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

# take your turn based on direction
def take_turn(direc, board):
    global score
    global game_won
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        if board[i - shift - 1][j] == 2048:
                            game_won = True
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
                        
    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        if board[3 - i + shift][j] == 2048:
                            game_won = True
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    if board[i][j - shift - 1] == 2048:
                        game_won = True
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        if board[i][4 - j + shift] == 2048:
                            game_won = True
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board

# draw game over and restart text
def draw_over(col):
    pygame.draw.rect(screen, 'black', [4 * 50, 6 * 50, 2 * 300, 2 * 100], 0, 2 * 10)
    game_over_text1 = font.render('Game Over!', True, col)
    game_over_text2 = font.render('Press Enter to Restart', True, col)
    screen.blit(game_over_text1, (360, 335))
    screen.blit(game_over_text2, (240, 415))
    
# draw game won and restart text
def draw_win(col):
    pygame.draw.rect(screen, 'black', [4 * 50, 6 * 50, 2 * 300, 2 * 100], 0, 2 * 10)
    game_won_text1 = font.render('You won!', True, col[0])
    game_won_text2 = font.render('Press Enter to Restart', True, col[1])
    screen.blit(game_won_text1, (370, 335))
    screen.blit(game_won_text2, (240, 415))

# draw start screen
def draw_startScreen():
    fundal = pygame.image.load("start_screen.png")
    screen.blit(fundal, (0,0))
    font = pygame.font.Font('freesansbold.ttf', 70)
    text1 = font.render('2048', True, colors['start_title'])

    textRect1 = text1.get_rect()
    surface = pygame.display.get_surface()
    x,y = surface.get_width(), surface.get_height()
    textRect1.center = (x // 2, y // 4 - 30)
    screen.blit(text1, textRect1)

    font = pygame.font.Font('freesansbold.ttf', 40)
    text3 = font.render('Press SPACE to start the game', True, colors['light_text_s'])
    textRect3 = text3.get_rect()
    textRect3.center = (x//2, y//2)
    screen.blit(text3, textRect3)

    start = False
    while not start:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    return start

# draw rules popup
def draw_startPopup():
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render('using the arrow keys', True, colors['light_text_s'])
    textRect = text.get_rect()
    surface = pygame.display.get_surface()
    x,y = surface.get_width(), surface.get_height()
    textRect.center = (x//2, y//2 - 20)
    screen.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 38)
    text = font.render('move tiles in the specified direction', True, colors['light_text_s'])
    textRect = text.get_rect()
    textRect.center = (x//2, y//2 + 30)
    screen.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 42)
    text = font.render('Think you got what it takes ?', True, colors['dark text'])
    textRect = text.get_rect()
    textRect.center = (x//2, y//2 - 120)
    screen.blit(text, textRect)

    popup = False
    while not popup:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    popup = True
                    return popup

# --- MAIN --- game loop
run = True
start = draw_startScreen()
screen.fill(colors['screen'])

draw_board()
popup = draw_startPopup()
while run:
    timer.tick(fps)
    screen.fill(colors['screen'])

    if start:
        draw_board()
        if popup:
            draw_pieces(board_values)
            
            if spawn_new or init_count < 2:
                board_values, game_over = new_pieces(board_values)
                spawn_new = False
                init_count += 1
            
            if direction != '':
                board_values = take_turn(direction, board_values)
                direction = ''
                spawn_new = True
            
            if score > high_score:
                high_score = score
                
            if game_over or game_won:
                if game_over: 
                    draw_over(def_col_flash)
                    col_change_flash(def_col_flash, col_dir_flash)
                    if first_loop:
                        lose_sfx.play(15)
                        first_loop = False
                else:
                    draw_win(def_col_gradient)
                    col_change_gradient(def_col_gradient[0], col_dir_gradient[0])
                    col_change_gradient(def_col_gradient[1], col_dir_gradient[1])
                    if first_loop:
                        win_sfx.play(15)
                        first_loop = False
                    
                if high_score > init_high:
                    file = open('high_score.txt', 'w')
                    file.write(f'{high_score}')
                    file.close()
                    init_high = high_score
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        direction = 'UP'
                        movement_sfx.play()
                    elif event.key == pygame.K_DOWN:
                        direction = 'DOWN'
                        movement_sfx.play()
                    elif event.key == pygame.K_LEFT:
                        direction = 'LEFT'
                        movement_sfx.play()
                    elif event.key == pygame.K_RIGHT:
                        direction = 'RIGHT'
                        movement_sfx.play()
                
                    if game_over or game_won:
                        if event.key == pygame.K_RETURN:
                            win_sfx.stop()
                            lose_sfx.stop()
                            board_values = [[0 for _ in range(4)] for _ in range(4)]
                            spawn_new = True
                            init_count = 0
                            score = 0
                            direction = ''
                            game_over = False
                            game_won = False
                            first_loop = True

    pygame.display.flip()
pygame.quit()