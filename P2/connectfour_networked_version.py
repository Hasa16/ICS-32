import connectfour as cf
import connectfour_functions as funcLib
import connectfour_networking as net


def start_game() -> None:
    """
    Starts the networked version of the connect four game on the ICS 32 servers.
    """
    #Welcomes the user and asks for IP/Host, Port, Username, and gameboard size.
    print("Welcome to ICS 32 networked Connect Four!")
    host, port = funcLib.get_iph_and_port()
    username = funcLib.get_username()
    columns, rows = funcLib.get_game_size()

    #Attempts to connect to the game server.
    if not net.connect_to_server(host, port, username, columns, rows):
        print('A connection could not be established with the server')
        return
    print('Successfully connected to the server. \n')
    print('')

    #Creates the Connect Four game board and initializes turns while checking for a winner.
    gameState = cf.new_game(columns, rows)
    funcLib.print_game_state(gameState)
    while cf.winner(gameState) == cf.EMPTY:
        if gameState.turn == cf.RED:
            print('')
            print('You are Red, it''s your move.')
            while True:
                col, move = funcLib.prompt_and_get_move(columns)
                try:
                    gameState = funcLib.execute_move(gameState, col, move)
                    break
                except cf.InvalidMoveError:
                    if move == funcLib.POP_BOTTOM:
                        print('Can not pop on the given column')
                    else:
                        print('Can not drop on the given column')
            response = net.send_moves(move, col)
        elif gameState.turn == cf.YELLOW:
            funcLib.print_game_state(gameState)
            print('')
            move, col = net.receive_moves()
            gameState = funcLib.execute_move(gameState, col, move)
            print('Yellow has made the move: ' + move + ' ' + str(col))
            funcLib.print_game_state(gameState)
            continue

    #Identifies the winner and prints who won.
    winner = cf.winner(gameState)
    print()
    funcLib.print_game_state(gameState)
    print('')
    if winner == cf.RED:
        print('You have won the game, congratulations!')
    else:
        print('The Yellow player, the server, has won the game.')
    net.kill_connection()
    return


if __name__ == '__main__':
    start_game()
