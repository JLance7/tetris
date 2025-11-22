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


def print_board(board):
  # 2d version
  # for row in range(HEIGHT):
  #   for col in range(WIDTH):
  #     print(board[row][col], end='')
  #   print()

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
  answer = input('Input (enter to do nothing, L for rotate left, R for rotate right)')
  answer = answer.capitalize()
  return answer


def game_logic(board):
  current_piece: list[str] = TETRIMINOS[get_random_tetrimino()]
  current_piece_rotation = 0
  currentCol = WIDTH // 2
  currentRow = 0
  
  # game loop
  while True:
    # update tetrimino in board array
    update_tetrimino_in_board(board, current_piece, current_piece_rotation, currentRow, currentCol)

    # Draw board
    print_board(board)
    
    # Get user input (also timing)
    user_input = get_user_input()
    

def update_tetrimino_in_board(board: list[str], current_piece: list[str], current_piece_rotation: int, 
                              currentRow: int, currentCol: int):
  for row in range(4):
    for col in range(4):
      i = rotate(col, row, current_piece_rotation)
      if current_piece[i] == 'X': # if tetrimino piece has a value, add it to the board
        board[(currentRow + row) * WIDTH + (currentCol + col)] = 'O'


def does_piece_fit(board: list[str], location_in_array: tuple[int, int], tetrimino_id: int, current_rotation: int): 
  # location_in_array is (row, col)
  row_i_in_array, col_i_in_array = location_in_array
  for row in range(4):
    for col in range(4):
      # index into piece
      piece_i = rotate(col, row, r=current_rotation)

      # index into board array (row * width + x)
      field_i = (row_i_in_array + row) * WIDTH + (col_i_in_array + col)

      # collision detection
      if (col_i_in_array + col >= 0) and (col_i_in_array + col < WIDTH):
        if (row_i_in_array + row >= 0) and (row_i_in_array + row < HEIGHT):
          if (TETRIMINOS[tetrimino_id][piece_i] == 'X') and (board[field_i] != '.'):
            return False # fail on first hit
  return True


def main():
  board = setup_board()
  # print_board(board)
  # test()
  game_logic(board)
  


main()