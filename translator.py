"""
translator.py - Sends NP2 screenshot to Claude Vision API and returns translations
"""

import json
import anthropic


TRANSLATION_PROMPT = """You are a Japanese to English translator specializing in PC-98 era games and software.

You will be shown a screenshot of Neko Project II (a PC-98 emulator) or a PC-98 game running inside it.

Your job:
1. Identify ALL visible Japanese text in the screenshot (UI menus, dialogue, labels, buttons, game text, error messages — everything)
2. Translate each piece of text to natural English
3. Return your response as a JSON array ONLY — no explanation, no markdown, no extra text

Each item in the array must have:
- "japanese": the original Japanese text exactly as seen
- "english": your English translation
- "location": one of "top", "center", "bottom", "left", "right", "top-left", "top-right", "bottom-left", "bottom-right", "menu", "dialog"
- "type": one of "menu", "dialog", "button", "label", "title", "game-text", "error", "other"
- "x_percent": approximate horizontal position as percentage (0-100) from left
- "y_percent": approximate vertical position as percentage (0-100) from top

If there is no Japanese text visible, return an empty array: []

Example response format:
[
  {
    "japanese": "ファイル",
    "english": "File",
    "location": "top-left",
    "type": "menu",
    "x_percent": 5,
    "y_percent": 2
  },
  {
    "japanese": "これは剣です。",
    "english": "This is a sword.",
    "location": "bottom",
    "type": "game-text",
    "x_percent": 50,
    "y_percent": 85
  }
]

Return ONLY the JSON array. Nothing else."""


def translate_screenshot(base64_image: str, api_key: str = None) -> list:
    """
    Send a base64-encoded screenshot to Claude Vision and get translations back.
    
    Args:
        base64_image: Base64-encoded PNG screenshot
        api_key: Anthropic API key (optional, uses env var if not provided)
    
    Returns:
        List of translation dicts, or empty list on failure
    """
    try:
        client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": TRANSLATION_PROMPT
                        }
                    ],
                }
            ],
        )

        raw = message.content[0].text.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]) if lines[-1] == "```" else "\n".join(lines[1:])

        translations = json.loads(raw)

        if not isinstance(translations, list):
            print("[translator] Unexpected response format, expected a list.")
            return []

        print(f"[translator] Got {len(translations)} translations.")
        return translations

    except json.JSONDecodeError as e:
        print(f"[translator] Failed to parse JSON response: {e}")
        print(f"[translator] Raw response: {raw[:300]}...")
        return []
    except anthropic.APIError as e:
        print(f"[translator] Anthropic API error: {e}")
        return []
    except Exception as e:
        print(f"[translator] Unexpected error: {e}")
        return []


def translate_from_file(image_path: str, api_key: str = None) -> list:
    """Translate a screenshot loaded from a local file (for testing)."""
    from capture import load_image_as_base64
    b64 = load_image_as_base64(image_path)
    return translate_screenshot(b64, api_key)
