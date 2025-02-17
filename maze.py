import pygame
import random
import numpy as np
from collections import deque

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Path color
RED = (255, 0, 0)    # Goal color
BLUE = (0, 0, 255)   # Agent color

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

# Fonts for displaying distance
font = pygame.font.Font(None, 36)

# Maze and agent parameters
maze = np.zeros((MAZE_HEIGHT, MAZE_WIDTH))
agent_pos = (1, 1)
goal_pos = (MAZE_HEIGHT - 2, MAZE_WIDTH - 2)

# Create a random maze with walls
def create_maze():
    global maze
    maze = np.zeros((MAZE_HEIGHT, MAZE_WIDTH))  # Reset maze
    for i in range(MAZE_HEIGHT):
        for j in range(MAZE_WIDTH):
            if random.random() < 0.2:  # 20% chance to place walls
                maze[i, j] = 1
    maze[agent_pos[0], agent_pos[1]] = 0  # Ensure agent starts on empty space
    maze[goal_pos[0], goal_pos[1]] = 0  # Ensure goal is open

# Draw the maze
def draw_maze():
    for row in range(MAZE_HEIGHT):
        for col in range(MAZE_WIDTH):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[row, col] == 1:  # Wall
                pygame.draw.rect(screen, BLACK, cell_rect)
            pygame.draw.rect(screen, BLACK, cell_rect, 2)  # Apply black border to all cells

# Draw the goal
def draw_goal():
    pygame.draw.circle(screen, RED, (goal_pos[1] * CELL_SIZE + CELL_SIZE // 2, goal_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

# Action space for agent (up, down, left, right)
actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# BFS to find the shortest path
def find_shortest_path():
    queue = deque([(agent_pos, [])])  # Queue with (position, path)
    visited = set()
    
    while queue:
        (current_pos, path) = queue.popleft()
        
        if current_pos in visited:
            continue
        visited.add(current_pos)
        
        if current_pos == goal_pos:
            return path + [goal_pos]  # Return full path

        for action in actions:
            new_pos = (current_pos[0] + action[0], current_pos[1] + action[1])
            if 0 <= new_pos[0] < MAZE_HEIGHT and 0 <= new_pos[1] < MAZE_WIDTH and maze[new_pos[0], new_pos[1]] == 0:
                queue.append((new_pos, path + [current_pos]))

    return []  # No path found

# Draw the shortest path
def draw_path(path):
    for pos in path:
        pygame.draw.circle(screen, GREEN, (pos[1] * CELL_SIZE + CELL_SIZE // 2, pos[0] * CELL_SIZE + CELL_SIZE // 2), 5)

# Animate agent moving along the path
def animate_agent(path):
    for pos in path:
        screen.fill(WHITE)  # Clear screen
        draw_maze()
        draw_goal()
        draw_path(path)  # Show full path
        pygame.draw.circle(screen, BLUE, (pos[1] * CELL_SIZE + CELL_SIZE // 2, pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
        # Display distance
        text = font.render(f"Distance: {len(path)-1} steps", True, BLACK)
        screen.blit(text, (20, 20))

        pygame.display.flip()
        pygame.time.delay(150)  # Animation speed

# Main game loop
def main():
    while True:
        create_maze()  # Generate a new maze
        path = find_shortest_path()
        
        if len(path) > 1:  # If a valid path is found
            break  # Exit loop and proceed

    distance = len(path) - 1  # Number of steps from start to goal
    running = True

    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_maze()
        draw_goal()
        draw_path(path)

        # Display distance
        text = font.render(f"Distance: {distance} steps", True, BLACK)
        screen.blit(text, (20, 20))

        pygame.display.flip()
        pygame.time.delay(500)  # Wait before animation starts

        # Animate agent moving step by step
        animate_agent(path)

        pygame.time.delay(2000)  # Wait before generating a new maze

main()
pygame.quit()

