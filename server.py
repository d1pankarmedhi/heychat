import asyncio

import websockets

connected_clients = set()  # track clients


async def handler(websocket):
    print("Handler function called for a new connection")
    connected_clients.add(websocket)  # Add new client to the set
    print(f"Client connected. Total clients: {len(connected_clients)}")
    try:
        name = await websocket.recv()  # Receive name from client
        print(f"Client identified as: {name}")
        await broadcast_message(f"{name} joined the chat.", websocket)  # Notify others

        async for message in websocket:
            print(f"Server handler received message: {message} from {name}")
            await broadcast_message(
                f"{name}: {message}", websocket
            )  # Broadcast message
            print("Broadcast message call completed in handler")
    except websockets.ConnectionClosed:
        print(f"Client {websocket} closed the connection.")
    except Exception as e:
        print(f"Error during message receiving: {e}")
    finally:
        connected_clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(connected_clients)}")


async def broadcast_message(message, sender_websocket):
    print(
        f"Broadcast message function called with message: {message}, sender: {sender_websocket}"
    )
    for client in connected_clients:
        print(
            f"  Broadcasting loop - current client: {client}, sender_websocket: {sender_websocket}"
        )
        if client != sender_websocket:  # Don't send to sender
            print(f"  Condition client != sender_websocket is TRUE")
            try:
                await client.send(message)
                print(f"  Successfully sent message to client: {client}")
            except websockets.ConnectionClosed:
                print(f"  Error sending to a closed client connection.")
            except Exception as e:
                print(f"  Error sending message to client: {e}")
        else:
            print(f"  Condition client != sender_websocket is FALSE - skipping sender")


async def main():
    try:
        async with websockets.serve(handler, "localhost", 8765):
            print("Server started on ws://localhost:8765")
            await asyncio.Future()
    except KeyboardInterrupt:
        print("\nServer stopped manually.")


if __name__ == "__main__":
    asyncio.run(main())
