from random import randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Объявление snake для использования в классе Apple:
snake = None

# Тут опишите все классы игры.
class GameObject:
    def __init__(self, body_color: tuple[int, int, int]=BOARD_BACKGROUND_COLOR):
        """Инициализация общих аттрибутов для змеи и яблока."""
        self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод-заглушка для дальнейшей реализации
        в дочерних классах.
        """
        pass

def convert_grid_size_to_pixels(position: tuple[int, int]) -> tuple[int, int]:
    """Конвертирует координаты из номеров ячеек в пиксели для дальнейшей отрисовки"""
    return tuple(map(lambda x: x * GRID_SIZE, position))  # type: ignore

def draw_cell(position, color, draw_borders=True):
    """Закрашивает клетку переданным цветом. Опционально рисует рамки для этой клетки."""
    rect = pygame.Rect(convert_grid_size_to_pixels(position), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, color, rect)
    if draw_borders:
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self, length=1, direction=RIGHT, next_direction=None, body_color=SNAKE_COLOR):
        """Инициализация змеи."""
        super().__init__(body_color)
        self.positions = [self.position]
        self.length = length
        self.direction = direction
        self.next_direction = next_direction

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def __check_if_snake_eats_apple(self, apple, snake_tail):
        """Проверяет, съела ли змея яблоко."""
        if self.positions[0] != apple.position:
            draw_cell(snake_tail, BOARD_BACKGROUND_COLOR, False)
        else:
            self.positions.append(snake_tail)
            apple.randomize_position()

    def move(self, apple):
        """Обновляет позицию змейки (координаты каждой секции), добавляя новую голову в начало списка positions и
        удаляя последний элемент, если длина змейки не увеличилась.
        """
        new_head_position = ((self.direction[0] + self.positions[0][0]), (self.direction[1] + self.positions[0][1]))
        snake_tail = self.positions[-1]
        self.positions = [new_head_position] + self.positions[:-1]

        if self.next_direction is not None:
            self.direction = self.next_direction

        self.__check_if_snake_eats_apple(apple, snake_tail)

        #  Проверяет, съела ли змея свой хвост.
        if self.positions[0] in self.positions[1:]:
            self.reset()

        #  Проверяет, не вышла ли змея за границы игрового экрана.
        for i in range(len(self.positions)):
            position = self.positions[i]
            self.positions[i] = ((position[0] + GRID_WIDTH) % GRID_WIDTH, (position[1] + GRID_HEIGHT) % GRID_HEIGHT)


    def draw(self):
        """Метод для отрисовки головы и тела змейки."""

        # Отрисовка головы змейки.
        draw_cell(self.positions[0], self.body_color)

        # Отрисовка тела змейки по сегментам ее тела.
        for position in self.positions[:-1]:
            draw_cell(position, self.body_color)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        for element in self.positions:
            draw_cell(element, BOARD_BACKGROUND_COLOR, False)
        self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


class Apple(GameObject):
    def __init__(self):
        """Создание яблока."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Удаляет съеденное яблоко и рандомизирует позицию нового."""
        if self.position is not None:
            draw_cell(self.position, APPLE_COLOR, False)
        while True:
            self.position = (randrange(0, GRID_WIDTH), randrange(0, GRID_HEIGHT))
            if self.position not in snake.positions:
                break

    def draw(self):
        """Метод, который отрисовывает яблоко."""
        draw_cell(self.position, APPLE_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя из прекода."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    pygame.init()

    global snake
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move(apple)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
