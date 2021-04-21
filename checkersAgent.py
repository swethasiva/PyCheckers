from collections import defaultdict
from copy import deepcopy
import sys

row_encoding = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
column_encoding = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
my_turn = False
my_coins_left = 0
opponent_coins_left = 0
my_turn = False
opp_color = None
valid_moves = []
moves_boards = defaultdict(list)
max_depth = 1
def count_pieces(board, player_color):
    global my_coins_left, opponent_coins_left
    for i in range(0, 8):
        for j in range(0, 8):
            if (board[i][j].lower() == player_color):
                my_coins_left += 1
            elif (board[i][j].lower() != "."):
                opponent_coins_left += 1
            else:
                continue
    return

def encode_player_color(player_color):
    if (player_color == "black"):
        player_color = "b"
    elif (player_color == "white"):
        player_color = "w"
    return player_color


def parse_input():
    with open("input.txt", "r") as f:
        game_data = f.readlines()
    game_board = []
    game_type = game_data[0].strip("\n").lower()
    player_color = game_data[1].strip("\n").lower()
    game_time = game_data[2].strip("\n")
    for row in range(3, len(game_data)):
        game_board.append(list(game_data[row].strip("\n")))
    return game_board, game_type, game_time, player_color

def check_my_turn(player_color, game_type):
    global my_turn
    if ((player_color == "b" and game_type == "game") or (game_type == "single")):
        my_turn = True
    return

