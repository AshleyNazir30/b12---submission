import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone
import os

SIGNING_SECRET = b"hello-there-from-b12"
URL = "https://b12.io/apply/submission"

payload = {
    "name": "Your name",
    "email": "you@example.com",
    "resume_link": "https://your-resume-link",
    "repository_link": "https://github.com/YOUR_USERNAME/b12-submission",
    "action_run_link": os.getenv("ACTION_RUN_LINK"),
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
}

body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

digest = hmac.new(SIGNING_SECRET, body, hashlib.sha256).hexdigest()
signature = f"sha256={digest}"

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "X-Signature-256": signature
}

response = requests.post(URL, data=body, headers=headers)

print(response.status_code)
print(response.text)
