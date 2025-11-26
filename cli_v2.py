import time
import sys
import select
import tty
import termios

def isData(timeout=0):
  return select.select([sys.stdin], [], [], timeout)[0] != []

old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())


TETRIMINOS_STRINGS = [
  # 1
  """
  ...X
  ...X
  ...X
  ...X
  """,

  # 2
  """
  ..X.
  .XX.
  .X..
  ....
  """,

  # 3
  """
  .X..
  .XX.
  ..X.
  ....
  """,

  # 4
  """
  .XXX
  ..X.
  ....
  ....
  """,

  # 5
  """
  ....
  .XX.
  .XX.
  ....
  """,

  # 6
  """
  X...
  X...
  XX..
  ....
  """,

  # 7
  """
  .X..
  .X..
  .X..
  XX..
  """
] 

def convert_tetriminos_string_to_2d_array() -> list[list[str]]:
  # 1d array
  # break into 1d array first
  two_d_array_tetriminos = []
  for tetrimino in TETRIMINOS_STRINGS:
    lines_list = [line for line in tetrimino.splitlines() if line.strip() != '']
    lines_list_striped = [line.replace(' ', '').replace('\n', '').replace('\t', '') for line in lines_list]
    array_version = []
    for line in lines_list_striped:
      for char in line:
        array_version.append(char)
      # ['.', '.', '.', 'X', '.', '.', '.', '.', 'X', '.', '.', '.', '.', 'X', '.', '.', '.', '.', 'X', '.']
    two_d_array_tetriminos.append(array_version)
  return two_d_array_tetriminos

TETRIMINOS = convert_tetriminos_string_to_2d_array()

"""
0  1   2    3 
4  5   6    7
8  9   10   11
12 13  14   15

normal:
i = row * w + col (a[row][col])

90 degree clockwise:
i = 12 + row - (col * 4) 
12 8 4 0
13 9 5 1
14 10 6 2
15 11 7 3

180 degree clockwise:
i = 15 - (row * 4) - col

270 degree clockwise:
i = 3 - row + (4 * col)

-----------------------------------------
90 degree counter-clockwise = 270 degree clockwise
180 degree counter-clockwise = 180 degree clockwise
270 degree counter-clockwise = 90 degree clockwise
"""

def rotate(col, row, r=0):
  if r == 0:
    i = row * 4 + col
  if r == 90 or r == -270:
    i = 12 + row - (col * 4)
  if r == 180 or r == -180:
    i = 15 - (row * 4) - col
  if r == 270 or r == -90:
    i = 3 - row + (4 * col)
  return i


WIDTH = 12
HEIGHT = 18

def get_i_board(row, col):
  i = row * WIDTH + col
  return i


def setup_board():
  # 2d version
  # board = [ ['.']*WIDTH for col in range(HEIGHT)]
  # board = []
  # for row in range(HEIGHT):
  #   new_row = []
  #   for col in range(WIDTH):
  #     if col == 0 or col == WIDTH - 1:
  #       new_row.append('X')
  #     elif row == HEIGHT - 1:
  #       new_row.append('X')
  #     else:
  #       new_row.append('.')
  #   board.append(new_row)
  # # print(board)
  # return board

  # 1d version
  board = []
  for row in range(HEIGHT):
    for col in range(WIDTH):
      i = get_i_board(row, col)
      if col == 0 or col == WIDTH - 1:
        board.append('X')
      elif row == HEIGHT - 1:
        board.append('X')
      else:
        board.append('.')
  return board

import os
def print_board(board):
  # 2d version
  # for row in range(HEIGHT):
  #   for col in range(WIDTH):
  #     print(board[row][col], end='')
  #   print()

  os.system('clear')
  # 1d version
  for row in range(HEIGHT):
    for col in range(WIDTH):
      i = get_i_board(row, col)
      # print(i, end=' ')
      if board[i] == '.':
        print(' ', end='')
      else:
        print(board[i], end='')
    print()


