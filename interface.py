import pygame
import config

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        
        self.font_big = pygame.font.SysFont('Arial', 40, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 20)
        self.font_ui = pygame.font.SysFont('Arial', 28, bold=True)
        self.font_grid = pygame.font.SysFont('Arial', 36, bold=True)

    def draw_button(self, text, rect, base_color, hover_color):
        mx, my = pygame.mouse.get_pos()
        
        color = hover_color if rect.collidepoint(mx, my) else base_color
        
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        pygame.draw.rect(self.screen, config.DARK_GREY, rect, width=3, border_radius=15)
        
        txt_surf = self.font_ui.render(text, True, config.WHITE)
        txt_rect = txt_surf.get_rect(center=rect.center)
        self.screen.blit(txt_surf, txt_rect)

    def draw_clues(self, level_index):
        start_x = 50 + (10 * (config.CELL_SIZE + config.MARGIN)) + 40
        start_y = 50
        level_data = config.LEVELS[level_index]
        
        title = self.font_ui.render("Pytania:", True, config.BLACK)
        self.screen.blit(title, (start_x, start_y - 40))

        y_offset = 0
        for line in level_data['clues']:
            color = config.BLACK if line.endswith(":") else config.DARK_GREY
            font = self.font_ui if line.endswith(":") else self.font_small
            
            clue_surf = font.render(line, True, color)
            self.screen.blit(clue_surf, (start_x, start_y + y_offset))
            y_offset += 30

    def draw_grid(self, local_board, local_locks, my_id, solution_grid):
        for r in range(10):
            for c in range(10):
                x = 50 + c * (config.CELL_SIZE + config.MARGIN)
                y = 50 + r * (config.CELL_SIZE + config.MARGIN)
                rect = pygame.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE)
                
                color = config.WHITE
                if solution_grid[r][c] == '.': 
                    color = config.BLACK
                elif local_board[r][c] == solution_grid[r][c]: 
                    color = config.GREEN
                elif my_id is not None and local_locks[r][c] == my_id: 
                    color = config.BLUE
                elif local_locks[r][c] is not None: 
                    color = config.RED
                
                # Rysowanie kwadratu
                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                
                # Obramowanie
                if solution_grid[r][c] != '.':
                    pygame.draw.rect(self.screen, config.DARK_GREY, rect, width=2, border_radius=5)

                # Litera
                if solution_grid[r][c] != '.':
                    char = local_board[r][c] if r < len(local_board) else ""
                    txt_color = config.BLACK if color != config.BLACK else config.WHITE
                    txt = self.font_grid.render(char, True, txt_color)
                    self.screen.blit(txt, txt.get_rect(center=rect.center))

    def draw_game_over_overlay(self, level_index, btn_next_rect):
        s = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        s.set_alpha(220)
        s.fill(config.WHITE)
        self.screen.blit(s, (0,0))
        
        msg = self.font_big.render("POZIOM UKOŃCZONY!", True, config.GREEN_DARK)
        self.screen.blit(msg, (config.SCREEN_WIDTH//2 - msg.get_width()//2, 200))
        
        if level_index + 1 < len(config.LEVELS):
            self.draw_button("NASTĘPNY POZIOM", btn_next_rect, config.BUTTON_COLOR, config.BUTTON_HOVER)
        else:
            fin = self.font_ui.render("To wszystkie poziomy! Dzięki za grę.", True, config.BLACK)
            self.screen.blit(fin, (config.SCREEN_WIDTH//2 - fin.get_width()//2, 350))

    def draw_menu(self, btn_start_rect):
        title = self.font_big.render("Krzyżówka", True, config.BLACK)
        self.screen.blit(title, (config.SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        self.draw_button("ROZPOCZNIJ GRĘ", btn_start_rect, config.BUTTON_COLOR, config.BUTTON_HOVER)
        
        info = self.font_small.render("Czekaj na innych graczy...", True, config.DARK_GREY)
        self.screen.blit(info, (config.SCREEN_WIDTH//2 - info.get_width()//2, config.SCREEN_HEIGHT//2 + 50))