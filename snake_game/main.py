import pygame
import random

# Initialize the game
pygame.init()

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of the screen
screen_width = 800
screen_height = 600
block_size = 20

# Set the initial speed of the snake
snake_speed = 15

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")


# Function to display game over message
def game_over():
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 - text.get_height()))
    screen.blit(text, text_rect)

    # Display the options
    font = pygame.font.Font(None, 36)
    text = font.render("Press ''Esc'' to exit", True, WHITE)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)

    text = font.render("Press ''Enter'' to play again", True, WHITE)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 + text.get_height()))
    screen.blit(text, text_rect)

    pygame.display.flip()


# Function to display the score
def show_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))


# Define main game function
def game():
    game_over_flag = False
    game_exit = False

    while not game_exit:
        # Set initial position of the snake
        x1 = screen_width / 2
        y1 = screen_height / 2

        # Set initial change in position of the snake
        x1_change = 0
        y1_change = 0

        # Create snake body
        snake_list = []
        length_of_snake = 1

        # Set initial position of the food
        foodx = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
        foody = round(random.randrange(0, screen_height - block_size) / 20.0) * 20.0

        while not game_exit and not game_over_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -block_size
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = block_size
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -block_size
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = block_size
                        x1_change = 0

            # Check if the snake hits the walls
            if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
                game_over_flag = True

            # Update the position of the snake
            x1 += x1_change
            y1 += y1_change
            screen.fill(BLACK)

            # Draw food
            pygame.draw.rect(screen, GREEN, [foodx, foody, block_size, block_size])

            # Draw snake
            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            # Check if the snake hits itself
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_over_flag = True

            # Draw the snake body
            for segment in snake_list:
                pygame.draw.rect(screen, WHITE, [segment[0], segment[1], block_size, block_size])

            # Check if the snake eats the food
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
                foody = round(random.randrange(0, screen_height - block_size) / 20.0) * 20.0
                length_of_snake += 1

            # Update the screen
            show_score(length_of_snake - 1)
            pygame.display.update()

            # Set the snake speed
            clock = pygame.time.Clock()
            clock.tick(snake_speed)

        while game_over_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over_flag = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_exit = True
                        game_over_flag = False
                    elif event.key == pygame.K_RETURN:
                        game_over_flag = False

            screen.fill(BLACK)
            game_over()

    # Quit the game
    pygame.quit()
    quit()


# Start the game
game()