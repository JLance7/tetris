import pygame
from enum import Enum
import sys

# Constants
FPS = 6
X_OFFSET = 50
Y_OFFSET = 50
WIDTH = 1260
HEIGHT = 900 + Y_OFFSET
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

def main():
  pygame.init()
  pygame.font.init()
  INFO = pygame.display.Info()
  pygame.display.set_caption("Tetris")
  clock = pygame.time.Clock()

  run = True
  direction = Direction.DOWN
  while run:
    time = clock.tick(FPS)
    direction = check_events(direction)
    # print(direction)
    draw_screen()


class Direction(Enum):
  DOWN = 0
  RIGHT = 1
  LEFT = 2


def check_events(direction: Direction):
  new_direction = Direction.DOWN
  for event in pygame.event.get():
    # key pressed
    if event.type == pygame.KEYDOWN:      
      if event.key == pygame.K_UP:
        new_direction = Direction.UP
      elif event.key == pygame.K_DOWN:
        new_direction = Direction.DOWN
      elif event.key == pygame.K_RIGHT:
        new_direction = Direction.RIGHT
      elif event.key == pygame.K_LEFT:
        new_direction = Direction.LEFT
      else:
        new_direction = direction

    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit() 
  return new_direction

def draw_screen():
  pygame.draw.rect(WIN, BLACK, BACKGROUND)
  pygame.draw.rect(WIN, GRAY, GAME_BOARD_RECT)
  draw_lines()
  draw_text()
  # # food
  # draw_cube(food_pos_x, food_pos_y, RED)
  # # snake
  # for segment in snake:
  #   draw_cube(segment.x, segment.y, GREEN)
  # show_score(score)
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
  end = BOARD_HEIGHT * BOARD_BLOCK_HEIGHT
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


if __name__ == '__main__':
  main()