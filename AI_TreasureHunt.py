import pygame
import random
import heapq

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 500
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // ROWS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (255, 69, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_GREY = (169, 169, 169)

# Initialize grid with 0s (walkable)
def generate_grid(rows, cols):
    return [[0 if random.random() > 0.2 else 1 for _ in range(cols)] for _ in range(rows)]

# Manhattan distance heuristic
def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

# A* algorithm for finding the shortest path
def a_star(grid, start, treasure):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0 + manhattan_distance(start, treasure), 0, start))  # f = g + h
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, treasure)}
    closed_list = set()

    while open_list:
        _, current_g, current = heapq.heappop(open_list)
        
        # If we reached the treasure
        if current == treasure:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        closed_list.add(current)

        # Explore neighbors (including diagonals)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Up, Down, Left, Right, Diagonals
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                neighbor = (nx, ny)

                if neighbor in closed_list:
                    continue

                tentative_g_score = current_g + 1  # Assuming uniform cost (each step has a cost of 1)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, treasure)
                    heapq.heappush(open_list, (f_score[neighbor], tentative_g_score, neighbor))
                    came_from[neighbor] = current

    return None

# Draw the grid
def draw_grid(screen, grid, player, agent, treasure):
    for i in range(ROWS):
        for j in range(COLS):
            color = LIGHT_BLUE if grid[i][j] == 0 else DARK_GREY
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # Draw player, agent, and treasure
    pygame.draw.rect(screen, RED, (player[1] * CELL_SIZE, player[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GREEN, (agent[1] * CELL_SIZE, agent[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, YELLOW, (treasure[1] * CELL_SIZE, treasure[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to get user input for positions
def get_user_input():
    print("Enter the positions (row, column) of the player, agent, and treasure.")
    player_x, player_y = map(int, input("Enter player position (row, col): ").split(','))
    agent_x, agent_y = map(int, input("Enter agent position (row, col): ").split(','))
    treasure_x, treasure_y = map(int, input("Enter treasure position (row, col): ").split(','))
    
    # Validate the input positions
    if not (0 <= player_x < ROWS and 0 <= player_y < COLS):
        print("Invalid player position! It should be within the grid bounds.")
        return None, None, None
    if not (0 <= agent_x < ROWS and 0 <= agent_y < COLS):
        print("Invalid agent position! It should be within the grid bounds.")
        return None, None, None
    if not (0 <= treasure_x < ROWS and 0 <= treasure_y < COLS):
        print("Invalid treasure position! It should be within the grid bounds.")
        return None, None, None
    
    return (player_x, player_y), (agent_x, agent_y), (treasure_x, treasure_y)

# Function to prompt the player for a move
def get_player_move():
    move = input("Enter your move (up, down, left, right, or diagonal directions like up-left, down-right): ").lower()
    return move

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI vs Player Treasure Hunt")

    # Generate grid and get user input
    grid = generate_grid(ROWS, COLS)
    
    # Get user input for player, agent, and treasure positions
    player, agent, treasure = get_user_input()
    
    # Ensure valid positions before proceeding
    if not player or not agent or not treasure:
        pygame.quit()
        return

    grid[player[0]][player[1]] = 0  # Set the player position as walkable
    grid[agent[0]][agent[1]] = 0  # Set the agent position as walkable
    grid[treasure[0]][treasure[1]] = 0  # Set the treasure position as walkable

    # Draw the initial grid with player, agent, and treasure positions
    screen.fill(WHITE)
    draw_grid(screen, grid, player, agent, treasure)
    pygame.display.flip()
    pygame.time.delay(1000)  # Pause to allow player to view initial setup

    # Get the A* path once at the start
    path = a_star(grid, agent, treasure)

    # Game loop
    running = True
    turn = "player"  # Player starts the game
    path_index = 1  # Start at the second step in the path (the first step is the agent's current position)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if turn == "player":
            # Get player's move
            move = get_player_move()

            # Move player based on input
            if move == "up" and player[0] > 0:
                player = (player[0] - 1, player[1])
            elif move == "down" and player[0] < ROWS - 1:
                player = (player[0] + 1, player[1])
            elif move == "left" and player[1] > 0:
                player = (player[0], player[1] - 1)
            elif move == "right" and player[1] < COLS - 1:
                player = (player[0], player[1] + 1)
            elif move == "up-left" and player[0] > 0 and player[1] > 0:
                player = (player[0] - 1, player[1] - 1)
            elif move == "up-right" and player[0] > 0 and player[1] < COLS - 1:
                player = (player[0] - 1, player[1] + 1)
            elif move == "down-left" and player[0] < ROWS - 1 and player[1] > 0:
                player = (player[0] + 1, player[1] - 1)
            elif move == "down-right" and player[0] < ROWS - 1 and player[1] < COLS - 1:
                player = (player[0] + 1, player[1] + 1)

            if player == treasure:
                print("Congratulations! You found the treasure. You win!")
                running = False
                continue

            turn = "agent"  # Switch to agent's turn
        
        elif turn == "agent":
            # Move the agent one step along the path
            if path_index < len(path):
                agent = path[path_index]
                path_index += 1

            if agent == treasure:
                print("The agent has found the treasure. You lose!")
                running = False
                continue

            turn = "player"  # Switch to player's turn

        # Draw updated positions
        screen.fill(WHITE)
        draw_grid(screen, grid, player, agent, treasure)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
