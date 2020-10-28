import numpy as np

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
BODY = 1
FRUIT = 2
FRUIT_REWARD = 1e5


class DynamicProgrammingRLAgent:
    def __init__(self, grid_size, gamma, theta):
        self.grid_size = grid_size
        self.gamma = gamma
        self.theta = theta


    def policy_iteration(self, grid, snake_head):
        values = np.zeros((self.grid_size + 2, self.grid_size + 2))

        delta = float('inf')
        while delta > self.theta:
            delta = 0
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    state = grid[i, j]
                    point = (i, j)

                    # Check if this state is a terminal state
                    if self.is_terminal_state(state):
                        continue

                    # Get the possible actions at the current state
                    actions = self.get_state_actions(grid, point)
                    new_value = 0

                    # If there is no action due to being trapped for example
                    # Then return any random action
                    if not len(actions):
                        return np.random.randint(0, 4)

                    for action in actions:
                        # We assume equiprobable actions
                        next_point, reward, pi_a_s = self.get_action_results(grid, point, action)
                        result = pi_a_s * (reward + self.gamma * values[next_point[0] + 1, next_point[1] + 1])
                        result /= len(actions)
                        new_value += result

                    delta = max(delta, abs(values[i + 1, j + 1] - new_value))

                    values[i + 1, j + 1] = new_value

        # Set body values to -1
        # Set fruit values to fruit reward
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if grid[i, j] == BODY:
                    values[i + 1, j + 1] = -1
                elif grid[i, j] == FRUIT:
                    values[i + 1, j + 1] = FRUIT_REWARD

        # Set wall values to -1
        values[:, 0] = -1
        values[:, -1] = -1
        values[0, :] = -1
        values[-1, :] = -1

        # Get the direction which maximizes the value
        snake_point = np.array([snake_head[0] + 1 , snake_head[1] + 1])
        neighbors = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
        next_points = snake_point + neighbors
        best_direction =  np.argmax(np.array([values[next_point[0], next_point[1]] for next_point in next_points]))

        return best_direction


    def is_terminal_state(self, state):
        return state == BODY or state == FRUIT

    def get_state_actions(self, grid, point):
        actions = []
        # All possible actions
        possible_actions = [UP, DOWN, LEFT, RIGHT]
        for action in possible_actions:
            # Get the result of movement in this direction
            target = self.get_movement_result(point, action)
            # Check if the result of movement is not outside the grid
            if target[0] >= 0 and target[0] < self.grid_size and target[1] >= 0 and target[1] < self.grid_size:
                # Check if the result of movement is not a body part
                if grid[target[0]][target[1]] != BODY:
                    # Add the action to the actions
                    actions.append(action)
        return actions

    def get_action_results(self, grid, source_point, action):
        target_point = self.get_movement_result(source_point, action)
        reward = 0
        if target_point[0] >= 0 and target_point[0] < self.grid_size and target_point[1] >= 0 and target_point[1] < self.grid_size:
            if grid[target_point[0]][target_point[1]] == FRUIT:
                reward = FRUIT_REWARD
        return [target_point, reward, 1]

    def get_movement_result(self, point, action):
        if action == UP:
            return (point[0] - 1, point[1])
        elif action == DOWN:
            return (point[0] + 1, point[1])
        elif action == LEFT:
            return (point[0], point[1] - 1)
        elif action == RIGHT:
            return (point[0], point[1] + 1)
