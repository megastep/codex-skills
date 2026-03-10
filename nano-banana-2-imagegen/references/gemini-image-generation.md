# Gemini Image Generation Notes

Use this reference when the task needs current model or request-shape details.

## Current doc summary

- The Google AI image generation guide describes:
  - `gemini-3.1-flash-image-preview` as Nano Banana 2.
  - `gemini-3-pro-image-preview` as Nano Banana Pro.
- The official Python library is `google-genai`.
- Google recommends using the Google GenAI SDK rather than legacy libraries.
- Quickstart install for Python is `pip install -U google-genai`.
- The image generation guide's Python examples use:
  - `from google import genai`
  - `from PIL import Image`
  - `client = genai.Client()`
  - `client.models.generate_content(...)`

## SDK usage

Install dependencies:

```bash
pip install -U google-genai pillow
```

Generate from text:

```python
from google import genai

client = genai.Client(api_key="...")
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=["Create a studio product shot of a matte-black espresso grinder"],
)
```

Edit from text plus image:

```python
from google import genai
from PIL import Image

client = genai.Client(api_key="...")
source = Image.open("/path/to/source.png")
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=["Turn this into a clean magazine-style cover shot", source],
)
```

Read response parts by checking `part.text` and `part.as_image()`.

## Multi-turn editing

The image generation guide recommends chat / multi-turn conversation when iterating on images. That is more appropriate when the task needs multiple successive edits or back-and-forth refinement. The bundled script supports that by storing and restoring serialized chat history.

The official Python pattern is chat-based:

```python
from google import genai

client = genai.Client(api_key="...")
chat = client.chats.create(model="gemini-3.1-flash-image-preview")
first = chat.send_message(["Create a glossy app icon from this sketch", source_image])
second = chat.send_message("Keep the same icon, but make the background cobalt blue")
history = chat.get_history()
```

For CLI persistence across separate invocations, serialize `chat.get_history()` with:

```python
[item.model_dump(mode="json", exclude_none=True) for item in history]
```

That form encodes inline image bytes as base64 strings and can be restored later with:

```python
from google.genai import types

history = [types.Content.model_validate(item) for item in serialized_history]
chat = client.chats.create(model="gemini-3.1-flash-image-preview", history=history)
```

## API key loading guidance for this skill

The bundled script resolves credentials in this order:

1. `--api-key`
2. `GEMINI_API_KEY`
3. `GOOGLE_API_KEY`
4. `--api-key-file`
5. `GEMINI_API_KEY_FILE`
6. `GOOGLE_API_KEY_FILE`

Key files may contain either:

- A raw key by itself
- `.env`-style lines such as `GEMINI_API_KEY=...`
- `.env`-style lines such as `GOOGLE_API_KEY=...`

## Sources

- https://ai.google.dev/gemini-api/docs/image-generation
- https://ai.google.dev/gemini-api/docs/quickstart
