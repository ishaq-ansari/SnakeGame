"""SnakeGame using Pygame"""

import pygame
import random
import time
import sys

# Initialize game engine
pygame.init()

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Set screen size and title
screen_size = (700, 500)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake Game")

# Set clock for controlling game speed
clock = pygame.time.Clock()


def main():
    """Runs the game"""

    game_over_flag = False

    # Start the game loop
    while not game_over_flag:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Define block size and font
        block_size = 10
        font = pygame.font.SysFont("Roboto", 30)

        # Initialize snake and food positions
        snake_position = [0, 50]
        snake_body = [[0, 50], [90, 50], [80, 50]]
        food_position = [
            random.randrange(1, (screen_size[0] // block_size)) * block_size,
            random.randrange(1, (screen_size[1] // block_size)) * block_size,
        ]
        food_spawned = True

        # Initialize direction and score
        direction = "RIGHT"
        change_to = direction
        speed = 10
        score = 0
        game_paused = False

        try:
            # Load the highest scores from the file if the file exist
            f = open("records.txt")
            str_h_score = f.read()
            h_score = int(str_h_score)
            f.close()
        except:
            # create a file with highest score "0" if file doesn't exist
            f = open(
                "records.txt", "w"
            )  # the second argument, 'w', means the file is being opened in write mode
            f.writelines("0")
            f.close()

            # Load the highest scores from the file
            f = open("records.txt")
            str_h_score = f.read()
            h_score = int(str_h_score)
            f.close()

        # Game loop
        running = True
        while running:
            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # Quit the game engine
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        change_to = "UP"
                    if event.key == pygame.K_DOWN:
                        change_to = "DOWN"
                    if event.key == pygame.K_LEFT:
                        change_to = "LEFT"
                    if event.key == pygame.K_RIGHT:
                        change_to = "RIGHT"
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if (event.key == pygame.K_p) or ((event.key == pygame.K_SPACE)):
                        game_paused = not game_paused

            if not game_paused:
                # Validate direction change
                if change_to == "UP" and direction != "DOWN":
                    direction = "UP"
                if change_to == "DOWN" and direction != "UP":
                    direction = "DOWN"
                if change_to == "LEFT" and direction != "RIGHT":
                    direction = "LEFT"
                if change_to == "RIGHT" and direction != "LEFT":
                    direction = "RIGHT"

                # Move snake
                if direction == "UP":
                    snake_position[1] -= block_size
                if direction == "DOWN":
                    snake_position[1] += block_size
                if direction == "LEFT":
                    snake_position[0] -= block_size
                if direction == "RIGHT":
                    snake_position[0] += block_size

                # Add new block to snake body
                snake_body.insert(0, list(snake_position))

                # Check if food was eaten
                if (
                    snake_position[0] == food_position[0]
                    and snake_position[1] == food_position[1]
                ):
                    score += 1
                    # check if current score is greater than high score, if so, make that high score
                    if score > h_score:
                        h_score = score
                    food_spawned = False  # switch the food_spawn to false so that new food is generated

                    # controls the speed of the snake
                    if score == 10:
                        speed = 15
                    if score == 25:
                        speed = 25
                    if score == 50:
                        speed = 35
                else:
                    snake_body.pop()

                # Spawn new food if necessary
                if not food_spawned:
                    food_position = [
                        random.randrange(1, (screen_size[0] // block_size))
                        * block_size,
                        random.randrange(1, (screen_size[1] // block_size))
                        * block_size,
                    ]
                food_spawned = True

                # Check if snake hit the wall or itself
                if snake_position[0] > screen_size[0] or snake_position[0] < 0:
                    if score > h_score:
                        h_score = score
                    running = False
                if snake_position[1] > screen_size[1] or snake_position[1] < 0:
                    if score > h_score:
                        h_score = score
                    running = False
                for block in snake_body[1:]:
                    if snake_position[0] == block[0] and snake_position[1] == block[1]:
                        if score > h_score:
                            h_score = score
                        running = False

                # Draw screen
                screen.fill(black)
                for pos in snake_body:
                    pygame.draw.rect(
                        screen,
                        white,
                        pygame.Rect(pos[0], pos[1], block_size, block_size),
                    )
                pygame.draw.rect(
                    screen,
                    red,
                    pygame.Rect(
                        food_position[0], food_position[1], block_size, block_size
                    ),
                )

                # Display score
                score_text = font.render("Score: " + str(score), True, white)
                screen.blit(score_text, [5, 0])

                highest_score = font.render(
                    "Highest Score: " + str(h_score), True, white
                )
                screen.blit(highest_score, [500, 0])

                # Set game speed
                clock.tick(speed)

                # Refresh screen
                pygame.display.update()

        # save the new high score
        str_h_score = str(h_score)
        f = open(
            "records.txt", "w"
        )  # the second argument, 'w', means the file is being opened in write mode
        f.writelines(str_h_score)
        f.close()

        # game over message
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(
            center=(screen_size[0] // 2, screen_size[1] // 2)
        )
        screen.blit(game_over_text, game_over_rect)

        score_text = font.render("Your score is " + str(score), True, white)
        score_rect = score_text.get_rect(
            center=(screen_size[0] / 2, screen_size[1] / 2 + 50)
        )
        screen.blit(score_text, score_rect)

        restart_text = font.render("Restarts in 2 seconds", True, white)
        restart_rect = restart_text.get_rect(
            center=(screen_size[0] / 2, screen_size[1] / 2 + 100)
        )
        screen.blit(restart_text, restart_rect)
        pygame.display.flip()  # make sure that any changes made to the display are shown on the screen.

        time.sleep(2)  # set a delay of 2 second

    # Quit the game
    pygame.quit()


# Run the game
main()
