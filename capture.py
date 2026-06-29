"""
capture.py - Captures screenshot of the NP2 window on Windows
"""

import os
import io
import base64
from PIL import ImageGrab, Image

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


def find_np2_window():
    """Find the NP2 window handle by searching for known window titles."""
    np2_titles = [
        "Neko Project II",
        "Neko Project 2",
        "NP2",
        "NekoProject",
        "PC-9801",
        "PC98",
    ]

    found_hwnd = None

    if not WIN32_AVAILABLE:
        print("[capture] win32gui not available. Running in demo mode.")
        return None

    def enum_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            for np2_title in np2_titles:
                if np2_title.lower() in title.lower():
                    results.append((hwnd, title))

    results = []
    win32gui.EnumWindows(enum_callback, results)

    if results:
        hwnd, title = results[0]
        print(f"[capture] Found NP2 window: '{title}' (hwnd={hwnd})")
        return hwnd

    print("[capture] NP2 window not found. Is Neko Project II running?")
    return None


def get_window_rect(hwnd):
    """Get the bounding rectangle of a window."""
    if not WIN32_AVAILABLE or hwnd is None:
        return None
    try:
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        if right - left <= 0 or bottom - top <= 0:
            print("[capture] Window has zero size.")
            return None
        return rect
    except Exception as e:
        print(f"[capture] Error getting window rect: {e}")
        return None


def bring_window_to_front(hwnd):
    """Bring the NP2 window to the foreground before capturing."""
    if not WIN32_AVAILABLE or hwnd is None:
        return
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        pass


def capture_window(hwnd=None):
    """
    Capture a screenshot of the NP2 window.
    Returns a PIL Image or None on failure.
    """
    if hwnd is None:
        hwnd = find_np2_window()

    if hwnd is None:
        print("[capture] No NP2 window found to capture.")
        return None

    rect = get_window_rect(hwnd)
    if rect is None:
        return None

    bring_window_to_front(hwnd)

    try:
        left, top, right, bottom = rect
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        print(f"[capture] Screenshot taken: {screenshot.size[0]}x{screenshot.size[1]}px")
        return screenshot
    except Exception as e:
        print(f"[capture] Screenshot failed: {e}")
        return None


def image_to_base64(image: Image.Image) -> str:
    """Convert a PIL Image to a base64-encoded PNG string."""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def capture_np2_as_base64(hwnd=None):
    """
    Full pipeline: find NP2 window → capture → return base64 string.
    Returns (base64_string, window_rect) or (None, None) on failure.
    """
    if hwnd is None:
        hwnd = find_np2_window()

    image = capture_window(hwnd)
    if image is None:
        return None, None

    rect = get_window_rect(hwnd)
    b64 = image_to_base64(image)
    return b64, rect


def load_image_as_base64(path: str) -> str:
    """Load a local image file and return as base64 (for testing)."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
