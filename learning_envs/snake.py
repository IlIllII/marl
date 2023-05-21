import gymnasium as gym
from gymnasium.utils import EzPickle
import numpy as np
import pygame

class Snake(gym.Env, EzPickle):

    metadata = {
        'render.modes': ['human'],
        "render_fps": 50,
    }

    def __init__(self):
        # These are required
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(32, 32, 3), dtype=np.uint8)
        self.action_space = gym.spaces.Discrete(5)

        self.screen: pygame.Surface = None
        self.clock = None
        self.grid = None
        self.snake = None
        self.food = None
        self.score = 0


    def step(self, action):
        pass

    def reset(self, *, seed=None):
        super().reset(seed=seed)
        self.reset_game()

    def render(self, mode='human'):
        pass

    def close(self):
        pass

class SnakeGrid:
    def __init__(self, width, height):
        # Snake is 1, food is 2, empty is 0
        self.grid = np.zeros((width, height), dtype=np.uint8)
        self.width = width
        self.height = height

    def __getitem__(self, item):
        return self.grid[item]

    def __setitem__(self, key, value):
        self.grid[key] = value

    def cell_to_str(self, cell):
        if cell == 0:
            return " "
        elif cell == 1:
            return "O"
        elif cell == 2:
            return "X"
        else:
            return "?"

    def __str__(self):
        s = " " + "-" * (self.width * 2 + 1) + "\n"
        for row in self.grid:
            s += "| "
            for cell in row:
                s += self.cell_to_str(cell) + " "
            s += "|\n"
        s += " " + "-" * (self.width * 2 + 1)
        return s

    def __repr__(self):
        return str(self.grid)
        
    def __iter__(self):
        return iter(self.grid)
    
    def clear_snake(self):
        self.grid[self.grid == 1] = 0

    def clear_food(self):
        self.grid[self.grid == 2] = 0

    def clear(self):
        self.clear_snake()
        self.clear_food()

    def place_snake(self, snake):
        for x, y in snake:
            self.grid[x, y] = 1

    def place_food(self, x, y):
        self.grid[x, y] = 2

    def place(self, snake, food):
        self.clear()
        self.place_snake(snake)
        self.place_food(*food)
    
    def is_empty(self, x, y):
        return self.grid[x, y] == 0
    
    def is_snake(self, x, y):
        return self.grid[x, y] == 1
    
    def is_food(self, x, y):
        return self.grid[x, y] == 2
    
    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    

    

class SnakeObject:
    def __init__(self, x, y):
        self.body = [(x, y)]
        self.direction = (0, 0)

    def __len__(self):
        return len(self.body)
    
    def __iter__(self):
        return iter(self.body)
    
    def head(self):
        return self.body[0]
    
    def tail(self):
        return self.body[-1]
    
    def move(self, x, y):
        self.body.insert(0, (x, y))
        self.body.pop()
    
    def grow(self, x, y):
        self.body.insert(0, (x, y))
    
    def is_colliding(self, x, y):
        return (x, y) in self.body
    
    def is_colliding_with_self(self):
        return self.is_colliding(*self.head())

    def default_direction(self):
        x1, y1 = self.body[1]
        x2, y2 = self.body[0]
        return x2 - x1, y2 - y1

class GameState:
    def __init__(self, width, height):
        self.grid = SnakeGrid(width, height)
        self.snake = SnakeObject(0, 0)
        self.snake.grow(0, 1)
        self.snake.direction = self.snake.default_direction()
        self.grid.place_snake(self.snake)
        self.place_food()
        self.score = 0
    
    def process_action(self, action):
        if action == 0:
            self.move_up()
        elif action == 1:
            self.move_down()
        elif action == 2:
            self.move_left()
        elif action == 3:
            self.move_right()
        elif action == 4:
            pass
        else:
            raise ValueError("Invalid action: " + str(action))
    
    def move_up(self):
        self.snake.direction = (0, -1)
        # self.process_movement(0, -1)

    def move_down(self):
        self.snake.direction = (0, 1)
        # self.process_movement(0, 1)

    def move_left(self):
        self.snake.direction = (-1, 0)
        # self.process_movement(-1, 0)

    def move_right(self):
        self.snake.direction = (1, 0)
        # self.process_movement(1, 0)
        # self.process_movement(*self.snake.direction())
    
    def process_movement(self):
        x, y = self.snake.direction
        x1, y1 = self.snake.head()
        x2, y2 = x1 + x, y1 + y
        if not self.grid.is_valid(x2, y2):
            return False
        if self.grid.is_snake(x2, y2):
            return False
        if self.grid.is_food(x2, y2):
            self.snake.grow(x2, y2)
            self.place_food()
            self.score += 1
        else:
            self.snake.move(x2, y2)
        return True
    
    def place_food(self):
        while True:
            x = np.random.randint(0, self.grid.width)
            y = np.random.randint(0, self.grid.height)
            if self.grid.is_empty(x, y):
                self.food = (x, y)
                self.grid.place_food(x, y)
                break
        
    def update(self, action):
        self.process_action(action)
        valid = self.process_movement()
        return valid or self.is_game_over()
    
    def update_grid(self):
        self.grid.clear()
        self.grid.place(self.snake, self.food)

    def is_game_over(self):
        return self.snake.is_colliding_with_self()
    
    def reset(self):
        self.snake = SnakeObject(0, 0, (255, 0, 0))
        self.place_food()
        self.grid.place(self.snake, self.food)
        self.score = 0

    

class Game:
    def __init__(self) -> None:
        self.state = GameState(10, 10)
        self.screen = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 5
        self.score = 0
    
    def update(self):
        self.running = not self.state.update_grid() and self.running
        self.draw()
        self.clock.tick(self.fps)
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        print(self.state.grid)
        for y, row in enumerate(self.state.grid.grid):
            for x, cell in enumerate(row):
                color = (255 - cell * 100, 255, cell * 100)
                pygame.draw.rect(self.screen, color, (y * 50, x * 50, 50, 50))
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # self.state.move_up()
                    return 0
                elif event.key == pygame.K_DOWN:
                    # self.state.move_down()
                    return 1
                elif event.key == pygame.K_LEFT:
                    # self.state.move_left()
                    return 2
                elif event.key == pygame.K_RIGHT:
                    return 3
                    # self.state.move_right()
        return 4
    
    def run(self):
        while self.running:
            action = self.handle_events()
            self.state.update(action)
            self.update()
        pygame.quit()


        


if __name__ == "__main__":
    game = Game()
    game.run()
