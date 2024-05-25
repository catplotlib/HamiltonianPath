import pygame
import sys
from game import Game
from graph import Graph

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
VERTEX_RADIUS = 20
VERTEX_COLOR = (255, 255, 255)
EDGE_COLOR = (128, 128, 128)
FONT_SIZE = 18
FONT_COLOR = (255, 255, 255)


import pygame
import sys
from game import Game
from graph import Graph

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
VERTEX_RADIUS = 20
VERTEX_COLOR = (255, 255, 255)
EDGE_COLOR = (128, 128, 128)
FONT_SIZE = 18
FONT_COLOR = (255, 255, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Hamiltonian Cycle Game")
    clock = pygame.time.Clock()

    # Instantiate the game with a temporary graph just for initialization
    temp_graph = Graph(1)  # Minimum vertices to initialize
    game = Game(temp_graph, screen)
    game.clock = clock  # Pass the clock to the game

    # Start Menu
    game.show_start_menu()

    # Get the number of vertices from the user after they press 'S'
    num_vertices = game.get_user_input("Enter number of vertices: ")
    edge_probability = 0.8  # This can also be made dynamic

    # Now create the actual graph with user-defined vertices
    graph = Graph(num_vertices)
    graph.generate_random_graph(edge_probability)
    game.graph = graph  # Set the actual graph in the game

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    game.handle_click(pos)

        game.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

