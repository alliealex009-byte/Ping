"""Opens the Space page in a real headless Chromium (like a person visiting), stays a while, scrolls and clicks.
Env: SPACE_ID (youruser/group-manager). Optional: SPACE_URL (direct https://xxx.hf.space address)."""
import os
import random
import sys
from playwright.sync_api import sync_playwright

SPACE = os.environ["SPACE_ID"].strip()
PAGE = f"https://huggingface.co/spaces/{SPACE}"
DIRECT = os.environ.get("SPACE_URL", "").strip()
UA = ("Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Mobile Safari/537.36")

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(user_agent=UA, viewport={"width": 412, "height": 915}, locale="en-IN", timezone_id="Asia/Kolkata")
    page = ctx.new_page()
    for url in [PAGE] + ([DIRECT] if DIRECT else []):
        try:
            page.goto(url, wait_until="networkidle", timeout=90000)
        except Exception as e:
            print(f"load warning for {url}: {e}")
        page.wait_for_timeout(random.randint(8000, 15000))
        for _ in range(3):
            page.mouse.wheel(0, random.randint(200, 600))
            page.wait_for_timeout(random.randint(1500, 3500))
        # if Hugging Face shows its "Restart this Space" button, press it
        for label in ("Restart this Space", "Restart Space", "Wake up", "Factory reboot"):
            try:
                btn = page.get_by_role("button", name=label)
                if btn.count() and label != "Factory reboot":
                    btn.first.click(timeout=5000)
                    print(f"clicked: {label}")
                    page.wait_for_timeout(5000)
            except Exception:
                pass
        print(f"visited {url}: title = {page.title()!r}")
    b.close()
sys.exit(0)
