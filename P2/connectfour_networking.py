import socket as socket
import connectfour_functions as funcLib

drop = 'DROP'
pop = 'POP'

client_end_sequence = '\r\n'
server_end_sequence = '\n'
WINNER_RED = 'WINNER_RED' + server_end_sequence
WINNER_YELLOW = 'WINNER_YELLOW' + server_end_sequence


def connect_to_server(address: str, port: int, username: str, columns: int, rows: int) -> bool:
    """Attempts to connect to the given IP or Host address and port.

    Paramaters:
    address (str): The IP or Host address of the server that will be attempted to be connected to
    port (int): The port of the IP or Host address
    username (str): The username used when attempting to connect to the server
    columns (int): The length of the game board created when connected to game server
    rows (int): The height of the game board created when connected to game server

    Returns:
    The status of connection to the server, True / false

    """

    global connection
    global sock_in
    global sock_out

    #Create socket and connect to given server.
    connection = socket.socket()
    connection.connect((address, port))

    #Create read and write sockets for said server.
    sock_in = connection.makefile('r')
    sock_out = connection.makefile('w')

    #Attempts hello message to server.
    _write_server('I32CFSP_HELLO ' + username + client_end_sequence)

    #Reads response of server.
    response = sock_in.readline()
    if response[0:7] != 'WELCOME' or response[8:] != (username + server_end_sequence):
        return False
    print(response)

    #Responds to server to initiate gameboard.
    _write_server('AI_GAME ' + str(columns) + ' ' + str(rows) + client_end_sequence)
    response = sock_in.readline()
    print(response)

    #Checks to see if server has created gameboard and is ready to play.
    if response != ('READY' + server_end_sequence):
        return False

    return True
    return connection, sock_in, sock_out


def send_moves(move: str, col: int) -> None:
    """
    Sends the given move and the column acted upon to the server.

    Parameters:
    move (str): The action imposed on the gameboard
    col (int): The column number that the action was imposed on

    """

    #Attempts to communicate the player's move to the server.
    try:
        if move == funcLib.DROP_TOP:
            _write_server(drop + ' ' + str(col) + client_end_sequence)
        elif move == funcLib.POP_BOTTOM:
            _write_server(pop + ' ' + str(col) + client_end_sequence)
        global sock_in
    except:
        kill_connection()


def receive_moves() -> (str, int):
    """
    Receives actions from the server

    Returns:
    The action (str) and column acted upon (int) by the server

    """

    #Attempts to read the actions of the server.
    global sock_in
    response = sock_in.readline()
    response = sock_in.readline()
    move = None
    col = None
    if response[0:4] == 'DROP':
        move = funcLib.DROP_TOP
        value = response[5:].strip()
        col = int(value)
    elif response[0:3] == 'POP':
        move = funcLib.POP_BOTTOM
        value = response[4:].strip()
        col = int(value)
    #Checks to see if someone had won
    response = sock_in.readline()
    if response == WINNER_RED or response == WINNER_YELLOW:
        kill_connection()

    return move, col



def _write_server(text: str) -> None:
    """
    Writes the given text to the server

    Parameters:
    text (str): The text that will be written to the server

    """

    global sock_out
    sock_out.write(text)
    sock_out.flush()


def kill_connection() -> None:
    """Closes all networks and streams."""

    sock_out.close()
    sock_in.close()
    connection.close()
