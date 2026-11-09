"""Wakes a sleeping / crashed Hugging Face Space through the Hugging Face API.
Needs two environment variables: HF_TOKEN (a token with WRITE access) and SPACE_ID (e.g. youruser/group-manager)."""
import json
import os
import sys
import urllib.request

SPACE = os.environ["nexapayz99/group-manager"].strip()
TOKEN = os.environ["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"].strip()
RESTART_WHEN = {"SLEEPING", "RUNTIME_ERROR", "STOPPED"}


def call(method, path):
    req = urllib.request.Request(f"https://huggingface.co/api/spaces/{SPACE}{path}", method=method,
                                 headers={"Authorization": f"Bearer {TOKEN}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read()
        return json.loads(body) if body else {}


stage = call("GET", "/runtime").get("stage", "UNKNOWN")
print(f"Space {SPACE}: stage = {stage}")
if stage in RESTART_WHEN:
    call("POST", "/restart")
    print("Restart requested - the Space is waking up.")
else:
    print("Nothing to do.")
sys.exit(0)
