import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 900, 700
NODE_COLOR = (135, 206, 250)
BLACK = (0, 0, 0)
NODE_RADIUS = 20
FONT_SIZE = 20
ARROW_SIZE = 10
WHITE = (255, 255, 255)
BROWN = (165, 42, 42)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
TRAVERSAL_COLOR = (0, 0, 255)
TRAVERSAL_RADIUS = 5

# Define node positions
node_positions = {
    'A': (600, 100),
    'B': (400, 200),
    'C': (700, 200),
    'D': (100, 400),
    'E': (650, 600),
    'F': (300, 400),
    'G': (800, 400),
    'H': (500, 400),
    'K': (800, 600),
    'I': (300, 600)
}

# Define the graph structure
graf = {
    'A': {'B', 'C'},
    'B': {'D', 'F', 'C', 'H'},
    'C': {'G'},
    'D': {'E'},
    'E': {'I', 'K'},
    'K': {},
    'F': {'I', 'H'},
    'G': {'H', 'E', 'K'},
    'H': {'I'},
    'I': {}
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DFS Visualization")
font = pygame.font.SysFont(None, FONT_SIZE)
visited = set()
parent = {}
edge_colors = {}
start_time = {}
end_time = {}
time = 0

def draw_graph(screen, graf, node_positions, parent, visited, edge_colors, start_time, end_time, traversal_position=None):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    text = font.render("DFS", True, BLACK)
    screen.blit(text, (50, 50))
    
    for node, neighbors in graf.items():
        start_pos = node_positions[node]
        for neighbor in neighbors:
            end_pos = node_positions[neighbor]
            color = edge_colors.get((node, neighbor), BLACK)
            pygame.draw.line(screen, color, start_pos, end_pos, 4)
            
            direction_x = end_pos[0] - start_pos[0]
            direction_y = end_pos[1] - start_pos[1]
            length = math.sqrt(direction_x ** 2 + direction_y ** 2)
            direction_x /= length
            direction_y /= length
            
            marker_pos = (
                end_pos[0] - direction_x * NODE_RADIUS * 1.5,
                end_pos[1] - direction_y * NODE_RADIUS * 1.5
            )
            pygame.draw.circle(screen, BLACK, marker_pos, 5)

    for node, pos in node_positions.items():
        pygame.draw.circle(screen, NODE_COLOR, pos, NODE_RADIUS)
        font = pygame.font.Font(None, 25)
        text = font.render(str(node), True, BLACK)
        screen.blit(text, (pos[0] - 8, pos[1] - 10))
        
        if node in start_time and node in end_time:
            time_text = font.render(f"{start_time[node]}/{end_time[node]}", True, BLACK)
            screen.blit(time_text, (pos[0] - 10, pos[1] + 30))

    if traversal_position:
        pygame.draw.circle(screen, TRAVERSAL_COLOR, traversal_position, TRAVERSAL_RADIUS)

    pygame.display.flip()

def move_edge(start_pos, end_pos, steps):
    for step in range(steps):
        t = step / float(steps)
        traversal_position = (
            (1 - t) * start_pos[0] + t * end_pos[0],
            (1 - t) * start_pos[1] + t * end_pos[1]
        )
        draw_graph(screen, graf, node_positions, parent, visited, edge_colors, start_time, end_time, traversal_position)
        pygame.time.delay(35)

def dfs_visit(node):
    global time
    time += 1
    start_time[node] = time
    visited.add(node)
    draw_graph(screen, graf, node_positions, parent, visited, edge_colors, start_time, end_time, node_positions[node])
    pygame.time.delay(1000)

    for neighbor in graf[node]:
        if neighbor not in visited:
            parent[neighbor] = node
            edge_colors[(node, neighbor)] = GREEN
            move_edge(node_positions[node], node_positions[neighbor], 20)
            dfs_visit(neighbor)
        elif neighbor in start_time and neighbor not in end_time:
            edge_colors[(node, neighbor)] = PURPLE
        elif neighbor in visited and parent.get(node) != neighbor:
            edge_colors[(node, neighbor)] = BROWN

    time += 1
    end_time[node] = time
    draw_graph(screen, graf, node_positions, parent, visited, edge_colors, start_time, end_time, node_positions[node])
    pygame.time.delay(1000)

def main():
    clock = pygame.time.Clock()
    dfs_visit('A')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)

if __name__ == "__main__":
    main()
