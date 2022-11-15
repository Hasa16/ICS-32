import column_functions as run
import columns as game


def run_game() -> None:
    """
    Starts the game.

    Returns:
        None
    """
    rows = run.get_int()
    cols = run.get_int()
    state = game.GameState(rows, cols)

    text = run.next_line()
    run.check_text(rows, cols, text, state)

    while True:
        run.display_board(state)
        text = run.next_line()
        if text == 'Q':
            return
        if text == '':
            if state.tick():
                run.display_board(state)
                break
        else:
            run.process_input(text, state)
    print('GAME OVER')


if __name__ == '__main__':
    run_game()
