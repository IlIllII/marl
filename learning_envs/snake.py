import pygame
import numpy as np

class Snake:
    def __init__(self, start_pos, start_direction) -> None:
        self.direction = start_direction
        self.body = [start_pos, start_pos - start_direction]
    
    def set_direction(self, direction):
        self.direction = direction
    
    def move(self):
        self.body.insert(0, self.body[0] + self.direction)
        self.body.pop()
    
    def grow(self):
        self.body.insert(0, self.body[0] + self.direction)
    
    def head(self):
        return self.body[0]
    
    def tail(self):
        return self.body[-1]
    
    def __len__(self):
        return len(self.body)
    
    def __iter__(self):
        return iter(self.body)
    
    def __getitem__(self, index):
        return self.body[index]
    
    def __setitem__(self, index, value):
        self.body[index] = value

class GameBoard:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height), dtype=np.int8)
    
    def clear(self):
        self.grid = np.zeros((self.width, self.height), dtype=np.int8)

    def clear_snake(self):
        self.grid[self.grid > 0] = 0

    def clear_food(self):
        self.grid[self.grid < 0] = 0
    
    def place_snake(self, snake):
        # snake is represented by ascending numbers on grid, with head being 1 and tal being len(snake)
        for i, (x, y) in enumerate(snake):
            self.grid[x % self.width, y % self.height] = i + 1
    
    def place_food(self):
        empty = np.where(self.grid == 0)
        i = np.random.randint(len(empty[0]))
        x, y = empty[0][i], empty[1][i]
        self.grid[x, y] = -1
    

class GameState:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.snake = Snake(np.array([width//2, height//2]), np.array([0, 1]))
        self.board = GameBoard(width, height)
        self.board.place_snake(self.snake)
        self.board.place_food()
    
    def is_valid(self, direction):
        result = (self.snake.direction[0] + direction[0], self.snake.direction[1] + direction[1])
        return result != (0, 0)

    def step(self, direction=None):
        if direction is not None and self.is_valid(direction): # and np.sum(self.snake.direction + direction) != 0:
            self.snake.set_direction(direction)
        next_head_loc = self.snake.head() + self.snake.direction
        next_head_cell = self.board.grid[next_head_loc[0] % self.width, next_head_loc[1] % self.height]
        if next_head_cell == 0:
            self.snake.move()
        elif next_head_cell == -1:
            self.snake.grow()
            self.board.clear_food()
            self.board.place_food()
        elif next_head_cell > 0:
            self.board.clear()
            self.snake = Snake(np.array([self.width//2, self.height//2]), np.array([0, 1]))
            self.board.place_snake(self.snake)
            self.board.place_food()
        self.board.clear_snake()
        self.board.place_snake(self.snake)

            



if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 500))
    running = True
    game_state = GameState(10, 10)
    while running:
        direction = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if direction is not None:
                    pygame.event.post(event)
                elif event.key == pygame.K_LEFT:
                    direction = np.array([-1, 0])
                elif event.key == pygame.K_RIGHT:
                    direction = np.array([1, 0])
                elif event.key == pygame.K_UP:
                    direction = np.array([0, -1])
                elif event.key == pygame.K_DOWN:
                    direction = np.array([0, 1])
            
        game_state.step(direction)
        screen.fill((0, 0, 0))
        for i in range(game_state.board.grid.shape[0]):
            for j in range(game_state.board.grid.shape[1]):
                pygame.draw.rect(screen, (0, 255, 0), (i*50, j*50, 50, 50), 1)
                if game_state.board.grid[i, j] > 0:
                    pygame.draw.rect(screen, (255, 255, 255), (i*50, j*50, 50, 50))
                elif game_state.board.grid[i, j] < 0:
                    pygame.draw.rect(screen, (255, 0, 0), (i*50, j*50, 50, 50))
        pygame.display.flip()
        clock.tick(5)
    pygame.quit()