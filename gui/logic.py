import time
import sys

WIDTH = 12
HEIGHT = 18

def setup():
  
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
  
  def setup_board():
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
  board = setup_board()

  return TETRIMINOS, board


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


def get_i_board(row, col):
  i = row * WIDTH + col
  return i


def get_random_tetrimino():
  import random
  random_num = random.randrange(0, 7)
  return random_num
      
    
def update_tetrimino_in_board(board: list[str], current_piece: list[str], current_piece_rotation: int, 
                              currentRow: int, currentCol: int, piece_val='O'):
  global game_over
  # if next piece doesn't fit, game over
  fits = does_piece_fit(board, (currentRow, currentCol), current_piece, current_piece_rotation)
  if not fits:
    game_over = True
    return
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


