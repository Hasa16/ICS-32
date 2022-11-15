import connectfour as cf
import connectfour_functions as funcLib


def start_game() -> None:
    """
    Starts the Python Shell version of the Connect Four game.
    """
    #Welcomes the user to the Python Shell version of Connect Four and prompts them to define gameboard size.
    print("Welcome to the ICS 32 Python Shell version of Connect Four!")
    columns, rows = funcLib.get_game_size()

    #Creates gameboard with inputted sizes
    gameState = cf.new_game(columns, rows)

    #Takes the turns of the players while checking for a winner.
    while cf.winner(gameState) == cf.EMPTY:
        funcLib.print_game_state(gameState)
        print('')
        funcLib.print_turn(gameState)
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

    # Identifies the winner and prints who won.
    winner = cf.winner(gameState)
    print()
    funcLib.print_game_state(gameState)
    print(funcLib.get_player_string(winner) + ' has won the game! Congrats!')
    return


if __name__ == '__main__':
    start_game()
