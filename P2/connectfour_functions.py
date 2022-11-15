import connectfour as cf
import random

DROP_TOP = 'DROP'
POP_BOTTOM = 'POP'

def get_iph_and_port() -> (str, int):
    """
    Prompts the user to enter an IP or Host address

    Return:
    A tuple whose first value (str) is the IP / Host address and second value (int) is the host port

    """

    #Asks for IP / Host import from user.
    print("Please enter an IP address or host to connect to")
    host = input().strip()
    print("Please enter a port to connect to on the given host")
    port = int(input())
    return host, port


def get_username() -> str:
    """
    Prompts the user to enter a username and then returns it

    Return: The username (str) entered by the user

    """

    while True:
        print("Please enter your username (without spaces)")
        username = input().strip()
        if ' ' not in username:
            return username


def get_player_string(player: int) -> str:
    """
    Returns a string representation of the given player number

    Parameter:
    player: An integer value representing a player

    Return:
    A string that represents the given player

    """

    if player == cf.YELLOW:
        return 'Yellow'
    elif player == cf.RED:
        return 'Red'
    else:
        return 'EMPTY'


def get_player_symbol(player: int) -> str:
    """
    Returns a single character representation of the given player number

    Param
    player (int): An integer value representing a player

    Return:
    A single character (str) that represents the given player

    """

    if player == cf.YELLOW:
        return 'Y'
    elif player == cf.RED:
        return 'R'
    else:
        return '.'


def execute_move(state: cf.GameState, col: int, move: str) -> cf.GameState:
    """
    Executes the given move upon the given column for the given GameState

    Parameter:
    state: The GameState that this move will be executed on
    col (int): The column that this move will act upon
    move (str): The move that will be executed

    Return:
    A new GameState with the results of the executed move

    """

    if move == DROP_TOP:
        return cf.drop(state, col - 1)
    elif move == POP_BOTTOM:
        return cf.pop(state, col - 1)
    else:
        raise cf.InvalidMoveError()


def print_game_state(state: cf.GameState) -> None:
    """
    Prints the contents of the given GameState to the console

    Parameter
    state: The GameState that will be printed to the console

    """

    x = 0
    for x in range(cf.columns(state)):
        if x != max(range(cf.columns(state))):
            if x != 8:
                x += 1
                text = "{:<3}"
                print(text.format(x), end='')
            elif x == 9:
                x += 1
                text = "{:<2}"
                print(text.format(x), end='')
            else:
                x += 1
                text = "{:<2}"
                print(text.format(x), end='')
        else:
            x += 1
            text = "{:<3}"
            print(text.format(x))
    for rowIdx in range(cf.rows(state)):
        for colIdx in range(cf.columns(state)):
            if colIdx == 0:
                print(get_player_symbol(state.board[colIdx][rowIdx]), end=' ')
            else:
                print(' ' + get_player_symbol(state.board[colIdx][rowIdx]), end=' ')
        print('')


def print_turn(state: cf.GameState) -> None:
    """
    Prints a message to the console that informs the players whose turn it is

    Parameter
    state: The GameState that will be used to determine which player has the current turn

    """

    print('It is the ' + get_player_string(state.turn) + ' players turn')


def prompt_and_get_move(columns) -> (int, str):
    """
    Prompts the current player to enter a valid column number and a valid move type

    Return: A tuple whose first value is the entered column number and second value is the move type

    """

    while True:
        print('Please input a move (drop or pop) and a number from 1 to {num}. Example: drop {random}'.format(num = columns, random = random.randint(0, columns)))
        line = input().strip()

        move = line[0:4].strip()
        colString = line[4:].strip()

        if not colString.isdigit():
            continue

        colNumber = int(colString)
        if colNumber < 1 or colNumber > columns:
            continue

        move = move.lower()
        if move == 'drop':
            return colNumber, DROP_TOP

        if move == 'pop':
            return colNumber, POP_BOTTOM


def get_game_size() -> (int, int):
    """
    Prompts the user to enter the length and height of the game board. Will accept any values above 3 and below 21.

    Returns:
    Column size and Row size

    """

    while True:
        try:
            print("Insert a column size above 3 and below 21")
            columns = int(input().strip())
            if columns > 3 and columns < 21:
                print("Columns entered successfully.")
                break
            else:
                print("Columns should be above 3 and below 21")
        except ValueError:
            print("Please provide a valid integer value")
            continue

    while True:
        try:
            print("Insert a row size above 3 and below 21")
            rows = int(input().strip())
            if rows > 3 and rows < 21:
                print("Rows entered successfully.")
                break
            else:
                print("Rows should be above 3 and below 21")
        except ValueError:
            print("Please provide a valid integer value")
            continue
    return columns, rows