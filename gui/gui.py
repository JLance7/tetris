import pygame
from enum import Enum
import sys
from logic import setup, get_random_tetrimino, update_tetrimino_in_board, rotate, get_i_board 
from logic import remove_tetrimino_from_board, does_piece_fit

# Constants
FPS = 3
X_OFFSET = 50
Y_OFFSET = 50
WIDTH = 1260
HEIGHT = 900 + Y_OFFSET * 2
GAME_BOARD_WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
BOARD_WIDTH = 12
BOARD_HEIGHT = 18
BOARD_BLOCK_WIDTH = 50
BOARD_BLOCK_HEIGHT = 50
BOARD_START_X = GAME_BOARD_WIDTH / 2

# Rectangles
BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT) 
GAME_BOARD_RECT = pygame.Rect(BOARD_START_X, 0 + Y_OFFSET, GAME_BOARD_WIDTH, HEIGHT - Y_OFFSET*2)  

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
GREEN = (0, 255, 0)

pygame.init()
MY_CUSTOM_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MY_CUSTOM_EVENT, 1000) 

def main():
  pygame.font.init()
  INFO = pygame.display.Info()
  pygame.display.set_caption("Tetris")
  clock = pygame.time.Clock()

  run = True
  direction = Direction.DOWN

  # initial setup
  TETRIMINOS, board = setup()
  current_piece: list[str] = TETRIMINOS[get_random_tetrimino()]
  current_piece_rotation = 0
  currentCol = 18 // 2
  currentRow = 0
  piece_reset = False
  score = 0
  lines = []

  game_over = False

  while run:
    time = clock.tick(FPS)
    # direction = check_events(direction)
    # print(direction)

    # logic
    if piece_reset:
      # permanently place piece in board
      update_tetrimino_in_board(board, current_piece, current_piece_rotation, currentRow, currentCol, 'M')
      if game_over: return
      piece_reset = False
      current_piece: list[str] = TETRIMINOS[get_random_tetrimino()]
      current_piece_rotation = 0
      currentCol = BOARD_WIDTH // 2
      currentRow = 0
    
    # Draw
    update_tetrimino_in_board(board, current_piece, current_piece_rotation, currentRow, currentCol)
    draw_screen(board)

    # move pieces down if lines
    if len(lines) > 0:
      for line in lines:
        for col in range(1, BOARD_WIDTH - 1):
          for row in range(line, 0, -1):
            board[(row * BOARD_WIDTH) + col] = board[(row - 1) * BOARD_WIDTH + col]
      lines = []

    # Get user keyboard input and check if user input fits
    fits = False
    
    new_direction = Direction.DOWN
    user_input = new_direction
    # check user input and events
    for event in pygame.event.get():
      # key pressed
      if event.type == pygame.KEYDOWN:      
        if event.key == pygame.K_DOWN:
          new_direction = Direction.DOWN
        elif event.key == pygame.K_RIGHT:
          new_direction = Direction.RIGHT
        elif event.key == pygame.K_LEFT:
          new_direction = Direction.LEFT
        elif event.key == pygame.K_r:
          new_direction = Direction.R
        elif event.key == pygame.K_l:
          new_direction = Direction.L
        else:
          new_direction = direction
        user_input = new_direction
      elif event.type == MY_CUSTOM_EVENT:
        # This code will execute every 1 second
        print("Action performed!")
        # Default behavior: move down
        if does_piece_fit(board, (currentRow + 1, currentCol), current_piece, current_piece_rotation):
          remove_tetrimino_from_board(board, current_piece, current_piece_rotation, currentRow, currentCol)
          currentRow += 1
        else:
          piece_reset = True

      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit() 

    # remove old state position of tetrimino, get ready to move it
    remove_tetrimino_from_board(board, current_piece, current_piece_rotation, currentRow, currentCol)

    # Handle user input or default movement
    if user_input == Direction.LEFT:
      if does_piece_fit(board, (currentRow, currentCol - 1), current_piece, current_piece_rotation):
        currentCol -= 1
    elif user_input == Direction.RIGHT:
      if does_piece_fit(board, (currentRow, currentCol + 1), current_piece, current_piece_rotation):
        currentCol += 1
    # elif user_input == Direction.DOWN:
    #   if does_piece_fit(board, (currentRow + 1, currentCol), current_piece, current_piece_rotation):
    #     currentRow += 1
    elif user_input == 'R':
      if does_piece_fit(board, (currentRow, currentCol), current_piece, current_piece_rotation + 90):
        current_piece_rotation = current_piece_rotation + 90
    elif user_input == 'L':
      if does_piece_fit(board, (currentRow, currentCol), current_piece, current_piece_rotation - 90):
        current_piece_rotation = current_piece_rotation - 90
  

    # Check if the piece hits the bottom or another piece
    fits = does_piece_fit(board, (currentRow + 1, currentCol), current_piece, current_piece_rotation)
    if not fits:
      # if hits bottom, reset piece
      update_tetrimino_in_board(board, current_piece, current_piece_rotation, currentRow, currentCol)
      piece_reset = True
      # Check for completed lines, replace with =
      for row in range(4):
        if currentRow + row < BOARD_HEIGHT - 1:
          line = True
          for col in range(1, BOARD_WIDTH - 1):
            # O is current pice, M is placed piece, X is value in tetrimino piece array
            if board[(currentRow + row) * BOARD_WIDTH + col] not in ('O', 'M'):
              line = False
          if line:
            lines.append(currentRow + row)
            score += 1
            # Remove line, set to '='
            for col in range(1, BOARD_WIDTH - 1):
              board[(currentRow + row) * BOARD_WIDTH + col] = '='
  

  print('Game Over')
  print(f'Score: {score}')


