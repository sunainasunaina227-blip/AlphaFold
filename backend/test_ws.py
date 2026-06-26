import asyncio
import websockets
import json
import os

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('GEMINI_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
    except:
        pass

async def test():
    # Try v1alpha and v1beta
    for version in ['v1alpha', 'v1beta']:
        for model in ['models/gemini-2.0-flash', 'models/gemini-2.0-flash-exp']:
            url = f'wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.{version}.GenerativeService.BidiGenerateContent?key={api_key}'
            print(f"\\nTesting {model} on {version}...")
            try:
                async with websockets.connect(url) as ws:
                    setup_message = {
                        'setup': {
                            'model': model,
                            'generationConfig': {
                                'responseModalities': ['AUDIO', 'TEXT']
                            }
                        }
                    }
                    await ws.send(json.dumps(setup_message))
                    response = await ws.recv()
                    print('SUCCESS! Response:', response)
                    return
            except Exception as e:
                print('Error:', e)

asyncio.run(test())
