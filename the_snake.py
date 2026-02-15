from random import choice, randrange

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_CENTER = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Словарь для нажатия кнопок:
KEYDOWN_DICT = {(UP, pg.K_LEFT): LEFT,
                (UP, pg.K_RIGHT): RIGHT,
                (DOWN, pg.K_LEFT): LEFT,
                (DOWN, pg.K_RIGHT): RIGHT,
                (RIGHT, pg.K_UP): UP,
                (RIGHT, pg.K_DOWN): DOWN,
                (LEFT, pg.K_UP): UP,
                (LEFT, pg.K_DOWN): DOWN}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Представление игрового объекта, например змейки и яблока."""

    def __init__(self,
                 body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR,
                 position: tuple[int, int] = GRID_CENTER):
        """Инициализация общих аттрибутов для змеи и яблока."""
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Абстрактный метод-заглушка для дальнейшей
        реализации в дочерних классах.
        """
        raise NotImplementedError(f'Необходимо переопределить метод '
                                  f'draw в классе {self.__class__.__name__}')

    def draw_cell(self, position: tuple[int, int] | None = None,
                  color: tuple[int, int, int] | None = None,
                  draw_borders=True):
        """Закрашивает клетку переданным цветом. Опционально
        рисует рамки для этой клетки.
        """
        position = position or self.position
        color = color or self.body_color

        rect = pg.Rect(convert_grid_size_to_pixels(position),
                       (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if draw_borders:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def convert_grid_size_to_pixels(position: tuple[int, int]) -> tuple[int, int]:
    """Конвертирует координаты из номеров ячеек в пиксели
    для дальнейшей отрисовки.
    """
    return tuple(map(lambda x: x * GRID_SIZE, position))  # type: ignore


class Snake(GameObject):
    """Представление змейки."""

    def __init__(self, position: tuple[int, int] = GRID_CENTER,
                 body_color=SNAKE_COLOR):
        """Инициализация змеи."""
        super().__init__(body_color, position)
        self.reset()
        self.direction = RIGHT

    def update_direction(self, direction: tuple[int, int]):
        """Метод обновления направления после нажатия на кнопку."""
        self.direction = direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и
        удаляя последний элемент, если длина змейки не увеличилась.
        """
        (x_direction, y_direction) = self.direction
        (x_pos, y_pos) = self.get_head_position()
        new_head_position = ((x_direction + x_pos) % GRID_WIDTH,
                             (y_direction + y_pos) % GRID_HEIGHT)
        self.positions.insert(0, new_head_position)

        self.last = self.positions.pop()

    def grow_snake_tail(self):
        """Добавляет хвост змейке."""
        self.positions.append(self.last)
        self.last = None

    def draw(self):
        """Метод для отрисовки головы и тела змейки."""
        # Отрисовка головы змейки.
        self.draw_cell(self.get_head_position())

        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, False)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None


class Apple(GameObject):
    """Представление яблока."""

    def __init__(self, occupied_positions: list[tuple[int, int]] | None = None,
                 body_color=APPLE_COLOR,
                 position: tuple[int, int] = GRID_CENTER):
        """Создание яблока."""
        super().__init__(body_color, position)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions: list[tuple[int, int]]):
        """Удаляет съеденное яблоко и рандомизирует позицию нового."""
        while True:
            self.position = (randrange(0, GRID_WIDTH),
                             randrange(0, GRID_HEIGHT))
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Метод, который отрисовывает яблоко."""
        self.draw_cell()


def handle_keys(game_object):
    """Функция обработки действий пользователя из прекода."""
    for event in pg.event.get():
        if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            game_object.update_direction(
                KEYDOWN_DICT.get((game_object.direction, event.key),
                                 game_object.direction)
            )


def main():
    """Основная игровая логика."""
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

    def check_if_snake_eats_apple():
        """Проверяет, съела ли змея яблоко."""
        if snake.get_head_position() == apple.position:
            snake.grow_snake_tail()
            apple.randomize_position(snake.positions)

    def check_if_snake_eats_tail():
        """Проверяет, съела ли змея свой хвост."""
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        check_if_snake_eats_apple()
        check_if_snake_eats_tail()
        handle_keys(snake)
        snake.move()
        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