class Direction(Enum):
  DOWN = 0
  RIGHT = 1
  LEFT = 2
  R = 3
  L = 4


def draw_screen(board):
  pygame.draw.rect(WIN, BLACK, BACKGROUND)
  pygame.draw.rect(WIN, GRAY, GAME_BOARD_RECT)
  draw_lines()
  draw_text()
  draw_board(board)
  pygame.display.update()


def draw_lines():
  # vertical lines
  start = int(BOARD_START_X) + BOARD_BLOCK_WIDTH 
  end = (BOARD_WIDTH * BOARD_BLOCK_WIDTH) + BOARD_START_X  
  end = int(end)
  increment = BOARD_BLOCK_WIDTH 
  # print('start', start, 'end', end, 'increment', increment)
  line_width = 1
  for x in range(start, end, increment):
    # print(x)
    # left, top, width, height
    line = pygame.Rect(x - line_width, 0 + Y_OFFSET, line_width, HEIGHT - Y_OFFSET * 2)
    pygame.draw.rect(WIN, WHITE, line)

  # 18 horizontal lines
  start = BOARD_BLOCK_HEIGHT
  end = BOARD_HEIGHT * BOARD_BLOCK_HEIGHT + Y_OFFSET
  increment = BOARD_BLOCK_HEIGHT
  for y in range(start, end, increment):
    # left, top, width, height
    line = pygame.Rect(BOARD_START_X, y - line_width, GAME_BOARD_WIDTH, line_width)
    pygame.draw.rect(WIN, WHITE, line)


def draw_text():
  score = 0
  my_font2 = pygame.font.SysFont('Bahnschrift', 40)
  score_text = my_font2.render(f'Score: {score}', True, WHITE)
  x = 0 + WIDTH//12
  y = 0 + HEIGHT//12
  WIN.blit(score_text, (x, y))


def draw_board(board: list[str]):
  for row in range(18):
    for col in range(12):
      i = get_i_board(row, col)
      # print(i, end=' ')
      if board[i] == '.':
        # empty cube
        pass
      else:
        value = board[i]
        left = int(BOARD_START_X) + (BOARD_BLOCK_WIDTH * col)
        top = Y_OFFSET + (BOARD_BLOCK_HEIGHT * row)
        width = BOARD_BLOCK_WIDTH
        height = BOARD_BLOCK_HEIGHT
        cube = pygame.Rect(left, top, width, height)
        pygame.draw.rect(WIN, GREEN, cube)


if __name__ == '__main__':
  main()