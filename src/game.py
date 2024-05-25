import pygame
import sys
from graph import Graph

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
VERTEX_RADIUS = 20
VERTEX_COLOR = (255, 255, 255)
EDGE_COLOR = (128, 128, 128)
FONT_SIZE = 18
FONT_COLOR = (255, 255, 255)

class Game:
    def __init__(self, graph, screen):
        self.graph = graph
        self.screen = screen
        self.selected_vertices = []
        self.game_over = False
        self.winning_path = self.find_hamiltonian_cycle()

    def handle_click(self, pos):
        if self.game_over:
            return  # Game is over, no more input handled.

        clicked_vertex = None
        for vertex in self.graph.get_vertices():
            x, y = self.get_vertex_position(vertex)
            if self.is_inside_vertex(pos, (x, y)):
                clicked_vertex = vertex
                break

        if clicked_vertex is not None:
            if len(self.selected_vertices) == 0:
                # Allow the first vertex to be selected freely.
                self.selected_vertices.append(clicked_vertex)
            elif clicked_vertex in self.graph.get_neighbors(self.selected_vertices[-1]):
                if clicked_vertex not in self.selected_vertices:
                    self.selected_vertices.append(clicked_vertex)
                    if len(self.selected_vertices) == self.graph.num_vertices:
                        if self.is_valid_hamiltonian_cycle(self.selected_vertices):
                            self.game_over = True
                            self.show_game_over_screen(True)
                        else:
                            self.game_over = True
                            self.show_game_over_screen(False)
            # Do not allow selection if not a neighbor
            return

    def is_inside_vertex(self, pos, vertex_pos):
        x, y = pos
        vertex_x, vertex_y = vertex_pos
        distance = ((x - vertex_x) ** 2 + (y - vertex_y) ** 2) ** 0.5
        return distance <= VERTEX_RADIUS

    def get_vertex_position(self, vertex):
        x = (vertex % 5) * (WINDOW_WIDTH // 5) + (WINDOW_WIDTH // 10)
        y = (vertex // 5) * (WINDOW_HEIGHT // 5) + (WINDOW_HEIGHT // 10)
        return x, y

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        self.draw_graph()
        self.draw_selected_vertices()
        pygame.display.flip()  # Update the display

    def draw_graph(self):
        for vertex in self.graph.get_vertices():
            x, y = self.get_vertex_position(vertex)
            color = VERTEX_COLOR  # Default color for non-selected vertices
            if vertex in self.selected_vertices:
                color = (255, 0, 0)  # Color for selected vertices
            elif len(self.selected_vertices) > 0 and vertex in self.graph.get_neighbors(self.selected_vertices[-1]):
                color = (0, 255, 0)  # Color for selectable vertices

            pygame.draw.circle(self.screen, color, (x, y), VERTEX_RADIUS)
            font = pygame.font.Font(None, FONT_SIZE)
            text = font.render(str(vertex), True, FONT_COLOR)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

            for neighbor in self.graph.get_neighbors(vertex):
                x2, y2 = self.get_vertex_position(neighbor)
                pygame.draw.line(self.screen, EDGE_COLOR, (x, y), (x2, y2))

    def draw_selected_vertices(self):
        if len(self.selected_vertices) > 1:
            for i in range(1, len(self.selected_vertices)):
                x1, y1 = self.get_vertex_position(self.selected_vertices[i - 1])
                x2, y2 = self.get_vertex_position(self.selected_vertices[i])
                pygame.draw.line(self.screen, (255, 0, 0), (x1, y1), (x2, y2), 3)  # Line color for selected path

    def show_start_menu(self):
        font_title = pygame.font.Font(None, 60)
        font_options = pygame.font.Font(None, 40)

        title_text = font_title.render("Hamiltonian Cycle Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))

        start_text = font_options.render("Press 'S' to Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        self.screen.fill((0, 0, 0))
        self.screen.blit(title_text, title_rect)
        self.screen.blit(start_text, start_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        waiting = False

    def show_options_screen(self):
        font_title = pygame.font.Font(None, 60)
        font_options = pygame.font.Font(None, 40)

        title_text = font_title.render("Game Options", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150))

        vertices_text = font_options.render("Number of Vertices:", True, (255, 255, 255))
        vertices_rect = vertices_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))

        edge_prob_text = font_options.render("Edge Probability:", True, (255, 255, 255))
        edge_prob_rect = edge_prob_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        self.screen.fill((0, 0, 0))
        self.screen.blit(title_text, title_rect)
        self.screen.blit(vertices_text, vertices_rect)
        self.screen.blit(edge_prob_text, edge_prob_rect)
        pygame.display.flip()

        num_vertices = self.get_user_input(vertices_rect.bottomleft)
        edge_prob = self.get_edge_probability(edge_prob_rect.bottomleft)

        return num_vertices, edge_prob

    def get_edge_probability(self, pos):
        input_box = pygame.Rect(pos[0], pos[1], 100, 40)
        font = pygame.font.Font(None, 32)
        text = ''

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return float(text)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            pygame.draw.rect(self.screen, (255, 255, 255), input_box)
            text_surface = font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            pygame.display.flip()

    def get_user_input(self, prompt):
        pygame.font.init()  # Ensure the font module is initialized
        font = pygame.font.Font(None, 32)  # Choose a font size
        input_box_width = 200
        input_box_height = 32
        input_box_x = (WINDOW_WIDTH - input_box_width) // 2
        input_box_y = (WINDOW_HEIGHT - input_box_height) // 2
        input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''

        prompt_surface = font.render(prompt, True, pygame.Color('white'))
        prompt_rect = prompt_surface.get_rect(center=(WINDOW_WIDTH // 2, input_box_y - 40))  # Position prompt above the input box

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            try:
                                num_vertices = int(text)
                                if num_vertices > 0:
                                    return num_vertices
                                else:
                                    print("Please enter a positive integer.")
                                    text = ''  # Reset text if not positive integer
                            except ValueError:
                                print("Please enter a valid number.")
                                text = ''  # Reset text if not valid
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            
            self.screen.fill((30, 30, 30))  # Dark background for better visibility
            # Render the current text.
            txt_surface = font.render(text, True, color)
            # Blit the text and the prompt.
            self.screen.blit(prompt_surface, prompt_rect)
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            # Blit the input_box rect.
            pygame.draw.rect(self.screen, color, input_box, 2)

            pygame.display.flip()
            pygame.time.Clock().tick(30)  # Limit the frame rate to 30 FPS

    def show_instructions(self):
        font_title = pygame.font.Font(None, 60)
        font_instructions = pygame.font.Font(None, 30)

        title_text = font_title.render("Instructions", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150))

        instructions = [
            "- The objective of the game is to find a Hamiltonian Cycle.",
            "- A Hamiltonian Cycle is a path that visits each vertex exactly once.",
            "- Click on the vertices to select them in the desired order.",
            "- You can only select vertices that are directly connected to the last selected vertex.",
            "- If a valid Hamiltonian Cycle is found, you win the game!",
            "- Press 'R' to reset the game.",
            "- Press 'Q' to quit the game.",
        ]

        self.screen.fill((0, 0, 0))
        self.screen.blit(title_text, title_rect)

        for i, instruction in enumerate(instructions):
            text = font_instructions.render(instruction, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50 + i * 40))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

    def find_hamiltonian_cycle(self):
        n = self.graph.num_vertices
        path = [-1] * n

        # Try different starting vertices for a possible cycle
        for start in range(n):
            path[0] = start
            if self._solve_hamiltonian_cycle(path, 1):
                return path
        return None

    def _solve_hamiltonian_cycle(self, path, pos):
        if pos == len(path):
            # All vertices are in the cycle, now check if the last vertex is connected to the first vertex
            return self.graph.has_edge(path[pos - 1], path[0])

        used_vertices = set(path[:pos])
        for vertex in range(self.graph.num_vertices):
            if vertex not in used_vertices and self.graph.has_edge(path[pos - 1], vertex):
                path[pos] = vertex
                if self._solve_hamiltonian_cycle(path, pos + 1):
                    return True
                # Backtrack
                path[pos] = -1
        return False
    
    def is_valid_hamiltonian_cycle(self, path):
        if len(path) != self.graph.num_vertices:
            return False

        for i in range(len(path)):
            current_vertex = path[i]
            next_vertex = path[(i + 1) % len(path)]
            if next_vertex not in self.graph.get_neighbors(current_vertex):
                return False

        return True

    def show_game_over_screen(self, won):
        font_title = pygame.font.Font(None, 60)
        font_message = pygame.font.Font(None, 40)

        if won:
            title_text = font_title.render("Congratulations!", True, (255, 255, 255))
            message_text = font_message.render("You found a Hamiltonian Cycle!", True, (255, 255, 255))
        else:
            title_text = font_title.render("Game Over", True, (255, 255, 255))
            message_text = font_message.render("The selected path is not a Hamiltonian Cycle.", True, (255, 255, 255))

        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        message_rect = message_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        self.screen.fill((0, 0, 0))
        self.screen.blit(title_text, title_rect)
        self.screen.blit(message_text, message_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False