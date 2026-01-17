import socket
import threading
import json
import config

BOARD = [['' for _ in range(config.GRID_SIZE)] for _ in range(config.GRID_SIZE)]
LOCKS = [[None for _ in range(config.GRID_SIZE)] for _ in range(config.GRID_SIZE)]

clients = []
game_lock = threading.Lock()

def send_json(conn, data):
    try:
        msg = json.dumps(data) + "\n"
        conn.sendall(msg.encode('utf-8'))
    except:
        pass

def broadcast():
    state = {"board": BOARD, "locks": LOCKS}
    for client in clients:
        send_json(client, state)

def handle_client(conn, addr, player_id):
    print(f"[NOWY] Gracz {player_id} połączony.")
    
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
                        if action == "SELECT":
                            for i in range(len(LOCKS)):
                                for j in range(len(LOCKS[0])):
                                    if LOCKS[i][j] == player_id:
                                        LOCKS[i][j] = None
                            if LOCKS[r][c] is None:
                                LOCKS[r][c] = player_id

                        elif action == "UPDATE":
                            char = data_json.get("char").upper()
                            if LOCKS[r][c] == player_id:
                                BOARD[r][c] = char
                    
                    broadcast()
                except json.JSONDecodeError:
                    pass

        except Exception as e:
            print(f"Błąd: {e}")
            connected = False

    conn.close()
    if conn in clients: clients.remove(conn)
    with game_lock:
        for i in range(len(LOCKS)):
            for j in range(len(LOCKS[0])):
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