import asyncio

import websockets


async def receive_messages(websocket, queue):
    while True:
        try:
            message = await websocket.recv()
            print(f"<<< {message}")  # Display received messages
            await queue.put(message)  # Put received message into the queue
        except websockets.ConnectionClosed:
            break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


async def send_messages(websocket, queue):
    name = input("What's your name? ")
    await websocket.send(name)
    print(f">>> {name}")

    while True:
        message = await asyncio.to_thread(
            input, "Enter message: "
        )  # avoid blocking async loop
        await websocket.send(message)
        print(f">>> {message}")

        # print message from queue
        if not queue.empty():
            received_message = await queue.get()
            print(f"<<< {received_message}")

        await asyncio.sleep(0.1)  # delay to yield to the receiver


async def main():
    uri = "ws://localhost:8765"
    queue = asyncio.Queue()  # Queue for managing messages

    async with websockets.connect(uri) as websocket:
        receive_task = asyncio.create_task(
            receive_messages(websocket, queue)
        )  # Start receiver task

        send_task = asyncio.create_task(
            send_messages(websocket, queue)
        )  # Start sender task

        await asyncio.gather(receive_task, send_task)  # Run both tasks concurrently


if __name__ == "__main__":
    asyncio.run(main())
