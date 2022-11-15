# Possible contents of the cells
_NONE = 'NONE'
EMPTY = ' '
S, T, V, W, X, Y, Z = 'S', 'T', 'V', 'W', 'X', 'Y', 'z'

# State of a cell
EMPTY_CELL = 'EMPTY STATE'
OCCUPIED = 'OCCUPIED STATE'
MATCHED = 'MATCHED STATE'
CELL_FALLER_MOVING = 'FALLER_MOVING STATE'
CELL_FALLER_STOPPED = 'FALLER_STOPPED STATE'
_FALLER_STOPPED = 0
_FALLER_MOVING = 1

# Set Directions
LEFT = -1
RIGHT = 1
_DOWN = 0
_DOWN_LEFT = 2


class Faller:
    def __init__(self):
        """
        Constructs a new faller object and initializes all the values
        """
        self.active = False
        self.contents = [EMPTY, EMPTY, EMPTY]
        self.state = _FALLER_MOVING
        self._row = 0
        self._col = 0

    def get_rows(self) -> int:
        """
        Gets the row value for this faller

        Returns:
            int: Represents the row value
        """
        return self._row

    def get_column(self) -> int:
        """
        Gets the column value for this faller

        Returns:
            int: Represents the column value
        """
        return self._col

    def set_row(self, row: int) -> None:
        """
        Sets the row value for this faller
        Args:
            row: The row value that this faller will be set to

        Returns:
            None
        """
        self._row = row

    def set_col(self, col: int) -> None:
        """
        Sets the column value for this faller
        Args:
            col: The column value that this faller will be set to

        Returns:
            None
        """
        self._col = col


