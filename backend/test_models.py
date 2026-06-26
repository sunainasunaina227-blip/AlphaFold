import os
import json
import urllib.request
import sys

# Fix encoding for Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

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

for version in ['v1beta', 'v1alpha']:
    url = f'https://generativelanguage.googleapis.com/{version}/models?key={api_key}'
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            models = data.get('models', [])

            print(f"\n=== {version} === (Total: {len(models)})")
            
            # Show ALL model names
            print("\nAll models:")
            for m in models:
                name = m.get('name', '')
                methods = m.get('supportedGenerationMethods', [])
                has_bidi = 'bidiGenerateContent' in methods
                marker = ' ** BIDI **' if has_bidi else ''
                live_marker = ' [LIVE/AUDIO]' if ('live' in name or 'native-audio' in name) else ''
                print(f"  {name}{live_marker}{marker}  -> {methods}")

    except Exception as e:
        print(f"\n=== {version} === Error: {e}")
