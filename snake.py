import numpy as np

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
BODY = 1
FRUIT = 2

class Snake:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        # Reset snake data
        self.reset_snake()

    def reset_snake(self):
        # Initial Snake head location
        self.head_row = self.grid_size // 2
        self.head_column = self.grid_size // 2
        # Initial snake head and tail directions
        self.head_direction = RIGHT
        self.tail_direction = RIGHT
        # Snake body list
        self.body = [[self.head_row, self.head_column],
                     [self.head_row, self.head_column - 1]]
        self.food_location = self.make_food()
        # Food color
        self.food_photo = np.random.randint(0, 255)
        # Game score
        self.score = 0
        # Food eaten during this step
        self.food_eaten = False

    def get_grid(self):
        # Set empty locations as zeros
        self.grid = np.zeros((self.grid_size, self.grid_size))
        # Set snake body locations as -1
        for part in self.body:
            self.grid[part[0], part[1]] = BODY
        self.grid[self.food_location[0], self.food_location[1]] = FRUIT
        return self.grid

    def check_walls_collision(self):
        head = self.body[0]
        # Check if the head hit one of the upper, lower, left or right walls
        return (head[0] < 0 or head[0] >= self.grid_size or\
                head[1] < 0 or head[1] >= self.grid_size)

    def check_body_collision(self):
        head = self.body[0]
        # Loop over all parts of the body and check if the head hit one of them
        for part in self.body[1:]:
            if head == part:
                return True
        return False

    def check_food_eaten(self):
        head = self.body[0]
        return head == self.food_location

    def check_food_collision(self, food_location):
        # Check if there is a collision between the food and the snake body
        for part in self.body:
            if (food_location[0] == part[0]) and (food_location[1] == part[1]):
                return True
        # Check if there is a collision between the food and walls
        if (food_location[0] < 0 or food_location[0] >= self.grid_size or\
            food_location[1] < 0 or food_location[1] >= self.grid_size):
            return True

        return False

    def make_food(self):
        # Create food in a random location
        food_location = np.random.randint(0, self.grid_size, 2).tolist()
        # While the food collides with a part of the body
        while(self.check_food_collision(food_location)):
            # Create food in another location
            food_location = np.random.randint(0, self.grid_size, 2).tolist()
        self.food_photo = np.random.randint(0, 255)
        return food_location

    def change_direction(self, direction):
        if ((self.head_direction == UP or self.head_direction == DOWN) and\
            (direction == LEFT or direction == RIGHT)) or\
           ((self.head_direction == LEFT or self.head_direction == RIGHT) and\
               (direction == UP or direction == DOWN)):
           self.head_direction = direction
           return True
        return False

    def step(self):
        self.food_eaten = False

        next_location = self.body[0].copy()

        # Increment head location
        if self.head_direction == UP:
            self.body[0][0] -= 1
        elif self.head_direction == DOWN:
            self.body[0][0] += 1
        elif self.head_direction == LEFT:
            self.body[0][1] -= 1
        elif self.head_direction == RIGHT:
            self.body[0][1] += 1

        # Each part of the body inherits the location of the part closer to tail
        for i in range(len(self.body[1:])):
            temp = self.body[i + 1].copy()
            self.body[i + 1] = next_location
            next_location = temp

        # Check for collision between walls and between body
        if(self.check_walls_collision() or self.check_body_collision()):
            return False

        # Check if the food was eaten
        if(self.check_food_eaten()):
            # Set food as eaten
            self.food_eaten = True
            # Add food at a new location
            self.food_location = self.make_food()
            self.score += 1
            self.body.append(next_location)

        if self.body[-1][0] - 1 == self.body[-2][0]:
            self.tail_direction = UP
        elif self.body[-1][0] + 1 == self.body[-2][0]:
            self.tail_direction = DOWN
        elif self.body[-1][1] - 1 == self.body[-2][1]:
            self.tail_direction = LEFT
        elif self.body[-1][1] + 1 == self.body[-2][1]:
            self.tail_direction = RIGHT

        return True