class GameState:
    def __init__(self, rows: int, columns: int):
        """
        Constructs a new GameState with a board containing x rows and y columns
        Args:
            rows: The number of rows that board will have
            columns: The number of columns that the board will have
        """
        self.rows = rows
        self.columns = columns
        self.board_rows = []
        self.board_states = []
        self.faller = Faller()
        for i in range(rows):
            row = []
            state_row = []
            for j in range(columns):
                row.append(EMPTY)
                state_row.append(EMPTY_CELL)
            self.board_rows.append(row)
            self.board_states.append(state_row)

    def tick(self) -> bool:
        """
        Ticks one time unit on the game. This causes fallers to move down and/or matching to occur

        Returns:
             True: if the game is over from a faller freezing out of bounds
             False: otherwise
        """
        if self.faller.active:
            if self.faller.state == _FALLER_STOPPED:
                self._update_faller_state()
                if self.faller.state == _FALLER_STOPPED:
                    value = False
                    if self.faller.get_rows() - 2 < 0:
                        value = True
                    for i in range(3):
                        self.board_rows[self.faller.get_rows() - i][self.faller.get_column()] \
                            = self.faller.contents[i]
                        self.board_states[self.faller.get_rows() - i][self.faller.get_column()] = OCCUPIED
                    self.faller.active = False
                    self._attempt_matching()
                    return value
            self.move_faller_down()
            self._update_faller_state()
        self._attempt_matching()
        return False

    def set_board(self, contents: [[str]]) -> None:
        """
        Sets the contents of the game board to the given contents, then applies the gravity and attempts matching
        Args:
            contents: A list of rows from the top of the board to the bottom

        Returns:
            None
        """
        for row in range(self.rows):
            for col in range(self.columns):
                value = contents[row][col]
                if value is EMPTY:
                    self.board_rows[row][col] = EMPTY
                    self.board_states[row][col] = EMPTY_CELL
                else:
                    self.board_rows[row][col] = value
                    self.board_states[row][col] = OCCUPIED
        self._jewel_gravity()
        self._attempt_matching()

    def spawn_faller(self, column: int, faller: [str, str, str]) -> None:
        """
        Spawns a faller in the given column with its given contents
        Args:
            column: A column number
            faller: The contents of the faller that will spawn.

        Returns:
            None
        """
        if self.faller.active:
            return

        self.faller.active = True
        self.faller.contents = faller
        self.faller.set_row(0)
        self.faller.set_col(column - 1)
        self.board_rows[0][self.faller.get_column()] = self.faller.contents[0]
        self.board_states[0][self.faller.get_column()] = CELL_FALLER_MOVING
        self._update_faller_state()

    def move_faller(self, direction: int) -> None:
        """
        Moves the faller in the given direction if possible
        Args:
            direction: The direction (RIGHT or LEFT) to move the faller in

        Returns:
            None
        """
        if not self.faller.active:
            return
        if not direction == RIGHT and not direction == LEFT:
            return
        if (direction == LEFT and self.faller.get_column() == 0) or (
                direction == RIGHT and self.faller.get_column() == self.columns - 1):
            return
        target_column = self.faller.get_column() + direction
        for i in range(3):
            if self.faller.get_rows() - i < 0:
                break
            if self.board_states[self.faller.get_rows() - i][target_column] == OCCUPIED:
                return
        for i in range(3):
            if self.faller.get_rows() - i < 0:
                break
            self.move_cell(self.faller.get_rows() - i, self.faller.get_column(), direction)
        self.faller.set_col(target_column)
        self._update_faller_state()

    def rotate_faller(self) -> None:
        """
        Rotates the faller so the first block becomes the last
        The middle becomes the first
        The top becomes the middle

        Returns:
            None
        """
        if not self.faller.active:
            return
        one = self.faller.contents[0]
        two = self.faller.contents[1]
        three = self.faller.contents[2]
        self.faller.contents = [two, three, one]
        for i in range(3):
            self.board_rows[self.faller.get_rows() - i][self.faller.get_column()] = self.faller.contents[i]
        self._update_faller_state()

    def move_cell(self, row: int, col: int, direction: int) -> None:
        """
        Moves the given cell in the given direction
        Args:
            row: The row number of the cell to move
            col: The column number of the cell to move
            direction: The direction to move the cell in (LEFT, RIGHT, DOWN)

        Returns:
            None
        """
        old_value = self.board_rows[row][col]
        old_state = self.board_states[row][col]

        self.board_rows[row][col] = EMPTY
        self.board_states[row][col] = EMPTY_CELL

        if direction == _DOWN:
            target_row = row + 1
            self.board_rows[target_row][col] = old_value
            self.board_states[target_row][col] = old_state
        else:
            target_col = col + direction
            self.board_rows[row][target_col] = old_value
            self.board_states[row][target_col] = old_state

    def move_faller_down(self) -> None:
        """
        Moves the faller down one space and updates the information

        Returns:
            None
        """
        if self._check_solid(self.faller.get_rows() + 1, self.faller.get_column()):
            return
        self.move_cell(self.faller.get_rows(), self.faller.get_column(), _DOWN)
        if self.faller.get_rows() - 1 >= 0:
            self.move_cell(self.faller.get_rows() - 1, self.faller.get_column(), _DOWN)
            if self.faller.get_rows() - 2 >= 0:
                self.move_cell(self.faller.get_rows() - 2, self.faller.get_column(), _DOWN)
            else:
                self.board_rows[self.faller.get_rows() - 1][self.faller.get_column()] = self.faller.contents[2]
                self.board_states[self.faller.get_rows() - 1][self.faller.get_column()] = CELL_FALLER_MOVING
        else:
            self.board_rows[self.faller.get_rows()][self.faller.get_column()] = self.faller.contents[1]
            self.board_states[self.faller.get_rows()][self.faller.get_column()] = CELL_FALLER_MOVING
        self.faller.set_row(self.faller.get_rows() + 1)

    def _jewel_gravity(self) -> None:
        """
        Applies jewel gravity to all frozen cells until the jewel is solid

        Returns:
            None
        """
        for col in range(self.columns):
            for row in range(self.rows - 1, -1, -1):
                state = self.board_states[row][col]

                if state == CELL_FALLER_MOVING or state == CELL_FALLER_STOPPED:
                    continue
                if state == OCCUPIED:
                    i = 1
                    while not self._check_solid(row + i, col):
                        self.move_cell(row + i - 1, col, _DOWN)
                        i += 1

    def _attempt_matching(self) -> None:
        """
        Ticks the matching state on all cell.
        All cells are compared for matching on the X, Y, and diagonal axes.

        Returns:
            None
        """
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board_states[row][col] == MATCHED:
                    self.board_rows[row][col] = EMPTY
                    self.board_states[row][col] = EMPTY_CELL

        self._jewel_gravity()
        self._match_x_axis()
        self._match_y_axis()
        self._match_diagonals()

    def _match_x_axis(self) -> None:
        """
        Attempts matching for all cells on the X-axis

        Returns:
            None
        """
        for current_row in range(self.rows - 1, -1, -1):
            matches = 0
            jewel = _NONE
            for col in range(0, self.columns):
                contents = self.board_rows[current_row][col]
                state = self.board_states[current_row][col]
                cell_matches = (contents == jewel and self._is_matchable(state))
                if cell_matches:
                    matches += 1
                if col == self.columns - 1:
                    if matches >= 3:
                        if cell_matches:
                            self.mark_matches(current_row, col, LEFT, matches)
                        else:
                            self.mark_matches(current_row, col - 1, LEFT, matches)
                elif not cell_matches:
                    if matches >= 3:
                        self.mark_matches(current_row, col - 1, LEFT, matches)
                    if self._is_matchable(state):
                        jewel = contents
                        matches = 1
                    else:
                        jewel = _NONE
                        matches = 1

    def _match_y_axis(self) -> None:
        """
        Attempts matching for all cells on the Y-axis

        Returns:
            None
        """
        for current_col in range(0, self.columns):
            matches = 0
            jewel = _NONE
            for row in range(self.rows - 1, -1, -1):
                contents = self.board_rows[row][current_col]
                state = self.board_states[row][current_col]
                cell_matches = (contents == jewel and self._is_matchable(state))
                if cell_matches:
                    matches += 1
                if row == 0:
                    if matches >= 3:
                        if cell_matches:
                            self.mark_matches(row, current_col, _DOWN, matches)
                        else:
                            self.mark_matches(row + 1, current_col, _DOWN, matches)
                elif not cell_matches:
                    if matches >= 3:
                        self.mark_matches(row + 1, current_col, _DOWN, matches)
                    if self._is_matchable(state):
                        jewel = contents
                        matches = 1
                    else:
                        jewel = _NONE
                        matches = 1

    def _match_diagonals(self) -> None:
        """
        Attempts matching for all cells on the diagonal-axis

        Returns:
            None
        """
        for current_row in range(self.rows - 1, -1, -1):
            for current_col in range(0, self.columns):
                matches = 0
                jewel = _NONE
                row_counter = 0
                col_counter = 0
                while True:
                    row = current_row - row_counter
                    col = current_col + col_counter

                    contents = self.board_rows[row][col]
                    state = self.board_states[row][col]
                    cell_matches = (contents == jewel and self._is_matchable(state))
                    if cell_matches:
                        matches += 1
                    if col == self.columns - 1 or row == 0:
                        if matches >= 3:
                            if cell_matches:
                                self.mark_matches(row, col, _DOWN_LEFT, matches)
                            else:
                                self.mark_matches(row + 1, col - 1, _DOWN_LEFT, matches)
                    elif not cell_matches:
                        if matches >= 3:
                            self.mark_matches(row + 1, col - 1, _DOWN_LEFT, matches)

                        if self._is_matchable(state):
                            jewel = contents
                            matches = 1
                        else:
                            jewel = _NONE
                            matches = 1

                    row_counter += 1
                    col_counter += 1

                    if current_row - row_counter < 0 or current_col + col_counter >= self.columns:
                        break

    def mark_matches(self, row: int, col: int, direction: int, amount: int) -> None:
        """
        Marks the given number of cells in the given direction as matching cells
        Args:
            row: The row number of the starting cell
            col: The column number of the starting cell
            direction: The direction to mark cells in
            amount: The amount of cells to mark as matching

        Returns:
            None
        """
        if direction == LEFT:
            for target_col in range(col, col - amount, -1):
                self.board_states[row][target_col] = MATCHED
        elif direction == _DOWN:
            for target_row in range(row, row + amount):
                self.board_states[target_row][col] = MATCHED
        elif direction == _DOWN_LEFT:
            for i in range(amount):
                self.board_states[row + i][col - i] = MATCHED

    def _check_solid(self, row: int, col: int) -> bool:
        """
        Checks if the cell of the given row and column is solid
        Args:
            row: The row of the cell to check
            col: The column of the cell the check

        Returns:
            bool:True if the given cell is solid, otherwise False
        """
        if row >= self.rows:
            return True
        if self.board_states[row][col] == OCCUPIED:
            return True

        return False

    def _update_faller_state(self) -> None:
        """
        Updates the state of the faller according to its current conditions.

        Returns:
            None
        """
        target_row = self.faller.get_rows() + 1
        if self._check_solid(target_row, self.faller.get_column()):
            state = CELL_FALLER_STOPPED
            self.faller.state = _FALLER_STOPPED
        else:
            state = CELL_FALLER_MOVING
            self.faller.state = _FALLER_MOVING

        for i in range(3):
            row = self.faller.get_rows() - i
            if row < 0:
                return
            self.board_rows[row][self.faller.get_column()] = self.faller.contents[i]
            self.board_states[row][self.faller.get_column()] = state

    def _is_matchable(self, state: str) -> bool:
        """
        Tells if the given state can be matched
        Args:
            state: The state that will be checked

        Returns:
            True if that given state can be matched. False otherwise
        """
        return state == OCCUPIED or state == MATCHED
