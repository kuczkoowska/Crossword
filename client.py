import pygame
import socket
import threading
import json
import config
import sys

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Krzyżówka Pygame")
font = pygame.font.SysFont('Arial', 40)

my_id = None
local_board = [['' for _ in range(10)] for _ in range(10)]
local_locks = [[None for _ in range(10)] for _ in range(10)]
running = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((config.HOST, config.PORT))
except:
    print("Błąd połączenia z serwerem!")
    sys.exit()

def send_action(action, r, c, char=None):
    msg = {"action": action, "r": r, "c": c}
    if char: msg["char"] = char
    try:
        client.send((json.dumps(msg) + "\n").encode('utf-8'))
    except: pass

def receive_data():
    global my_id, local_board, local_locks, running
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
                    if "type" in msg and msg["type"] == "WELCOME":
                        my_id = msg["id"]
                        print(f"--- JESTEM GRACZEM NR {my_id} ---")
                    else:
                        local_board = msg["board"]
                        local_locks = msg["locks"]
                except:
                    pass
        except:
            break

threading.Thread(target=receive_data, daemon=True).start()

while running:
    screen.fill(config.GREY)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            c = (x - 50) // (config.CELL_SIZE + config.MARGIN)
            r = (y - 50) // (config.CELL_SIZE + config.MARGIN)
            
            rows = len(config.SOLUTION)
            cols = len(config.SOLUTION[0])
            
            if 0 <= r < rows and 0 <= c < cols:
                if config.SOLUTION[r][c] != '.':
                    send_action("SELECT", r, c)

        if event.type == pygame.KEYDOWN:
            target_r, target_c = -1, -1
            rows = len(local_locks)
            cols = len(local_locks[0]) if rows > 0 else 0
            
            for i in range(rows):
                for j in range(cols):
                    if my_id is not None and local_locks[i][j] == my_id:
                        target_r, target_c = i, j
            
            if target_r != -1:
                if event.unicode.isalpha():
                    send_action("UPDATE", target_r, target_c, event.unicode)

    start_x, start_y = 50, 50
    rows = len(config.SOLUTION)
    cols = len(config.SOLUTION[0])

    for r in range(rows):
        for c in range(cols):
            x = start_x + c * (config.CELL_SIZE + config.MARGIN)
            y = start_y + r * (config.CELL_SIZE + config.MARGIN)
            rect = pygame.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE)
            
            color = config.WHITE
            if config.SOLUTION[r][c] == '.':
                color = config.BLACK
            else:
                if r < len(local_board) and c < len(local_board[0]):
                    val = local_board[r][c]
                    lock = local_locks[r][c]
                    
                    if val == config.SOLUTION[r][c]:
                        color = config.GREEN
                    elif my_id is not None and lock == my_id:
                        color = config.BLUE
                    elif lock is not None:
                        color = config.RED

            pygame.draw.rect(screen, color, rect)
            
            if config.SOLUTION[r][c] != '.':
                char = ""
                if r < len(local_board) and c < len(local_board[0]):
                    char = local_board[r][c]
                text = font.render(char, True, config.BLACK if color != config.BLACK else config.WHITE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()