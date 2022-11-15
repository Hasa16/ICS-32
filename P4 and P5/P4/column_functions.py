import columns as game


def check_text(rows: int, cols: int, text: str, state: game.GameState) -> None:
    """Checks the text to see if there is any other input
    Args:
        rows: Number of rows
        cols: Number of Columns
        text: str of text
        state: GameState from Columns

    Returns:
        None
    """
    if text == 'CONTENTS':
        row_list = []
        for i in range(rows):
            row = []
            text = raw_next_line()
            for index in range(cols):
                row.append(text[index])
            row_list.append(row)
        state.set_board(row_list)


def display_board(state: game.GameState) -> None:
    """
    Displays the board of the GameState
    Args:
        state: The GameState that will be displayed in the console

    Returns:
        None
    """
    for row in range(state.rows):
        row_string = "|"
        for col in range(state.columns):
            cell_value = state.board_rows[row][col]
            cell_state = state.board_states[row][col]
            if cell_state == game.EMPTY_CELL:
                row_string += '   '
            elif cell_state == game.OCCUPIED:
                row_string += (' ' + cell_value + ' ')
            elif cell_state == game.CELL_FALLER_MOVING:
                row_string += ('[' + cell_value + ']')
            elif cell_state == game.CELL_FALLER_STOPPED:
                row_string += ('|' + cell_value + '|')
            elif cell_state == game.MATCHED:
                row_string += ('*' + cell_value + '*')
        row_string += '|'
        print(row_string)
    final_line = ' '
    for col in range(state.columns):
        final_line += '---'
    final_line += ' '
    print(final_line)


def get_int() -> int:
    """
    Gets a lone integer from the console

    Returns:
        int: The int value that was read in from the console
    """
    line = input().strip()
    return int(line)


def next_line() -> str:
    """
    Gets a line from the console and returns it stripped

    Returns:
        str:The line that was retrieved from the console
    """
    return input().strip()


def raw_next_line() -> str:
    """
    Gets a completely raw line from the console

    Returns:
        str: The line that was retrieved from the console
    """
    return input()


def process_input(input: str, state: game.GameState) -> None:
    """
    Processes an input and then executes the action on the given GameState
    Args:
        input: The action that will be executed
        state: The GameState that the given input will be executed on

    Returns:
        None
    """
    if input == 'R':
        state.rotate_faller()
    elif input == '<':
        state.move_faller(game.LEFT)
    elif input == '>':
        state.move_faller(game.RIGHT)
    elif input[0] == 'F':
        try:
            args = input.split(' ')
            column_number = int(args[1])
            faller = [args[4], args[3], args[2]]
            state.spawn_faller(column_number, faller)
        except:
            return
