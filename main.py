"""
main.py - NP2 Translator
Press F1 to translate the current NP2 window. Press F1 again to hide.
Press F2 to force a fresh translation even if overlay is visible.
Press ESC or close the tray icon to quit.
"""

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Optional: keyboard hotkey support
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("[main] 'keyboard' module not found. Hotkeys disabled. Use GUI buttons instead.")

from capture import capture_np2_as_base64, find_np2_window
from translator import translate_screenshot
from overlay import TranslationOverlay
from config import load_config


class NP2Translator:
    def __init__(self):
        self.config = load_config()
        self.overlay = TranslationOverlay()
        self.last_translations = []
        self.last_rect = None
        self.is_translating = False
        self.running = True

        # GUI control panel
        self.gui = None
        self._build_control_panel()

    def _build_control_panel(self):
        """Build a small always-on-top control panel."""
        self.gui = tk.Tk()
        self.gui.title("NP2 Translator")
        self.gui.attributes("-topmost", True)
        self.gui.resizable(False, False)
        self.gui.geometry("300x200")
        self.gui.configure(bg="#0d1117")

        # Title
        tk.Label(
            self.gui,
            text="NP2 Translator",
            bg="#0d1117",
            fg="#58a6ff",
            font=("Segoe UI", 13, "bold")
        ).pack(pady=(16, 4))

        tk.Label(
            self.gui,
            text="Japanese → English Overlay",
            bg="#0d1117",
            fg="#8b949e",
            font=("Segoe UI", 9)
        ).pack()

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(
            self.gui,
            textvariable=self.status_var,
            bg="#0d1117",
            fg="#3fb950",
            font=("Segoe UI", 9, "italic")
        ).pack(pady=6)

        # Buttons frame
        btn_frame = tk.Frame(self.gui, bg="#0d1117")
        btn_frame.pack(pady=8)

        self.translate_btn = tk.Button(
            btn_frame,
            text="Translate  [F1]",
            command=self.on_translate_toggle,
            bg="#238636",
            fg="white",
            activebackground="#2ea043",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2"
        )
        self.translate_btn.grid(row=0, column=0, padx=6)

        tk.Button(
            btn_frame,
            text="Refresh  [F2]",
            command=self.on_retranslate,
            bg="#1f6feb",
            fg="white",
            activebackground="#388bfd",
            activeforeground="white",
            font=("Segoe UI", 9),
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2"
        ).grid(row=0, column=1, padx=6)

        tk.Button(
            self.gui,
            text="Quit",
            command=self.quit,
            bg="#21262d",
            fg="#8b949e",
            activebackground="#30363d",
            font=("Segoe UI", 8),
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2"
        ).pack(pady=(4, 0))

        self.gui.protocol("WM_DELETE_WINDOW", self.quit)

        # Register hotkeys
        if KEYBOARD_AVAILABLE:
            keyboard.add_hotkey("f1", self.on_translate_toggle)
            keyboard.add_hotkey("f2", self.on_retranslate)
            keyboard.add_hotkey("esc", self.quit)
            print("[main] Hotkeys registered: F1=Toggle, F2=Refresh, ESC=Quit")

    def set_status(self, msg: str, color: str = "#3fb950"):
        self.status_var.set(msg)
        # find label and update color
        for widget in self.gui.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("textvariable") == str(self.status_var):
                widget.configure(fg=color)
        self.gui.update_idletasks()

    def on_translate_toggle(self):
        """F1: toggle overlay on/off. If off and no translation yet, translate first."""
        if self.overlay.visible:
            self.overlay.hide()
            self.set_status("Overlay hidden", "#8b949e")
            self.translate_btn.configure(text="Translate  [F1]", bg="#238636")
        else:
            if self.last_translations and self.last_rect:
                # Re-show existing translation instantly
                self.overlay.show(self.last_translations, self.last_rect)
                self.set_status(f"{len(self.last_translations)} translations shown", "#3fb950")
                self.translate_btn.configure(text="Hide  [F1]", bg="#da3633")
            else:
                # First time — need to translate
                self._run_translation()

    def on_retranslate(self):
        """F2: force a fresh translation."""
        self.last_translations = []
        self.last_rect = None
        if self.overlay.visible:
            self.overlay.hide()
        self._run_translation()

    def _run_translation(self):
        """Run translation in a background thread to keep UI responsive."""
        if self.is_translating:
            self.set_status("Already translating...", "#e3b341")
            return

        def worker():
            self.is_translating = True
            self.set_status("Capturing window...", "#e3b341")

            api_key = self.config.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                self.set_status("No API key set!", "#f85149")
                self.is_translating = False
                return

            b64, rect = capture_np2_as_base64()
            if b64 is None:
                self.set_status("NP2 window not found!", "#f85149")
                self.is_translating = False
                return

            self.set_status("Translating...", "#e3b341")
            translations = translate_screenshot(b64, api_key)

            if not translations:
                self.set_status("No Japanese text found", "#8b949e")
                self.is_translating = False
                return

            self.last_translations = translations
            self.last_rect = rect

            self.overlay.show(translations, rect)
            self.set_status(f"{len(translations)} items translated ✓", "#3fb950")
            self.translate_btn.configure(text="Hide  [F1]", bg="#da3633")
            self.is_translating = False

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def run(self):
        """Main loop."""
        print("[main] NP2 Translator running. Press F1 to translate.")
        while self.running:
            try:
                self.gui.update()
                self.overlay.update()
                time.sleep(0.033)  # ~30fps GUI refresh
            except tk.TclError:
                break

    def quit(self):
        print("[main] Shutting down.")
        self.running = False
        self.overlay.destroy()
        if KEYBOARD_AVAILABLE:
            keyboard.unhook_all()
        try:
            self.gui.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    app = NP2Translator()
    app.run()
