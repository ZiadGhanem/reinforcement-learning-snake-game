from snake import Snake
from reinforcement_learning_agent import DynamicProgrammingRLAgent
import numpy as np
import pygame
import glob
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
SNAKE_COLOR = (57, 148, 60)
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
FIRST_TIME = 0
RUNNING_HUMAN = 1
RUNNING_AGENT = 2
GAMEOVER = 3


BACKGROUND_PATH = "images/background"
FOOD_PATH = "images/food"
MENU_PHOTO_PATH = "images/menu_photo.jpg"
SNAKE_HEAD_PATH = "images/snake/head.png"
SNAKE_BODY_PATH = "images/snake/body.png"
SNAKE_TAIL_PATH = "images/snake/tail.png"
EAT_SOUND_PATH = "sound_effects/eat.wav"
FAIL_SOUND_PATH = "sound_effects/fail.wav"

class App:
    def __init__(self, window_size, grid_size):
        self._running = True
        self._display_surf = None
        # Window size
        self.window_size = window_size
        # Snake Grid Size
        self.grid_size = grid_size


    def on_init(self):
        # Initialize PyGame
        pygame.init()
        # Create the window
        self._display_surf = pygame.display.set_mode(
                                        (self.window_size, self.window_size),
                                        pygame.HWSURFACE | pygame.DOUBLEBUF)
        # Square size
        self.square_size = self.window_size // self.grid_size
        # Delay between movements
        self.delay = 500
        # Game State: 0 -> First Time, 1 -> Playing, 2 -> GameOver
        self.game_state = FIRST_TIME
        # Set the window name
        pygame.display.set_caption('Snake Game')
        # The Snake
        self.snake = Snake(self.grid_size)
        # Create Dynamic Programming Reinforcement Learning Agent
        self.rl_agent = DynamicProgrammingRLAgent(self.grid_size, 0.9, 0.1)
        # Set the window as running
        self._running = True
        # Load the images
        self.load_images()
        # Load the sound effects
        self.load_sound_effects()
        # Rest app choices
        self.reset_app()

    def load_images(self):
        # Load background image
        self.background_imgs = [pygame.image.load(os.path.join(BACKGROUND_PATH, path)) for path in os.listdir(BACKGROUND_PATH)]
        # Resize fruit images
        self.background_imgs = [pygame.transform.scale(img, (self.window_size, self.window_size)) for img in self.background_imgs]
        # Load fruit images
        self.food_imgs = [pygame.image.load(os.path.join(FOOD_PATH, path)) for path in os.listdir(FOOD_PATH)]
        # Resize fruit images
        self.food_imgs = [pygame.transform.scale(img, (self.square_size, self.square_size)) for img in self.food_imgs]
        # Load menu image
        self.menu_img = pygame.image.load(MENU_PHOTO_PATH)
        # Resize menu image
        self.menu_img = pygame.transform.scale(self.menu_img, (self.window_size, self.window_size))
        # Load snake head image
        self.snake_head_img = pygame.image.load(SNAKE_HEAD_PATH)
        # Resize snake head image
        self.snake_head_img = pygame.transform.scale(self.snake_head_img, (self.square_size, self.square_size))
        # Load snake head image
        self.snake_body_img = pygame.image.load(SNAKE_BODY_PATH)
        # Resize snake head image
        self.snake_body_img = pygame.transform.scale(self.snake_body_img, (self.square_size, self.square_size))
        # Load snake tail image
        self.snake_tail_img = pygame.image.load(SNAKE_TAIL_PATH)
        # Resize snake head image
        self.snake_tail_img = pygame.transform.scale(self.snake_tail_img, (self.square_size, self.square_size))

    def load_sound_effects(self):
        # Eating sound effect
        self.eat_sound = pygame.mixer.Sound(EAT_SOUND_PATH)
        # Fail sound effect
        self.fail_sound = pygame.mixer.Sound(FAIL_SOUND_PATH)

    def reset_app(self):
        self.background_choice = np.random.randint(0, len(self.background_imgs))


    def on_event(self, event):
        # If the event is quit
        if event.type == pygame.QUIT:
            # Set the window as not running
            self._running = False

        # If it is the first time or gameover
        elif self.game_state == FIRST_TIME or self.game_state == GAMEOVER:
            if event.type == pygame.KEYDOWN:
                # Human player
                if event.key == pygame.K_RETURN:
                    # Reset the snake
                    self.snake.reset_snake()
                    # Rest app choices
                    self.reset_app()
                    self.game_state = RUNNING_HUMAN
                # Reinforcement learning player
                elif event.key == pygame.K_SPACE:
                    # Reset the snake
                    self.snake.reset_snake()
                    # Rest app choices
                    self.reset_app()
                    self.game_state = RUNNING_AGENT

        # If the game is running
        elif self.game_state == RUNNING_HUMAN:
            # Change snake direction
            if event.type == pygame.KEYDOWN:
                # Quit Game
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GAMEOVER
                if not self.direction_changed:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                        self.direction_changed = True
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                        self.direction_changed = True
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                        self.direction_changed = True
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                        self.direction_changed = True

        elif self.game_state == RUNNING_AGENT:
            if event.type == pygame.KEYDOWN:
                # Quit Game
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GAMEOVER


    def on_loop(self):
        if (self.game_state == RUNNING_HUMAN or self.game_state == RUNNING_AGENT):
            if not self.snake.step():
                self.game_state = GAMEOVER
                # Player failure sound effect
                pygame.mixer.Sound.play(self.fail_sound)
            # Check if food was eaten during this this step
            elif self.snake.food_eaten:
                # Play eating sound effect
                pygame.mixer.Sound.play(self.eat_sound)

    def draw_snake(self):
        # Fill screen with black
        #self._display_surf.fill(BLACK)
        self._display_surf.blit(self.background_imgs[self.background_choice], (0, 0))

        # Draw the grid
        for i in range(self.grid_size):
            pygame.draw.line(self._display_surf,
                             WHITE,
                             (0, i * self.square_size),
                             (self.window_size, i * self.square_size), 1)
            pygame.draw.line(self._display_surf,
                             WHITE,
                             (i * self.square_size, 0),
                             (i * self.square_size, self.window_size), 1)

        # Draw the snake head
        if self.snake.head_direction == UP:
            angle = 0
        elif self.snake.head_direction == DOWN:
            angle = 180
        elif self.snake.head_direction == LEFT:
            angle = 90
        elif self.snake.head_direction == RIGHT:
            angle = 270

        self._display_surf.blit(
                                pygame.transform.rotate(
                                self.snake_head_img, angle),
                                (self.snake.body[0][1] * self.square_size,
                                self.snake.body[0][0] * self.square_size))

        # Draw the snake body
        for part in self.snake.body[1:-1]:
            self._display_surf.blit(self.snake_body_img,
                                    (part[1] * self.square_size,
                                    part[0] * self.square_size))

        # Draw the snake tail
        if self.snake.tail_direction == UP:
            angle = 0
        elif self.snake.tail_direction == DOWN:
            angle = 180
        elif self.snake.tail_direction == LEFT:
            angle = 90
        elif self.snake.tail_direction == RIGHT:
            angle = 270

        self._display_surf.blit(pygame.transform.rotate(
                                self.snake_tail_img, angle),
                                (self.snake.body[-1][1] * self.square_size,
                                self.snake.body[-1][0] * self.square_size))

        # Draw the food
        self._display_surf.blit(
            self.food_imgs[self.snake.food_photo % len(self.food_imgs)],
            (self.snake.food_location[1] * self.square_size,
            self.snake.food_location[0] * self.square_size))

    def on_render(self):
        # If it is the First time then display welcome screen
        if self.game_state == FIRST_TIME or self.game_state == GAMEOVER:
            self._display_surf.blit(self.menu_img, (0, 0))

        # If the game is running then display the game
        elif (self.game_state == RUNNING_HUMAN or self.game_state == RUNNING_AGENT):
            self.draw_snake()

        # If gameover display score and restart screen
        if self.game_state == GAMEOVER:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render("You scored {}".format(self.snake.score), True, WHITE, GRAY)
            text_rect = text.get_rect(center=(self.window_size // 2, self.window_size * 9 // 10))
            self._display_surf.blit(text, text_rect)


        pygame.display.update()

    def on_rl_agent_execute(self):
        # Perform policy iteration
        self.snake.change_direction(self.rl_agent.policy_iteration(self.snake.get_grid(), self.snake.body[0]))

    def on_cleanup(self):
        # Close the window
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        self.last = pygame.time.get_ticks()

        # Direction did not change on this step
        self.direction_changed = False
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            # We need no delay in case of RL Agent
            if self.game_state == RUNNING_AGENT:
                self.on_rl_agent_execute()
                self.on_loop()
                self.on_render()
            # We need delay in case of human player
            else:
                # Check if the delay is over
                now = pygame.time.get_ticks()
                if now - self.last >= self.delay:
                    self.on_loop()
                    self.on_render()
                    self.last = now
                    # We can now change the direction again
                    self.direction_changed = False

        self.on_cleanup()
