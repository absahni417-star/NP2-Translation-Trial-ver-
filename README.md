# NP2 Translator
### Japanese → English Overlay for Neko Project II

A lightweight tool that translates any Japanese text visible in the Neko Project II emulator window — including both the emulator's own UI **and** the PC-98 games running inside it — using Claude Vision AI.

---

## How It Works

```
Press F1
  → Captures a screenshot of the NP2 window
  → Sends it to Claude Vision API
  → Claude reads all Japanese text in context
  → English translations appear as an overlay on top of NP2
Press F1 again → overlay disappears
```

No continuous monitoring. No performance drain. Translate on demand.

---

## Setup

### 1. Requirements
- Windows 10 or 11
- Python 3.8+
- Neko Project II (NP2) installed and running

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Your Anthropic API Key
Open `config.json` and add your key:
```json
{
  "api_key": "sk-ant-api03-..."
}
```
Or set it as an environment variable:
```bash
set ANTHROPIC_API_KEY=sk-ant-api03-...
```
Get an API key at: https://console.anthropic.com

### 4. Run
Double-click `launch.bat`  
**or** run from terminal:
```bash
python main.py
```

---

## Usage

1. Launch **Neko Project II** and load your game
2. Launch **NP2 Translator** (`launch.bat`)
3. When you need to read Japanese text — press **F1**
4. An English overlay appears on top of the NP2 window
5. Press **F1** again to hide the overlay and keep playing
6. Press **F2** to force a fresh translation (e.g. after a scene change)

---

## Hotkeys

| Key | Action |
|-----|--------|
| `F1` | Toggle overlay on / off |
| `F2` | Force fresh translation |
| `ESC` | Quit the translator |

---

## Project Structure

```
np2-translator/
├── main.py           # Entry point + control panel GUI
├── capture.py        # Screenshots the NP2 window
├── translator.py     # Sends to Claude Vision API
├── overlay.py        # Transparent overlay renderer
├── config.py         # Config loader
├── config.json       # Your settings and API key
├── requirements.txt  # Python dependencies
└── launch.bat        # Windows launcher
```

---

## Notes

- Requires an **Anthropic API key** (Claude claude-sonnet-4-6)
- Works with **any PC-98 game** — no game-specific configuration needed
- The overlay is **click-through** — mouse clicks pass through to NP2
- Translation quality depends on text clarity in the screenshot
- Each F1 press that triggers a new translation makes one API call

---

## Troubleshooting

**"NP2 window not found"**  
Make sure Neko Project II is running before pressing F1. The tool searches for windows with "Neko Project" or "NP2" in the title.

**"No API key set"**  
Add your key to `config.json` or set `ANTHROPIC_API_KEY` environment variable.

**Overlay not appearing**  
Try pressing F2 to force a fresh capture. Make sure NP2 is not minimized.

**Text boxes in wrong position**  
Claude estimates text positions from the screenshot. Accuracy improves with cleaner, less cluttered screens.
