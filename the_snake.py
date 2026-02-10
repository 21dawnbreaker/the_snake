from random import choice, randrange

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


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, body_color: tuple[int, int, int]):
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

    def move(self, snake_len: int, new_position: tuple[int, int]):
        """обновляет позицию змейки (координаты каждой секции), добавляя новую голову в начало списка positions и
        удаляя последний элемент, если длина змейки не увеличилась.
        """
        if self.length == snake_len:
            tail = self.positions.pop()
            self.positions = [tail] + self.positions[:len(self.positions) - 1]

    def draw(self):
        """Метод draw класса Snake для отрисовки головы и тела."""
        # Отрисовка головы змейки.
        head_rect = pygame.Rect(convert_grid_size_to_pixels(self.positions[0]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Отрисовка тела змейки.
        for position in self.positions[:-1]:
            rect = (pygame.Rect(tuple(map(lambda x: x * GRID_SIZE, position)), (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


class Apple(GameObject):
    def __init__(self):
        """Инициализация яблока."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Рандомизирует позицию яблока."""
        if self.position is not None:
            last_rect = pygame.Rect(convert_grid_size_to_pixels(self.position), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.position = (randrange(0, GRID_WIDTH), randrange(0, GRID_HEIGHT))

    def draw(self):
        """Метод draw класса Apple."""
        rect = pygame.Rect(convert_grid_size_to_pixels(self.position), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
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
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()







#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