def print_tetrimino(tetrimino: list[str], r=0):
  """
  For testing
  """
  # tetrimino = ['.', '.', '.', 'X', '.', '.', '.', '.', 'X', '.', '.', '.', '.', 'X', '.', '.', '.', '.', 'X', '.']
  for row in range(4):
    for col in range(4):
      i = rotate(col, row, r)
      # print(i, end=' ')
      print(tetrimino[i], end='')
    print()


def test():
  random_tetrimino = TETRIMINOS[get_random_tetrimino()]
  print_tetrimino(random_tetrimino)
  print()
  print_tetrimino(random_tetrimino, r=90)


def get_random_tetrimino():
  import random
  random_num = random.randrange(0, 7)
  return random_num


def get_user_input():
  if isData(0.1):  # Shorter timeout for responsiveness
    key = read_key(0.1)  # Try to read a key sequence
    if key:
      # print(f"DEBUG: Key received: {key}")  # Debug print
      if key == 'RIGHT':
        return 'Right'
      elif key == 'LEFT':
        return 'Left'
      elif key == 'DOWN':
        return 'Down'
      elif key == 'UP':
        return 'Up'
      elif key in ('R', 'r'):
        return 'R'
      elif key in ('L', 'l'):
        return 'L'
    return None


def read_key(timeout=0):
  if isData(timeout):  # Check if there's input within the timeout
    c1 = sys.stdin.read(1)  # Read the first byte

    # If it's the ESC key, check for the full arrow key sequence
    if c1 == '\x1b':  # ESC key
      if isData(timeout):  # Check if there's more input
        c2 = sys.stdin.read(1)  # Read the next byte
        if c2 == '[':
          if isData(timeout):  # Check if there's more input
            c3 = sys.stdin.read(1)  # Read the final byte
            # Handle arrow keys
            if c3 == 'C':
              return "RIGHT"
            elif c3 == 'D':
              return "LEFT"
            elif c3 == 'B':
              return "DOWN"
            elif c3 == 'A':
              return "UP"
    elif c1 in ('R', 'r'):
      return 'R'
    elif c1 in ('L', 'l'):
      return 'L'
    return c1  # Return the single character if not an arrow key
  return None  # Return None if no input is available


# todo check block clear and lose
def game_logic(board):
    current_piece: list[str] = TETRIMINOS[0]
    current_piece_rotation = 0
    currentCol = WIDTH // 2
    currentRow = 0
    piece_reset = False
    score = 0
    lines = []

    game_over = False
    last_tick = time.time()
    # game loop
    while not game_over:
      if piece_reset:
        # if next piece doesn't fit, game over
        fits = does_piece_fit(board, (currentRow, currentCol), current_piece, current_piece_rotation)
        if not fits:
            game_over = True
            break

        # permanently place piece in board
        update_tetrimino_in_board(board, current_piece, current_piece_rotation, currentRow, currentCol, 'M')
        piece_reset = False
        current_piece: list[str] = TETRIMINOS[0]
        current_piece_rotation = 0
        currentCol = WIDTH // 2
        currentRow = 0

      # Draw
      update_tetrimino_in_board(board, current_piece, current_piece_rotation, currentRow, currentCol)
      print_board(board)
      print(f'Score: {score}')

      # move pieces down if lines
      if len(lines) > 0:
        for line in lines:
          for col in range(1, WIDTH - 1):
            for row in range(line, 0, -1):
              board[(row * WIDTH) + col] = board[(row - 1) * WIDTH + col]
        lines = []

      # Get user input (also timing) and check if user input fits
      fits = False
      user_input = get_user_input()
      if user_input:
        pass
        # print(f"User Input: {user_input}")

      now = time.time()
      # wait 1 sec before moving piece
      if now - last_tick >= 1:
        last_tick = now
        # print("TICK (1 second update)")

        # Clear keyboard input buffer
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

        # remove old state position of tetrimino, get ready to move it
        remove_tetrimino_from_board(board, current_piece, current_piece_rotation, currentRow, currentCol)

        # Handle user input or default movement
        if user_input == 'Left':
          if does_piece_fit(board, (currentRow, currentCol - 1), current_piece, current_piece_rotation):
            currentCol -= 1
        elif user_input == 'Right':
          if does_piece_fit(board, (currentRow, currentCol + 1), current_piece, current_piece_rotation):
            currentCol += 1
        elif user_input == 'Down':
          if does_piece_fit(board, (currentRow + 1, currentCol), current_piece, current_piece_rotation):
            currentRow += 1
        elif user_input == 'R':
          if does_piece_fit(board, (currentRow, currentCol), current_piece, current_piece_rotation + 90):
            print('yes')
            current_piece_rotation = current_piece_rotation + 90
          else:
            print('no')
        elif user_input == 'L':
          if does_piece_fit(board, (currentRow, currentCol), current_piece, current_piece_rotation - 90):
            current_piece_rotation = current_piece_rotation - 90
        
        # Default behavior: move down
        if does_piece_fit(board, (currentRow + 1, currentCol), current_piece, current_piece_rotation):
          currentRow += 1
        else:
          piece_reset = True

        # Check if the piece hits the bottom or another piece
        fits = does_piece_fit(board, (currentRow + 1, currentCol), current_piece, current_piece_rotation)
        if not fits:
          # if hits bottom, reset piece
          update_tetrimino_in_board(board, current_piece, current_piece_rotation, currentRow, currentCol)
          piece_reset = True
          # Check for completed lines, replace with =
          for row in range(4):
            if currentRow + row < HEIGHT - 1:
              line = True
              for col in range(1, WIDTH - 1):
                if board[(currentRow + row) * WIDTH + col] not in ('O', 'M'):
                    line = False
              if line:
                lines.append(currentRow + row)
                score += 1
                # Remove line, set to '='
                for col in range(1, WIDTH - 1):
                    board[(currentRow + row) * WIDTH + col] = '='
    
    time.sleep(0.1) # reduce cpu usage
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings) # clear stuff
    print('Game Over')
    print(f'Score: {score}')
      
    
