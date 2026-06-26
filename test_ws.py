import asyncio
import websockets

async def test_ws():
    uri = 'ws://localhost:8000/api/ws/live-chat'
    try:
        async with websockets.connect(uri) as ws:
            print('Connected')
            while True:
                msg = await ws.recv()
                print(f'Received: {msg[:100]}')
    except Exception as e:
        print(f'Error: {e}')

asyncio.run(test_ws())
