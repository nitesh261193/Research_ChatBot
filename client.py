# client.py
import asyncio
# from contextlib import suppress
import websockets


async def client(url: str):
    async with websockets.connect(url) as websocket:
        while True:
            message = input("> ")
            await websocket.send(f'got your message', message)
            response = await websocket.recv()
            print(response)


start_server = websockets.serve(client, "localhost", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

#
# with suppress(KeyboardInterrupt):
#     # See asyncio docs for the Python 3.6 equivalent to .run().
#     asyncio.run(client("ws://localhost:8000/conversation"))
