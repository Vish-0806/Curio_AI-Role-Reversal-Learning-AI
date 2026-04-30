import urllib.request
import json
import traceback

out = []
try:
    req = urllib.request.Request("http://127.0.0.1:8000/health", method="GET")
    with urllib.request.urlopen(req, timeout=2) as response:
        out.append("Health: " + response.read().decode())
except Exception as e:
    out.append("Health error: " + str(e))
    out.append(traceback.format_exc())

with open("test_result.txt", "w") as f:
    f.write("\n".join(out))
