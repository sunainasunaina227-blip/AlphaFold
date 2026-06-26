import asyncio
import json
import websockets
import os
import sys

# add backend dir to sys path so we can import config
sys.path.append(r"d:\Web development\Projects\AlphaFold\auxilab-agent-ap-discovery\backend")
import config

async def test():
    api_key = config.GEMINI_LIVE_API_KEY
    url = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key={api_key}"
    
    async with websockets.connect(url) as gemini_ws:
        setup_msg = {
            "setup": {
                "model": "models/gemini-2.0-flash-exp",
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                },
                "inputAudioTranscription": {
                    "language": "en-US"
                }
            }
        }
        await gemini_ws.send(json.dumps(setup_msg))
        raw = await asyncio.wait_for(gemini_ws.recv(), timeout=10)
        print("Response 1:", raw)

asyncio.run(test())
