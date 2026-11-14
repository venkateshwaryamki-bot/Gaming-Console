# Phone Gamepad 🎮

Turn your phone into a game controller for your laptop. No app needed: your phone
opens a web page from your laptop over Wi-Fi, and each button you tap becomes a real
key press on the laptop. It works with **any game that can be played with a keyboard**
(PC games, browser games, emulators).

```
 Phone (browser)  ──Wi-Fi / WebSocket──▶  Laptop (server.py)  ──key presses──▶  Your game
```

## Setup (one time)

1. Install [Python 3.9+](https://www.python.org/downloads/) on your laptop.
2. In this folder, run:

   ```bash
   pip install -r requirements.txt
   ```

## Easiest way (Windows)

1. On this GitHub page click the green **Code** button, then **Download ZIP**, and extract it.
2. Open the extracted folder and double-click **Start Gaming Console**.
3. Scan the QR code it shows with your phone (same Wi-Fi).

## Play

1. Make sure your phone and laptop are on the **same Wi-Fi network**.
2. On the laptop, run:

   ```bash
   python server.py
   ```

3. It prints an address like `http://192.168.1.5:8080` and a QR code. Scan it or type the address into your phone's browser.
4. Turn the phone sideways and tap **Full screen**.
5. Click into your game window on the laptop so it has focus, then play from the phone.

## Default controls

| Phone button | Laptop key |
|---|---|
| D-pad | Arrow keys (diagonals work) |
| A / B / X / Y | Z / X / A / S |
| L / R | Q / W |
| START / SELECT | Enter / Shift |

To change them, edit `config.json`. Use single letters (`"z"`) or key names such as
`up`, `space`, `enter`, `shift`, `ctrl`, `alt`, `tab`, `esc` or `f1`. For WASD games, set
`UP: "w"`, `LEFT: "a"`, `DOWN: "s"`, `RIGHT: "d"`.

## Troubleshooting

- **Phone can't open the page:** allow Python through your laptop's firewall when
  Windows asks (Private networks), and check that both devices are on the same Wi-Fi.
  Guest or office networks often block devices from talking to each other.
- **Buttons light up but the game doesn't react:** click the game window so it is focused.
  Some games run as administrator; if so, start `server.py` from an administrator terminal too.
- **macOS:** give your terminal permission under System Settings → Privacy & Security → Accessibility.
- **Linux:** works on X11. Wayland usually blocks simulated key presses.
- Several phones can connect at once (for example two players with different keys mapped).
