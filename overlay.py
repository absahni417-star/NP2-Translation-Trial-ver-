"""
overlay.py - Renders a transparent overlay with English translations over the NP2 window
"""

import tkinter as tk
from tkinter import font as tkfont


# Color scheme for overlay text boxes
TYPE_COLORS = {
    "menu":      {"bg": "#1a1a2e", "fg": "#e0e0ff"},
    "dialog":    {"bg": "#0d1b2a", "fg": "#ffffff"},
    "button":    {"bg": "#16213e", "fg": "#90caf9"},
    "label":     {"bg": "#1a1a2e", "fg": "#b0bec5"},
    "title":     {"bg": "#0f3460", "fg": "#e94560"},
    "game-text": {"bg": "#1b2838", "fg": "#c7d5e0"},
    "error":     {"bg": "#3e0000", "fg": "#ff6b6b"},
    "other":     {"bg": "#1a1a2e", "fg": "#e0e0e0"},
}

DEFAULT_COLORS = {"bg": "#1a1a2e", "fg": "#ffffff"}


class TranslationOverlay:
    """
    A transparent, click-through, always-on-top window that floats
    over the NP2 window and displays English translations.
    """

    def __init__(self):
        self.root = None
        self.canvas = None
        self.visible = False
        self.text_items = []

    def _build_window(self, x, y, width, height):
        """Create the overlay window positioned exactly over NP2."""
        self.root = tk.Tk()
        self.root.title("NP2 Translator Overlay")

        # Frameless, transparent, always on top
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#010101")  # near-black = transparent
        self.root.attributes("-alpha", 0.92)
        self.root.configure(bg="#010101")

        # Position over NP2 window
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Canvas with transparent background
        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            bg="#010101",
            highlightthickness=0
        )
        self.canvas.pack()

        # Make the window click-through on Windows
        self._set_click_through()

    def _set_click_through(self):
        """Make overlay click-through so NP2 still receives mouse events."""
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(
                hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT
            )
        except Exception as e:
            print(f"[overlay] Click-through setup failed (non-critical): {e}")

    def _clear(self):
        """Remove all text items from canvas."""
        if self.canvas:
            self.canvas.delete("all")
        self.text_items = []

    def render_translations(self, translations: list, window_rect: tuple):
        """
        Draw translation boxes on the overlay.
        
        Args:
            translations: List of translation dicts from translator.py
            window_rect: (left, top, right, bottom) of NP2 window on screen
        """
        if not translations:
            return

        left, top, right, bottom = window_rect
        win_width = right - left
        win_height = bottom - top

        self._clear()

        for item in translations:
            try:
                english = item.get("english", "")
                x_pct = float(item.get("x_percent", 50)) / 100.0
                y_pct = float(item.get("y_percent", 50)) / 100.0
                text_type = item.get("type", "other")

                colors = TYPE_COLORS.get(text_type, DEFAULT_COLORS)
                bg = colors["bg"]
                fg = colors["fg"]

                # Canvas position
                cx = int(x_pct * win_width)
                cy = int(y_pct * win_height)

                # Draw rounded rectangle background
                pad = 4
                text_id = self.canvas.create_text(
                    cx, cy,
                    text=english,
                    fill=fg,
                    font=("Segoe UI", 9, "bold"),
                    anchor="nw",
                    width=220
                )

                # Get bounding box of text to draw background behind it
                bbox = self.canvas.bbox(text_id)
                if bbox:
                    x1, y1, x2, y2 = bbox
                    rect_id = self.canvas.create_rectangle(
                        x1 - pad, y1 - pad, x2 + pad, y2 + pad,
                        fill=bg,
                        outline="#444466",
                        width=1
                    )
                    # Move rect behind text
                    self.canvas.tag_lower(rect_id, text_id)

                self.text_items.append(text_id)

            except Exception as e:
                print(f"[overlay] Error rendering item: {e}")

    def show(self, translations: list, window_rect: tuple):
        """Show the overlay with translations over the NP2 window."""
        left, top, right, bottom = window_rect
        width = right - left
        height = bottom - top

        if self.root is None:
            self._build_window(left, top, width, height)
        else:
            self.root.geometry(f"{width}x{height}+{left}+{top}")
            self.root.deiconify()

        self.render_translations(translations, window_rect)
        self.visible = True
        self.root.update()
        print(f"[overlay] Showing {len(translations)} translations.")

    def hide(self):
        """Hide the overlay without destroying it."""
        if self.root:
            self.root.withdraw()
        self.visible = False
        print("[overlay] Hidden.")

    def toggle(self, translations: list = None, window_rect: tuple = None):
        """Toggle overlay visibility."""
        if self.visible:
            self.hide()
        else:
            if translations and window_rect:
                self.show(translations, window_rect)

    def destroy(self):
        """Fully destroy the overlay window."""
        if self.root:
            self.root.destroy()
            self.root = None
        self.visible = False

    def update(self):
        """Process tkinter events (call in main loop)."""
        if self.root:
            try:
                self.root.update()
            except tk.TclError:
                pass
