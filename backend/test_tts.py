import os
import json
import urllib.request
import base64

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('GEMINI_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
    except:
        pass

if not api_key:
    print('No API key')
    exit(1)

# Test TTS via REST API
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={api_key}'

payload = {
    "contents": [{"parts": [{"text": "Hello! Welcome to the discovery chat."}]}],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
            "voiceConfig": {
                "prebuiltVoiceConfig": {
                    "voiceName": "Kore"
                }
            }
        }
    }
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        candidates = result.get('candidates', [])
        if candidates:
            parts = candidates[0].get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    audio_data = part['inlineData']['data']
                    mime = part['inlineData'].get('mimeType', 'unknown')
                    print(f"SUCCESS! Got audio: {mime}, {len(audio_data)} base64 chars")
                    # Save a sample to test
                    raw = base64.b64decode(audio_data)
                    print(f"Decoded size: {len(raw)} bytes")
                    break
            else:
                print("No audio data in response parts")
                print(json.dumps(result, indent=2)[:500])
        else:
            print("No candidates in response")
            print(json.dumps(result, indent=2)[:500])
except Exception as e:
    print(f"Error: {e}")
