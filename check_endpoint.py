import urllib.request
import json

try:
    req = urllib.request.Request("http://localhost:8000/health")
    with urllib.request.urlopen(req) as response:
        print("Health:", response.read().decode())
except Exception as e:
    print("Health error:", e)

# Test the docs page
try:
    req = urllib.request.Request("http://localhost:8000/openapi.json")
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        paths = data.get("paths", {})
        if "/voice-chat" in paths:
            print("SUCCESS: /voice-chat is registered in the API!")
        else:
            print("ERROR: /voice-chat NOT found in the API.")
except Exception as e:
    print("OpenAPI error:", e)