def update_tetrimino_in_board(board: list[str], current_piece: list[str], current_piece_rotation: int, 
                              currentRow: int, currentCol: int, piece_val='O'):
  for row in range(4):
    for col in range(4):
      i = rotate(col, row, current_piece_rotation)
      field_i = (currentRow + row) * WIDTH + (currentCol + col)
      if current_piece[i] == 'X' and board[field_i] != '=': # if tetrimino piece has a value, add it to the board
        board[(currentRow + row) * WIDTH + (currentCol + col)] = piece_val # the magic


def remove_tetrimino_from_board(board: list[str], current_piece: list[str], current_piece_rotation: int, 
                              currentRow: int, currentCol: int):
  # remove old values for next draw
  for row in range(4):
    for col in range(4):
      i = rotate(col, row, current_piece_rotation)
      if current_piece[i] == 'X': # if tetrimino piece has a value, add it to the board
        board[(currentRow + row) * WIDTH + (currentCol + col)] = '.'


# does_piece_fit(board, (currentRow + 1, currentCol), tetrimino_id, current_piece_rotation)
def does_piece_fit(board: list[str], location_in_array: tuple[int, int], tetrimino_piece: list[str], 
                   current_rotation: int) -> bool: 
  # location_in_array is (row, col)
  row_i_in_array, col_i_in_array = location_in_array
  for row in range(4):
    for col in range(4): 
      # check if each tetrimino piece's cell is a value, if so check if it fits in the boards value when inserted

      # index into piece
      piece_i = rotate(col, row, r=current_rotation)

      # index into board array (row * width + x)
      field_i = (row_i_in_array + row) * WIDTH + (col_i_in_array + col) # y * width + x

      # collision detection
      if (col_i_in_array + col >= 0) and (col_i_in_array + col < WIDTH):
        if (row_i_in_array + row >= 0) and (row_i_in_array + row < HEIGHT):
          # main check thing, if piece index is a blck, and it's board index is not and not fully placed piece (M)
          if (tetrimino_piece[piece_i] == 'X') and ( (board[field_i] == 'X') or (board[field_i] == 'M') ): 
            return False # fail on first hit
  return True


def main():
  board = setup_board()
  # print_board(board)
  # test()
  game_logic(board)
  


if __name__ == '__main__':
  main()