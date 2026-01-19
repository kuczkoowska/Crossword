import pygame
import socket
import threading
import json
import config
import sys
from interface import GameRenderer

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Krzyżówka Multiplayer")

renderer = GameRenderer(screen)

my_id = None
local_board = [['' for _ in range(10)] for _ in range(10)]
local_locks = [[None for _ in range(10)] for _ in range(10)]
current_level = 0
game_active = False
game_finished = False
running = True

BTN_WIDTH, BTN_HEIGHT = 300, 80
btn_start_rect = pygame.Rect(
    config.SCREEN_WIDTH//2 - BTN_WIDTH//2, 
    config.SCREEN_HEIGHT//2 - BTN_HEIGHT//2, 
    BTN_WIDTH, BTN_HEIGHT
)
btn_next_rect = pygame.Rect(
    config.SCREEN_WIDTH//2 - BTN_WIDTH//2, 
    config.SCREEN_HEIGHT//2 + 60, 
    BTN_WIDTH, BTN_HEIGHT
)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((config.HOST, config.PORT))
except:
    print("Brak połączenia!")
    sys.exit()

def send_action(action, r=0, c=0, char=None):
    msg = {"action": action, "r": r, "c": c}
    if char: msg["char"] = char
    try: client.send((json.dumps(msg) + "\n").encode('utf-8'))
    except: pass

def receive_data():
    global my_id, local_board, local_locks, game_active, game_finished, current_level, running
    buffer = ""
    while running:
        try:
            data = client.recv(4096).decode('utf-8')
            if not data: break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line: continue
                try:
                    msg = json.loads(line)
                    if msg.get("type") == "WELCOME":
                        my_id = msg["id"]
                    else:
                        local_board = msg["board"]
                        local_locks = msg["locks"]
                        game_active = msg["active"]
                        game_finished = msg["finished"]
                        current_level = msg["level_index"]
                except: pass
        except: break

threading.Thread(target=receive_data, daemon=True).start()

while running:
    current_solution = config.LEVELS[current_level]['grid']
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            
            if not game_active:
                if btn_start_rect.collidepoint(mx, my):
                    send_action("START_GAME")

            elif game_finished:
                if btn_next_rect.collidepoint(mx, my):
                    send_action("NEXT_LEVEL")

            else:
                c = (mx - 50) // (config.CELL_SIZE + config.MARGIN)
                r = (my - 50) // (config.CELL_SIZE + config.MARGIN)
                if 0 <= r < 10 and 0 <= c < 10:
                    if current_solution[r][c] != '.' and local_board[r][c] != current_solution[r][c]:
                        send_action("SELECT", r, c)

        if event.type == pygame.KEYDOWN and game_active and not game_finished:
            tr, tc = -1, -1
            for i in range(10):
                for j in range(10):
                    if my_id is not None and local_locks[i][j] == my_id:
                        tr, tc = i, j
            
            if tr != -1 and event.unicode.isalpha():
                if local_board[tr][tc] != current_solution[tr][tc]:
                     send_action("UPDATE", tr, tc, event.unicode)

    screen.fill(config.GREY)

    if not game_active:
        renderer.draw_menu(btn_start_rect)
    else:
        renderer.draw_grid(local_board, local_locks, my_id, current_solution)
        renderer.draw_clues(current_level)

        if game_finished:
            renderer.draw_game_over_overlay(current_level, btn_next_rect)

    pygame.display.flip()

pygame.quit()