def white_simple_moves(game_board, i, j, boards, depth, is_king):
    global valid_moves
    global moves_boards
    move_type = "E"
    make_king = False
    is_left, is_right = False, False
    is_foward, is_backward = False, False
    if ((i - 1) == 0):
        make_king = True
    # Is there a valid simple-left-forward-move
    if ((i - 1) >= 0 and (i - 1) <= 7 and (j - 1) >= 0 and (j - 1) <= 7 and (game_board[i - 1][j - 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i - 1) + str(j - 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        if (make_king):
            my_coin = my_coin.upper()
        new_board[i - 1][j - 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)

    if ((i - 1) >= 0 and (i - 1) <= 7 and (j + 1) >= 0 and (j + 1) <= 7 and (game_board[i - 1][j + 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i - 1) + str(j + 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        if (make_king):
            my_coin = my_coin.upper()
        new_board[i - 1][j + 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)
    return

def white_jump_moves(game_board, i, j, boards, depth, is_king, moves=None):
    if moves is None:
        moves = []
    global valid_moves
    global moves_boards
    #print("entering recursion")
    move_type = "J"
    is_left, is_right = False, False
    # Is there a valid jump-left-forward-move
    if ((i - 2) >= 0 and (i - 2) <= 7 and (j - 2) >= 0 and (j - 2) <= 7 and (game_board[i - 2][j - 2] == ".") and (
            game_board[i - 1][j - 1].lower() == "b")):
        if ((i - 2) == 0 and not is_king):
            is_king = True
        #print("left_called")
        my_move = "J " + str(i) + str(j) + " " + str(i - 2) + str(j - 2)
        moves.append(my_move)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i - 1][j - 1] = "."
        if (is_king):
            my_coin = my_coin.upper()
        new_board[i - 2][j - 2] = my_coin
        is_left = True
        white_jump_moves(new_board, i - 2, j - 2, boards, depth, is_king, moves)

    # Is there a valid jump-right-forward-move
    if ((i - 2) >= 0 and (i - 2) <= 7 and (j + 2) >= 0 and (j + 2) <= 7 and (game_board[i - 2][j + 2] == ".") and (game_board[i - 1][j + 1].lower() == 'b')):
        #print("right_called")
        if ((i - 2) == 0 and not is_king):
            is_king = True
        my_move = "J " + str(i) + str(j) + " " + str(i - 2) + str(j + 2)
        moves.append(my_move)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i - 1][j + 1] = "."
        if (is_king):
            my_coin = my_coin.upper()
        new_board[i - 2][j + 2] = my_coin
        is_right = True
        white_jump_moves(new_board, i - 2, j + 2, boards, depth, is_king, moves)

    if (is_left == False and is_right == False and moves):
        print("adding to valid moves")
        valid_moves.append(deepcopy(moves))
        boards.append(game_board)
        if (depth == max_depth):
            moves_boards[str(moves)] = game_board
        if (len(moves) > 0):
            moves.pop()

    return

def white_king_simple_moves(game_board, i, j, boards, depth, is_king):
    move_type = "E"
    # Is there a valid simple-left-forward-move
    if ((i - 1) >= 0 and (i - 1) <= 7 and (j - 1) >= 0 and (j - 1) <= 7 and (game_board[i - 1][j - 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i - 1) + str(j - 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i - 1][j - 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)

    # Is there a valid simple-right-forward-move
    if ((i - 1) >= 0 and (i - 1) <= 7 and (j + 1) >= 0 and (j + 1) <= 7 and (game_board[i - 1][j + 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i - 1) + str(j + 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i - 1][j + 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)

    # Is there a valid simple-left-backward-move
    if ((i + 1) >= 0 and (i + 1) <= 7 and (j - 1) >= 0 and (j - 1) <= 7 and (game_board[i + 1][j - 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i + 1) + str(j - 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i + 1][j - 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)

    # Is there a valid simple-right-backward-move
    if ((i + 1) >= 0 and (i + 1) <= 7 and (j + 1) >= 0 and (j + 1) <= 7 and (game_board[i + 1][j + 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i + 1) + str(j + 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i + 1][j + 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)
    return

def white_king_jump_moves(game_board, i, j, boards, depth, is_king, moves = []):
    if moves is None:
        moves = []
    global valid_moves
    global moves_boards
    #print("entering recursion")
    move_type = "J"
    is_left, is_right = False, False
    # Is there a valid jump-left-forward-move
    if ((i - 2) >= 0 and (i - 2) <= 7 and (j - 2) >= 0 and (j - 2) <= 7 and (game_board[i - 2][j - 2] == ".") and (
            game_board[i - 1][j - 1].lower() == "b")):
        print("left_called")
        my_move = "J " + str(i) + str(j) + " " + str(i - 2) + str(j - 2)
        moves.append(my_move)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i - 1][j - 1] = "."
        new_board[i - 2][j - 2] = my_coin
        is_left = True
        white_king_jump_moves(new_board, i - 2, j - 2, boards, depth, is_king, moves)

    # Is there a valid jump-right-forward-move
    if ((i - 2) >= 0 and (i - 2) <= 7 and (j + 2) >= 0 and (j + 2) <= 7 and (game_board[i - 2][j + 2] == ".") and (
            game_board[i - 1][j + 1].lower() == "b")):
        print("right_called")
        my_move = "J " + str(i) + str(j) + " " + str(i - 2) + str(j + 2)
        moves.append(my_move)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i - 1][j + 1] = "."
        is_right = True
        new_board[i - 2][j + 2] = my_coin
        is_right = True
        white_king_jump_moves(new_board, i - 2, j + 2, boards, depth, is_king, moves)

    if (is_king):
        if ((i + 2) >= 0 and (i + 2) <= 7 and (j - 2) >= 0 and (j - 2) <= 7 and (game_board[i + 2][j - 2] == ".") and (
                game_board[i + 1][j - 1].lower() == "b")):
            print("king left_called")
            my_move = "J " + str(i) + str(j) + " " + str(i + 2) + str(j - 2)
            moves.append(my_move)
            new_board = deepcopy(game_board)
            my_coin = new_board[i][j]
            new_board[i][j] = "."
            new_board[i + 1][j - 1] = "."
            new_board[i + 2][j - 2] = my_coin
            is_left = True
            white_king_jump_moves(new_board, i + 2, j - 2, boards, depth, is_king, moves)

        # Is there a valid jump-right-forward-move
        if ((i + 2) >= 0 and (i + 2) <= 7 and (j + 2) >= 0 and (j + 2) <= 7 and (game_board[i + 2][j + 2] == ".") and (
                game_board[i + 1][j + 1].lower() == "b")):
            print("right_called")
            my_move = "J " + str(i) + str(j) + " " + str(i + 2) + str(j + 2)
            moves.append(my_move)
            new_board = deepcopy(game_board)
            my_coin = new_board[i][j]
            new_board[i][j] = "."
            new_board[i + 1][j + 1] = "."
            is_right = True
            new_board[i + 2][j + 2] = my_coin
            white_king_jump_moves(new_board, i + 2, j + 2, boards, depth, is_king, moves)

    if (is_left == False and is_right == False and moves):
        print("adding to valid moves")
        valid_moves.append(deepcopy(moves))
        boards.append(game_board)
        if (depth == max_depth):
            moves_boards[str(moves)] = game_board
        if (len(moves) > 0):
            moves.pop()
    return

def black_simple_moves(game_board, i, j, boards, depth, is_king):
    make_king = False
    if ((i + 1) == 7):
        make_king = True
    # Is there a valid simple-left-forward-move
    if ((i + 1) >= 0 and (i + 1) <= 7 and (j - 1) >= 0 and (j - 1) <= 7 and (game_board[i + 1][j - 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i + 1) + str(j - 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        if (make_king):
            my_coin = my_coin.upper()
        new_board[i + 1][j - 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)

    # Is there a valid simple-right-forward-move
    if ((i + 1) >= 0 and (i + 1) <= 7 and (j + 1) >= 0 and (j + 1) <= 7 and (game_board[i + 1][j + 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i + 1) + str(j + 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        if (make_king):
            my_coin = my_coin.upper()
        new_board[i + 1][j + 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)
    return

def black_jump_moves(game_board, i, j, boards, depth, is_king, moves = None):
    if moves is None:
        moves = []
    global valid_moves
    global moves_boards
    #print("entering recursion")
    move_type = "J"
    is_left, is_right = False, False
    # Is there a valid jump-left-forward-move
    if ((i + 2) >= 0 and (i + 2) <= 7 and (j - 2) >= 0 and (j - 2) <= 7 and (game_board[i + 2][j - 2] == ".") and (
            game_board[i + 1][j - 1].lower() == "w")):
        if ((i + 2) == 7 and not is_king):
            is_king = True
        #print("left_called")
        my_move = "J " + str(i) + str(j) + " " + str(i + 2) + str(j - 2)
        moves.append(my_move)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i + 1][j - 1] = "."
        if (is_king):
            my_coin = my_coin.upper()
        new_board[i + 2][j - 2] = my_coin
        is_left = True
        black_jump_moves(new_board, i + 2, j - 2, boards, depth, is_king, moves)

    # Is there a valid jump-right-forward-move
    if ((i + 2) >= 0 and (i + 2) <= 7 and (j + 2) >= 0 and (j + 2) <= 7 and (game_board[i + 2][j + 2] == ".") and (
            game_board[i + 1][j + 1].lower() == "w")):
        #print("right_called")
        if ((i + 2) == 7 and not is_king):
            is_king = True
        my_move = "J " + str(i) + str(j) + " " + str(i + 2) + str(j + 2)
        moves.append(my_move)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i + 1][j + 1] = "."
        is_right = True
        if (is_king):
            my_coin = my_coin.upper()
        new_board[i + 2][j + 2] = my_coin
        black_jump_moves(new_board, i + 2, j + 2, boards, depth, is_king, moves)

    if (is_left == False and is_right == False and moves):
        #print("adding to valid moves")
        valid_moves.append(deepcopy(moves))
        boards.append(game_board)
        if (depth == max_depth):
            moves_boards[str(moves)] = game_board
        if (len(moves) > 0):
            moves.pop()
    return

def black_king_simple_moves(game_board, i, j, boards, depth, is_king):
    # Is there a valid simple-left-forward-move
    if ((i + 1) >= 0 and (i + 1) <= 7 and (j - 1) >= 0 and (j - 1) <= 7 and (game_board[i + 1][j - 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i + 1) + str(j - 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i + 1][j - 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)

    # Is there a valid simple-right-forward-move
    if ((i + 1) >= 0 and (i + 1) <= 7 and (j + 1) >= 0 and (j + 1) <= 7 and (game_board[i + 1][j + 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i + 1) + str(j + 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i + 1][j + 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)

    # Is there a valid simple-left-backward-move
    if ((i - 1) >= 0 and (i - 1) <= 7 and (j - 1) >= 0 and (j - 1) <= 7 and (game_board[i - 1][j - 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i - 1) + str(j - 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i - 1][j - 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)

    # Is there a valid simple-right-backward-move
    if ((i - 1) >= 0 and (i - 1) <= 7 and (j + 1) >= 0 and (j + 1) <= 7 and (game_board[i - 1][j + 1] == ".")):
        my_move = "E " + str(i) + str(j) + " " + str(i - 1) + str(j + 1)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i - 1][j + 1] = my_coin
        if (depth == max_depth):
            moves_boards[str(my_move)] = new_board
        valid_moves.append([my_move])
        boards.append(new_board)

    return

def black_king_jump_moves(game_board, i, j, boards, depth, is_king, moves = None):
    if moves is None:
        moves = []
    global valid_moves
    global moves_boards
    #print("entering recursion")
    move_type = "J"
    is_left, is_right = False, False
    # Is there a valid jump-left-forward-move
    if ((i + 2) >= 0 and (i + 2) <= 7 and (j - 2) >= 0 and (j - 2) <= 7 and (game_board[i + 2][j - 2] == ".") and (
            game_board[i + 1][j - 1].lower() == "w")):
        #print("left_called")
        my_move = "J " + str(i) + str(j) + " " + str(i + 2) + str(j - 2)
        moves.append(my_move)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i + 1][j - 1] = "."
        new_board[i + 2][j - 2] = my_coin
        is_left = True
        black_king_jump_moves(new_board, i + 2, j - 2, boards, depth, is_king, moves)

    # Is there a valid jump-right-forward-move
    if ((i + 2) >= 0 and (i + 2) <= 7 and (j + 2) >= 0 and (j + 2) <= 7 and (game_board[i + 2][j + 2] == ".") and (
            game_board[i + 1][j + 1].lower() == "w")):
        #print("right_called")
        my_move = "J " + str(i) + str(j) + " " + str(i + 2) + str(j + 2)
        moves.append(my_move)
        new_board = deepcopy(game_board)
        my_coin = new_board[i][j]
        new_board[i][j] = "."
        new_board[i + 1][j + 1] = "."
        is_right = True
        new_board[i + 2][j + 2] = my_coin
        black_king_jump_moves(new_board, i + 2, j + 2, boards, depth, is_king, moves)
    if (is_king):
        if ((i - 2) >= 0 and (i - 2) <= 7 and (j - 2) >= 0 and (j - 2) <= 7 and (game_board[i - 2][j - 2] == ".") and (
                game_board[i - 1][j - 1].lower() == "w")):
            #print("king left_called")
            my_move = "J " + str(i) + str(j) + " " + str(i - 2) + str(j - 2)
            moves.append(my_move)
            new_board = deepcopy(game_board)
            my_coin = new_board[i][j]
            new_board[i][j] = "."
            new_board[i - 1][j - 1] = "."
            new_board[i - 2][j - 2] = my_coin
            is_left = True
            black_king_jump_moves(new_board, i - 2, j - 2, boards, depth, is_king, moves)

        # Is there a valid jump-right-forward-move
        if ((i - 2) >= 0 and (i - 2) <= 7 and (j + 2) >= 0 and (j + 2) <= 7 and (game_board[i - 2][j + 2] == ".") and (
                game_board[i - 1][j + 1].lower() == "w")):
            #print("right_called")
            my_move = "J " + str(i) + str(j) + " " + str(i - 2) + str(j + 2)
            moves.append(my_move)
            new_board = deepcopy(game_board)
            my_coin = new_board[i][j]
            new_board[i][j] = "."
            new_board[i - 1][j + 1] = "."
            is_right = True
            new_board[i - 2][j + 2] = my_coin
            is_right = True
            black_king_jump_moves(new_board, i - 2, j + 2, boards, depth, is_king, moves)

    if (is_left == False and is_right == False and moves):
        #print("adding to valid moves")
        valid_moves.append(deepcopy(moves))
        boards.append(game_board)
        if (depth == max_depth):
            moves_boards[str(moves)] = game_board
        if (len(moves) > 0):
            moves.pop()
    return

def generate_valid_moves(game_board, pl_color, depth):
    global valid_moves
    valid_moves = []
    boards = []
    for i in range(0, 8):
        for j in range(0, 8):
            if (game_board[i][j].lower() == pl_color):
                if (pl_color == 'w'):
                    if (game_board[i][j] == "w"):
                        is_king = False
                        white_jump_moves(game_board, i, j, boards, depth, is_king)
                    elif (game_board[i][j] == "W"):
                        is_king = True
                        white_king_jump_moves(game_board, i, j, boards, depth, is_king)
                if (pl_color == 'b'):
                    if (game_board[i][j] == "b"):
                        is_king = False
                        black_jump_moves(game_board, i, j, boards, depth, is_king)
                    elif (game_board[i][j] == "B"):
                        is_king = True
                        black_king_jump_moves(game_board, i, j, boards, depth, is_king)
    if (not valid_moves):
        for i in range(0, 8):
            for j in range(0, 8):
                if (game_board[i][j].lower() == pl_color):
                    if (pl_color == 'w'):
                        if (game_board[i][j] == "w"):
                            is_king = False
                            white_simple_moves(game_board, i, j, boards, depth, is_king)
                        elif (game_board[i][j] == "W"):
                            is_king = True
                            white_king_simple_moves(game_board, i, j, boards, depth, is_king)
                    if (pl_color == 'b'):
                        if (game_board[i][j] == "b"):
                            is_king = False
                            black_simple_moves(game_board, i, j, boards, depth, is_king)
                        elif (game_board[i][j] == "B"):
                            is_king = True
                            black_king_simple_moves(game_board, i, j, boards, depth, is_king)
    return boards


def evaluation_function(board):
    #print("called")
    # print(board)
    score = 0.0
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j].lower() == player_color:
                if (board[i][j].islower()):
                    score = score + 3.0
                # print("my pawn")
                elif (board[i][j].isupper()):
                    # print("called")
                    score = score + 15.0
            elif board[i][j].lower() == opp_color:
                if (board[i][j].islower()):
                    score = score - 3.0
                # print("opponent pawn")
                else:
                    score = score - 15.0
                # print("opponent king")
            temp_score = 0
            if board[i][j].lower() == "w" and board[i][j].islower() and i < 4:
                temp_score = 10
            elif board[i][j].lower() == "b" and board[i][j].islower() and i > 4:
                temp_score = 10

            if board[i][j].lower() == player_color:
                score = score + temp_score
            elif board[i][j].lower() == opp_color:
                score = score - temp_score

    return score

def write_game_move(optimal_move):
    optimal_move.replace("'", "")
    final_moves = optimal_move.strip("[]").split(",")
    #print(final_moves)
    with open("output.txt", "a+") as f:
        for i in range(len(final_moves)):
            ref_move = deepcopy(final_moves[i])
            ref_move = ref_move.replace("'", "")
            ref_move = ref_move.strip(" ")
            #print(ref_move)
            temp_move= ""
            for j in range(len(ref_move)):
                if(j == 0):
                    temp_move += ref_move[j]
                elif (j == 2 or j == 5):
                    temp_move += row_encoding[int(ref_move[j])]
                elif (j == 3 or j == 6):
                    temp_move += column_encoding[int(ref_move[j])]
                else:
                    temp_move+=ref_move[j]
            #print(temp_move)
            new_temp_move = ""
            for j in range(len(temp_move)):
                if (j == 2):
                    new_temp_move += temp_move[3]
                elif (j == 3):
                    new_temp_move += temp_move[2]
                elif (j == 5):
                    new_temp_move += temp_move[6]
                elif (j == 6):
                    new_temp_move += temp_move[5]
                else:
                    new_temp_move += temp_move[j]
            #print(new_temp_move)
            #print("\n")
            f.write(new_temp_move+"\n")
    f.close()
    return

def write_game_board(game_board):
    with open("output.txt", "w+") as f:
        board_full = ""
        for i in range(len(game_board)):
            board_row = ""
            for j in range(len(game_board[i])):
                board_row += game_board[i][j]
            board_row+="\n"
            board_full += board_row
        f.write(board_full+"\n")
    f.close()
    return

def minimax(board, depth, max_player, color):
    #print("dwfewfwe")
    if (depth == 0):
        #print("end of one recursion")
        return evaluation_function(board)
    if max_player:
        boards = generate_valid_moves(board, color, depth)
        if (not boards):
            return - 100
        for child_board in boards:
            if(count_pieces(child_board, color) == 0):
                return -100
            if (color == "w"):
                new_color = "b"
            else:
                new_color = "w"
            return minimax(child_board, deepcopy(depth) - 1, False, new_color)
    else:
        boards = generate_valid_moves(board, color, depth)
        #print(len(boards))
        if (not boards):
            return 100
        for child_board in boards:
            if (count_pieces(child_board, color) == 0):
                return float('inf')
            if (color == "w"):
                new_color = "b"
            else:
                new_color = "w"
            return minimax(child_board, deepcopy(depth) - 1, True, new_color)

def find_best_move(game_board, player_color, max_depth):
    generate_valid_moves(game_board, player_color, max_depth)
    #valid_moves.sort(key = len)
    # best_move = valid_moves[-1]
    # best_board = moves_boards[str(best_move)]
    best_move = None
    best_board = None
    max_evaluation_score = float('-inf')
    # print(moves_boards["['J 41 23', 'J 23 05']"])
    for key in moves_boards.keys():
        #print("printing key" + str(key))
        evaluation_score = minimax(moves_boards[key], max_depth - 1, False, opp_color)
        #print(evaluation_score)
        if (evaluation_score > max_evaluation_score):
            best_move = key
            best_board = moves_boards[key]
            max_evaluation_score = evaluation_score

    return best_move, best_board

game_board, game_type, game_time, player_color = parse_input()
player_color = encode_player_color(player_color)
check_my_turn(player_color, game_type)
count_pieces(game_board, player_color)
if (player_color == 'w'):
    opp_color = 'b'
else:
    opp_color = 'w'
if game_type.lower() == 'single':
    max_depth = 1
elif game_type.lower() == 'game':
    max_depth = 10
#print(max_depth)
next_move, next_board = find_best_move(game_board, player_color, max_depth)
write_game_move(next_move)
#write_game_board(next_board)
# print(next_move)
#print(next_board)
    # for key in moves_boards :
    #     print(moves_boards[key])
    #     minimax (moves_boards[key], max_depth-1, True, player_color)
