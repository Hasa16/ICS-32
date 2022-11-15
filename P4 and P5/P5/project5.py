import columns as game
import pygame
import random

ROWS = 13
COLS = 6
FPS = 12
JEWELS = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']


class Game:

    def __init__(self):
        self._surface = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
        self._backgroundColor = pygame.Color(0, 0, 0)
        self._boxColor = pygame.Color(220, 220, 220)
        self._state = game.GameState(ROWS, COLS)
        self._tick_counter = FPS
        self._running = True
        self._jewelBufferY = 0.04
        self._jewelSize = (1.0 - self._jewelBufferY) / self._state.rows
        self._jewelBufferX = (1.0 - (self._jewelSize * self._state.columns))

    def start_game(self) -> None:
        """Start the columns game.

        Returns:
            None

        """
        pygame.init()
        try:
            self._surface.fill(self._backgroundColor)
            clock = pygame.time.Clock()
            while self._running:
                clock.tick(FPS)
                self._handle_events()
                self._tick_counter -= 1
                if self._tick_counter == 0:
                    self._tick_game()
                    self._tick_counter = FPS
                self._draw_game_objects()
                pygame.display.flip()
        finally:
            pygame.quit()

    def _tick_game(self) -> None:
        """Ticks the game.

        Returns:
            None

        """
        self._running = not self._state.tick()
        if not self._state.faller.active:
            contents = random.sample(JEWELS, 3)
            column = random.randint(1, COLS)
            self._state.spawn_faller(column, contents)

    def _draw_game_objects(self) -> None:
        """Draws game objects.

        Returns:
            None

        """
        top_left_x = int((self._jewelBufferX / 2) * self._surface.get_width())
        top_left_y = int((self._jewelBufferY / 2) * self._surface.get_height())
        width = int(((self._jewelSize * self._state.columns) - 0.001) * self._surface.get_width())
        height = int((self._jewelSize * self._state.rows) * self._surface.get_height())
        outline_rect = pygame.Rect(top_left_x, top_left_y, width, height)
        pygame.draw.rect(self._surface, self._boxColor, outline_rect, 0)
        for row in range(self._state.rows):
            for col in range(self._state.columns):
                self._draw_jewel(row, col)

    def _draw_jewel(self, row: int, col: int) -> None:
        """Draws jewels in game on given row and column.

        Args:
            row: int value of row to be drawn on
            col: int value of column to be drawn on

        Returns:
            None

        """
        jewel = self._state.board_rows[row][col]
        if jewel is game.EMPTY:
            return
        state = self._state.board_states[row][col]
        if state == game.MATCHED:
            raw_color = (255, 255, 255)
        else:
            raw_color = _get_jewel_color(jewel)
        color = pygame.Color(raw_color[0], raw_color[1], raw_color[2])
        jewel_x = (col * self._jewelSize) + (self._jewelBufferX / 2)
        jewel_y = (row * self._jewelSize) + (self._jewelBufferY / 2)
        top_left_x = int(jewel_x * self._surface.get_width())
        top_left_y = int(jewel_y * self._surface.get_height())
        width = int(self._jewelSize * self._surface.get_width())
        height = int(self._jewelSize * self._surface.get_height())
        rect = pygame.Rect(top_left_x, top_left_y, width, height)
        pygame.draw.rect(self._surface, color, rect, 0)
        if state == game.CELL_FALLER_STOPPED:
            pygame.draw.rect(self._surface, pygame.Color(255, 255, 255), rect, 2)

    def _handle_events(self) -> None:
        """Handles given events.

        Returns:
            None

        """
        for event in pygame.event.get():
            self._handle_event(event)
        self._handle_input()

    def _handle_event(self, event: pygame.event.EventType) -> None:
        """Checks given event for quit or resize.

        Args:
            event: pygame event-type

        Returns:
            None

        """
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.VIDEORESIZE:
            self._surface = pygame.display.set_mode(event.size, pygame.RESIZABLE)

    def _handle_input(self) -> None:
        """Handles user input.

        Returns:
            None

        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self._state.move_faller(game.LEFT)
        if keys[pygame.K_RIGHT]:
            self._state.move_faller(game.RIGHT)
        if keys[pygame.K_SPACE]:
            self._state.rotate_faller()


def _get_jewel_color(jewel: str) -> (int, int, int):
    """Gets the jewel color based on character.

    Args:
        jewel: str of character for jewel

    Returns:
        (int, int, int): RGB color code

    """
    if jewel == 'S':  # Red
        return 255, 0, 0
    elif jewel == 'T':  # Green
        return 0, 255, 0
    elif jewel == 'V':  # Blue
        return 0, 0, 255
    elif jewel == 'X':  # Orange
        return 255, 128, 0
    elif jewel == 'Y':  # Purple
        return 102, 0, 204
    elif jewel == 'W':  # Yellow
        return 255, 255, 0
    elif jewel == 'Z':  # Pink
        return 255, 105, 180


if __name__ == '__main__':
    Game().start_game()
