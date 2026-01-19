import socket
import threading
import json
import config

current_level_index = 0
game_active = False
game_finished = False

current_grid = config.LEVELS[0]['grid']
BOARD = [['' for _ in range(10)] for _ in range(10)]
LOCKS = [[None for _ in range(10)] for _ in range(10)]

clients = []
game_lock = threading.Lock()

def load_level(index):
    global current_level_index, current_grid, BOARD, LOCKS, game_finished
    if index < len(config.LEVELS):
        current_level_index = index
        current_grid = config.LEVELS[index]['grid']
        BOARD = [['' for _ in range(10)] for _ in range(10)]
        LOCKS = [[None for _ in range(10)] for _ in range(10)]
        game_finished = False
        return True
    return False

def check_win():
    global game_finished
    for r in range(10):
        for c in range(10):
            target = current_grid[r][c]
            if target != '.' and BOARD[r][c] != target:
                return False
    game_finished = True
    return True

def send_json(conn, data):
    try:
        msg = json.dumps(data) + "\n"
        conn.sendall(msg.encode('utf-8'))
    except: pass

def broadcast():
    state = {
        "board": BOARD,
        "locks": LOCKS,
        "level_index": current_level_index,
        "active": game_active,
        "finished": game_finished
    }
    for client in clients:
        send_json(client, state)

def handle_client(conn, addr, player_id):
    global game_active
    print(f"[NOWY] Gracz {player_id}")
    send_json(conn, {"type": "WELCOME", "id": player_id})
    broadcast()

    connected = True
    buffer = ""
    while connected:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data: break
            buffer += data
            while "\n" in buffer:
                msg_str, buffer = buffer.split("\n", 1)
                if not msg_str: continue
                try:
                    data_json = json.loads(msg_str)
                    action = data_json.get("action")
                    r = data_json.get("r")
                    c = data_json.get("c")

                    with game_lock:
                        if action == "START_GAME":
                            game_active = True
                            load_level(0)

                        elif action == "NEXT_LEVEL":
                            if not load_level(current_level_index + 1):
                                game_active = False

                        elif game_active and not game_finished:
                            is_solved = (current_grid[r][c] != '.' and BOARD[r][c] == current_grid[r][c])

                            if action == "SELECT":
                                if not is_solved:
                                    for i in range(10):
                                        for j in range(10):
                                            if LOCKS[i][j] == player_id: LOCKS[i][j] = None
                                    if LOCKS[r][c] is None:
                                        LOCKS[r][c] = player_id

                            elif action == "UPDATE":
                                if not is_solved:
                                    char = data_json.get("char").upper()
                                    if LOCKS[r][c] == player_id:
                                        BOARD[r][c] = char
                                        check_win()
                    
                    broadcast()
                except json.JSONDecodeError: pass
        except: break

    conn.close()
    if conn in clients: clients.remove(conn)
    with game_lock:
        for i in range(10):
            for j in range(10):
                if LOCKS[i][j] == player_id: LOCKS[i][j] = None
    broadcast()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((config.HOST, config.PORT))
    server.listen()
    print("SERWER DZIAŁA...")
    id_counter = 0
    while True:
        conn, addr = server.accept()
        id_counter += 1
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr, id_counter)).start()

if __name__ == "__main__":
    start_server()