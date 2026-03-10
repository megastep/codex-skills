---
name: nano-banana-2-imagegen
description: Generate and edit images with Google's Nano Banana 2 model through the official Python Google GenAI SDK. Use when a user asks to create an image, edit an existing image, restyle a photo, add or remove visual elements, create concept art, mockups, infographics, or product shots with Gemini / Nano Banana, especially when the result should be saved locally and the API key may come from the environment or a file.
---

# Nano Banana 2 Imagegen

## Overview

Use the bundled Python script to turn a prompt into one or more saved image files through Google's official `google-genai` SDK. Require `google-genai` and `Pillow` for this skill, and prefer the bundled script over ad-hoc snippets so API key loading, image editing inputs, and output handling stay consistent.

## Requirements

Install the required Python packages before using this skill:

```bash
pip install -U google-genai pillow
```

## Quick Start

Run the bundled script:

```bash
python nano-banana-2-imagegen/scripts/generate_image.py \
  "Create a cinematic product photo of a brass fountain pen on dark slate" \
  --output /tmp/fountain-pen.png
```

Edit an existing image:

```bash
python nano-banana-2-imagegen/scripts/generate_image.py \
  "Turn this sneaker photo into a clean studio ad with a pale blue backdrop" \
  --input-image /tmp/sneaker.jpg \
  --output /tmp/sneaker-ad.png
```

Load a prompt from a file and apply post-processing:

```bash
python nano-banana-2-imagegen/scripts/generate_image.py \
  --prompt-file /tmp/prompt.txt \
  --api-key-file ~/.config/gemini/api-key \
  --resize 1536x1024 \
  --crop 128,0,1408,1024 \
  --output /tmp/generated.png
```

Continue a multi-turn edit across separate invocations:

```bash
python nano-banana-2-imagegen/scripts/generate_image.py \
  "Create a glossy app icon from this sketch" \
  --input-image /tmp/sketch.png \
  --state-file /tmp/icon-chat.json \
  --output /tmp/icon-v1.png

python nano-banana-2-imagegen/scripts/generate_image.py \
  "Keep the icon shape, but make the background cobalt blue and add a soft shadow" \
  --state-file /tmp/icon-chat.json \
  --output /tmp/icon-v2.png
```

## Workflow

1. Resolve the prompt from CLI text or `--prompt-file`.
2. Resolve the API key from explicit value, environment, or key file.
3. Optionally load one or more input images with Pillow for edit requests.
4. Call Gemini through the Google GenAI SDK with `gemini-3.1-flash-image-preview` by default.
5. If `--state-file` is set, create or resume a persistent SDK chat for multi-turn editing.
6. Optionally apply Pillow post-processing such as crop or resize.
7. Save returned image parts to the requested output path.
8. Save updated chat history back to the state file when multi-turn mode is enabled.
9. Print any model text plus the saved file paths.

## Arguments

- `--input-image`: Provide one or more images for image-to-image editing.
- `--output`: Destination file path. If the model returns multiple images, the script appends `-2`, `-3`, and so on.
- `--state-file`: Persist full Gemini chat history to JSON so later invocations can continue the same edit conversation.
- `--reset-state`: Ignore any existing state file and start a fresh chat.
- `--model`: Override the model id. Default is `gemini-3.1-flash-image-preview`.
- `--api-key`: Pass the API key directly.
- `--api-key-file`: Read the API key from a file.
- `--crop`: Apply `left,top,right,bottom` cropping after generation.
- `--resize`: Apply `WIDTHxHEIGHT` resizing after generation.
- `--format`: Force the saved format to `PNG`, `JPEG`, or `WEBP`.
- `--dry-run`: Print the resolved request payload without calling the API.

## API Key Resolution

Resolve credentials in this order:

1. `--api-key`
2. `GEMINI_API_KEY`
3. `GOOGLE_API_KEY`
4. `--api-key-file`
5. `GEMINI_API_KEY_FILE`
6. `GOOGLE_API_KEY_FILE`

Accept these key file formats:

- Plain text containing only the key
- `.env` style: `GEMINI_API_KEY=...`
- `.env` style: `GOOGLE_API_KEY=...`

## When to Read References

Read [references/gemini-image-generation.md](references/gemini-image-generation.md) when you need:

- Current model names or their intended roles
- The latest documented SDK usage for generation vs image editing
- A reminder of installation, auth conventions, chat history, or multi-turn image workflows

Read [references/prompting-guide.md](references/prompting-guide.md) when:

- The model is producing vague, generic, or inconsistent results
- You need better generation prompts for a product shot, icon, poster, mockup, or hero image
- You need tighter edit prompts that clearly separate what should change from what should stay fixed
- You are doing multi-turn refinement and want prompts that reduce drift between turns

## Constraints

- Use the bundled script and the official Google GenAI SDK instead of raw REST calls.
- Prefer `--dry-run` first when verifying prompt assembly or key resolution.
- Treat `google-genai` and `Pillow` as required dependencies for this skill.
- Use `--input-image` whenever the request is an edit, restyle, or transformation of an existing image.
- Use `--state-file` for iterative refinement across separate CLI invocations.
- Use `--reset-state` when reusing a state-file path for a completely new concept.
- Keep prompts explicit about subject, composition, lighting, style, and text rendering requirements.
- Treat generated images as local outputs that should be saved to a user-specified path when one is available.
- Do not claim a generation succeeded unless the script actually saved image files.

## Files

- `scripts/generate_image.py`: SDK-based CLI for generation, editing, and light post-processing.
- `references/gemini-image-generation.md`: Current Google Gemini image generation notes.
- `references/prompting-guide.md`: Practical prompt-writing patterns for generation, editing, and multi-turn refinement.

## Source

- https://ai.google.dev/gemini-api/docs/image-generation
