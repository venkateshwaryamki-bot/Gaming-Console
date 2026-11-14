"""Phone-as-gamepad server.

Run this on your laptop, open the printed URL on your phone (same Wi-Fi),
and every button you press on the phone becomes a real key press on the laptop.
"""

import asyncio
import json
import socket
import sys
from pathlib import Path

from aiohttp import WSMsgType, web

try:
    from pynput.keyboard import Controller, Key
except Exception as exc:  # pragma: no cover - depends on OS/display
    print(f"Could not load pynput ({exc}). Keyboard simulation is unavailable.")
    sys.exit(1)

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / "config.json").read_text())
keyboard = Controller()


def resolve_key(name: str):
    """Turn a config name like 'up', 'enter' or 'z' into a pynput key."""
    name = name.strip().lower()
    if len(name) == 1:
        return name
    special = getattr(Key, name, None)
    if special is None:
        raise ValueError(f"Unknown key name in config.json: {name!r}")
    return special


KEYMAP = {button: resolve_key(k) for button, k in CONFIG["keys"].items()}


def lan_ip() -> str:
    """Best guess at this laptop's address on the local network."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # no packet is actually sent
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


async def index(_request):
    return web.FileResponse(ROOT / "static" / "index.html")


async def websocket(request):
    ws = web.WebSocketResponse(heartbeat=10)
    await ws.prepare(request)
    held: set[str] = set()
    peer = request.remote
    print(f"Controller connected: {peer}")

    try:
        async for msg in ws:
            if msg.type != WSMsgType.TEXT:
                continue
            try:
                data = json.loads(msg.data)
                button, action = data["b"], data["t"]
            except (ValueError, KeyError, TypeError):
                continue
            key = KEYMAP.get(button)
            if key is None:
                continue
            if action == "down" and button not in held:
                keyboard.press(key)
                held.add(button)
            elif action == "up" and button in held:
                keyboard.release(key)
                held.discard(button)
    finally:
        # Never leave a key stuck down if the phone drops off Wi-Fi.
        for button in held:
            keyboard.release(KEYMAP[button])
        print(f"Controller disconnected: {peer}")
    return ws


def print_banner(url: str):
    print("\n  Phone Gamepad is running!")
    print(f"  On your phone, open:  {url}\n")
    try:
        import qrcode

        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.print_ascii(invert=True)
        print("  ...or scan the QR code above with your phone camera.\n")
    except ImportError:
        pass
    print("  Click into your game window on the laptop, then play from the phone.")
    print("  Press Ctrl+C here to stop.\n")


def main():
    port = int(CONFIG.get("port", 8080))
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", websocket)
    app.router.add_static("/static", ROOT / "static")
    print_banner(f"http://{lan_ip()}:{port}")
    web.run_app(app, host="0.0.0.0", port=port, print=None)


if __name__ == "__main__":
    main()
