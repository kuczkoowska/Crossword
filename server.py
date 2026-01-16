import asyncio
import websockets
import json

CONNECTED_CLIENTS = set()

async def handler(websocket):
    print("[SERWER] Nowy gracz dołączył!")
    CONNECTED_CLIENTS.add(websocket)
    
    try:
        async for message in websocket:
            print(f"[SERWER] Otrzymano wiadomość: {message}")
            
            response = {"status": "ok", "msg": "Serwer cię słyszy!"}
            await websocket.send(json.dumps(response))
            
    except websockets.exceptions.ConnectionClosedOK:
        pass
    finally:
        CONNECTED_CLIENTS.remove(websocket)
        print("[SERWER] Gracz rozłączony.")

async def main():
    async with websockets.serve(handler, "localhost", 8001):
        print("SERWER KRZYŻÓWKI RUSZYŁ (ws://localhost:8001)")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSerwer zatrzymany.")