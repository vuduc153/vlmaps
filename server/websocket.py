import asyncio
import websockets

# Store connected clients
client_a = None
client_b = None

async def handler(websocket, path):
    global client_a, client_b
    
    try:
        if client_a is None:
            client_a = websocket
        elif client_b is None:
            client_b = websocket
        else:
            await websocket.close()
            return

        async for message in websocket:
            if websocket == client_a and client_b is not None:
                print(f"Client A sent: {message}")
                await client_b.send(message)
            elif websocket == client_b and client_a is not None:
                print(f"Client B sent: {message}")
                await client_a.send(message)

    except websockets.ConnectionClosed:
        print(f"Client disconnected")
    
    finally:
        # Clean up when a client disconnects
        if websocket == client_a:
            print("Client A disconnected")
            client_a = None
        elif websocket == client_b:
            print("Client B disconnected")
            client_b = None

async def main():
    async with websockets.serve(handler, "localhost", 43000):
        await asyncio.Future()

asyncio.run(main())