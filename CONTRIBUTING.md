# Contributing to NP2 Translator

First off — thank you for taking the time to contribute! This project exists to make PC-98 games accessible to non-Japanese speakers, and every contribution helps.

---

## Ways to Contribute

### 🐛 Bug Reports
Open an issue with:
- Your Windows version
- Python version (`python --version`)
- The NP2 version you are using
- What you expected vs what happened
- Any error messages from the terminal

### 💡 Feature Ideas
Open an issue tagged `enhancement`. Good ideas for this project:
- Translation history panel
- Per-game font size tuning
- Support for NP2kai fork
- Configurable hotkeys via GUI
- Overlay position fine-tuning
- Packaging as a standalone `.exe` (PyInstaller)

### 🌐 Translation Prompt Improvements
The heart of the tool is the prompt in `translator.py`. If you speak Japanese and notice mistranslations or missing context (especially for specific game genres like RPGs or visual novels), improving the prompt is hugely valuable. Open a PR with your changes and explain what it improves.

### 🛠️ Code Contributions

#### Setup
```bash
git clone https://github.com/YOUR_USERNAME/np2-translator.git
cd np2-translator

# Copy the example config and add your API key
copy config.example.json config.json
# Edit config.json and add your Anthropic API key

# Install dependencies
pip install -r requirements.txt
```

#### Project Structure
```
np2-translator/
├── main.py           # Entry point + control panel GUI
├── capture.py        # Screenshots the NP2 window
├── translator.py     # Claude Vision API integration
├── overlay.py        # Transparent overlay renderer
├── config.py         # Config loader/saver
├── config.example.json  # Safe template (no real keys)
└── launch.bat        # Windows one-click launcher
```

#### Pull Request Guidelines
- Keep PRs focused — one feature or fix per PR
- Test on a real NP2 window before submitting
- Don't commit `config.json` (it's in `.gitignore` for a reason — API keys!)
- Add a short description of what changed and why

---

## Code Style
- Python 3.8+ compatible
- Keep dependencies minimal — this tool should be easy to install
- Print `[module]` prefixed messages for debugging (e.g. `[capture] Window found`)
- Prefer simple and readable over clever

---

## Questions?
Open an issue tagged `question` — no question is too small.
