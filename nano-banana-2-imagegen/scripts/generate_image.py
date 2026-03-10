#!/usr/bin/env python3
"""
Generate or edit images with Gemini image models via the Google GenAI SDK.

Requirements:
    pip install -U google-genai pillow
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from io import BytesIO
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError as exc:
    genai = None
    types = None
    GENAI_IMPORT_ERROR = exc
else:
    GENAI_IMPORT_ERROR = None

try:
    from PIL import Image
except ImportError as exc:
    Image = None
    PIL_IMPORT_ERROR = exc
else:
    PIL_IMPORT_ERROR = None

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_OUTPUT = "nano-banana-image.png"
ENV_KEY_NAMES = ("GEMINI_API_KEY", "GOOGLE_API_KEY")
ENV_KEY_FILE_NAMES = ("GEMINI_API_KEY_FILE", "GOOGLE_API_KEY_FILE")
SAVE_FORMATS = {"PNG", "JPEG", "WEBP"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate or edit images with Nano Banana 2 using google-genai.",
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Prompt text. Use --prompt-file to load from a file instead.",
    )
    parser.add_argument(
        "--prompt-file",
        help="Path to a text file containing the full prompt.",
    )
    parser.add_argument(
        "--input-image",
        action="append",
        default=[],
        help="Path to an input image to edit. Repeat for multiple reference images.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output image path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--state-file",
        help="Optional JSON file used to persist chat history for multi-turn editing.",
    )
    parser.add_argument(
        "--reset-state",
        action="store_true",
        help="Ignore any existing state file contents and start a fresh chat.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini image model id. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--api-key",
        help="API key value. Overrides environment variables and key files.",
    )
    parser.add_argument(
        "--api-key-file",
        help="Path to a file containing the API key or KEY=value entries.",
    )
    parser.add_argument(
        "--crop",
        help="Optional crop box as left,top,right,bottom applied after generation.",
    )
    parser.add_argument(
        "--resize",
        help="Optional resize target as WIDTHxHEIGHT applied after generation.",
    )
    parser.add_argument(
        "--format",
        choices=sorted(SAVE_FORMATS),
        help="Optional output format override applied when saving.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve prompt, credentials, and inputs without calling the API.",
    )
    return parser.parse_args()


def ensure_dependencies() -> None:
    missing = []
    if genai is None:
        missing.append(f"google-genai ({GENAI_IMPORT_ERROR})")
    if Image is None:
        missing.append(f"Pillow ({PIL_IMPORT_ERROR})")
    if missing:
        details = ", ".join(missing)
        raise RuntimeError(
            "Missing required dependencies: "
            f"{details}. Install them with: pip install -U google-genai pillow"
        )


def load_state_history(state_file: str | None, reset_state: bool) -> list[object]:
    if not state_file or reset_state:
        return []
    path = Path(state_file).expanduser()
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    history_data = payload.get("history", [])
    return [types.Content.model_validate(item) for item in history_data]


def save_state_history(state_file: str | None, model: str, history: list[object]) -> None:
    if not state_file:
        return
    path = Path(state_file).expanduser()
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": model,
        "history": [
            item.model_dump(mode="json", exclude_none=True)
            if hasattr(item, "model_dump")
            else item
            for item in history
        ],
    }
    path.write_text(json.dumps(payload, indent=2))


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        prompt_text = Path(args.prompt_file).expanduser().read_text().strip()
    else:
        prompt_text = " ".join(args.prompt).strip()
    if not prompt_text:
        raise ValueError("Provide a prompt as arguments or via --prompt-file.")
    return prompt_text


def read_api_key_file(path_str: str) -> str:
    path = Path(path_str).expanduser()
    raw = path.read_text().strip()
    if not raw:
        raise ValueError(f"API key file is empty: {path}")

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            return line.strip().strip("\"'")
        key_name, value = line.split("=", 1)
        key_name = key_name.strip()
        value = value.strip().strip("\"'")
        if key_name in ENV_KEY_NAMES and value:
            return value

    if "\n" not in raw and "=" not in raw:
        return raw.strip().strip("\"'")
    raise ValueError(
        f"Could not find {', '.join(ENV_KEY_NAMES)} in API key file: {path}"
    )


def resolve_api_key(args: argparse.Namespace) -> tuple[str, str]:
    if args.api_key:
        return args.api_key.strip(), "--api-key"

    for env_name in ENV_KEY_NAMES:
        value = os.environ.get(env_name, "").strip()
        if value:
            return value, env_name

    file_candidates = []
    if args.api_key_file:
        file_candidates.append(args.api_key_file)
    for env_name in ENV_KEY_FILE_NAMES:
        value = os.environ.get(env_name, "").strip()
        if value:
            file_candidates.append(value)

    for candidate in file_candidates:
        api_key = read_api_key_file(candidate)
        if api_key:
            return api_key, candidate

    raise ValueError(
        "No API key found. Set GEMINI_API_KEY or GOOGLE_API_KEY, "
        "or pass --api-key-file / GEMINI_API_KEY_FILE."
    )


def parse_crop(value: str | None) -> tuple[int, int, int, int] | None:
    if not value:
        return None
    parts = [item.strip() for item in value.split(",")]
    if len(parts) != 4:
        raise ValueError("Crop must be left,top,right,bottom.")
    try:
        left, top, right, bottom = (int(item) for item in parts)
    except ValueError as exc:
        raise ValueError("Crop values must be integers.") from exc
    if right <= left or bottom <= top:
        raise ValueError("Crop right/bottom must be greater than left/top.")
    return left, top, right, bottom


def parse_resize(value: str | None) -> tuple[int, int] | None:
    if not value:
        return None
    parts = value.lower().split("x")
    if len(parts) != 2:
        raise ValueError("Resize must be WIDTHxHEIGHT.")
    try:
        width, height = (int(item) for item in parts)
    except ValueError as exc:
        raise ValueError("Resize width and height must be integers.") from exc
    if width <= 0 or height <= 0:
        raise ValueError("Resize width and height must be positive.")
    return width, height


def load_input_images(paths: list[str]) -> list[Image.Image]:
    images = []
    for path_str in paths:
        path = Path(path_str).expanduser()
        with Image.open(path) as image:
            images.append(image.copy())
    return images


def build_contents(prompt: str, input_images: list[Image.Image]) -> list[object]:
    return [prompt, *input_images]


def extract_images_and_texts(response: object) -> tuple[list[Image.Image], list[str]]:
    images: list[Image.Image] = []
    texts: list[str] = []
    for part in getattr(response, "parts", []) or []:
        if getattr(part, "text", None):
            texts.append(part.text)
            continue
        inline_data = getattr(part, "inline_data", None)
        data = getattr(inline_data, "data", None) if inline_data is not None else None
        if data:
            with Image.open(BytesIO(data)) as image:
                images.append(image.copy())
    return images, texts


def apply_post_processing(
    image: Image.Image,
    crop_box: tuple[int, int, int, int] | None,
    resize_to: tuple[int, int] | None,
) -> Image.Image:
    result = image.copy()
    if crop_box:
        result = result.crop(crop_box)
    if resize_to:
        result = result.resize(resize_to, Image.Resampling.LANCZOS)
    return result


def destination_for_index(base_output: Path, index: int, save_format: str | None) -> Path:
    if save_format:
        suffix = f".{save_format.lower()}"
        if index == 0:
            return base_output.with_suffix(suffix)
        return base_output.with_name(f"{base_output.stem}-{index + 1}{suffix}")

    if index == 0:
        return base_output
    if base_output.suffix:
        return base_output.with_name(f"{base_output.stem}-{index + 1}{base_output.suffix}")
    return base_output.with_name(f"{base_output.name}-{index + 1}")


def save_images(
    images: list[Image.Image],
    output: str,
    crop_box: tuple[int, int, int, int] | None,
    resize_to: tuple[int, int] | None,
    save_format: str | None,
) -> list[Path]:
    base_output = Path(output).expanduser()
    if base_output.parent != Path("."):
        base_output.parent.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    for index, image in enumerate(images):
        processed = apply_post_processing(image, crop_box, resize_to)
        destination = destination_for_index(base_output, index, save_format)
        if save_format == "JPEG" and processed.mode not in ("RGB", "L"):
            processed = processed.convert("RGB")
        if save_format:
            processed.save(destination, format=save_format)
        else:
            processed.save(destination)
        saved_paths.append(destination)
    return saved_paths


def main() -> int:
    args = parse_args()
    try:
        prompt = load_prompt(args)
        api_key, api_key_source = resolve_api_key(args)
        ensure_dependencies()
        input_images = load_input_images(args.input_image)
        crop_box = parse_crop(args.crop)
        resize_to = parse_resize(args.resize)
        history = load_state_history(args.state_file, args.reset_state)
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        mode = "edit" if input_images else "generate"
        print(
            "\n".join(
                [
                    f"mode={mode}",
                    f"model={args.model}",
                    f"api_key_source={api_key_source}",
                    f"input_images={len(input_images)}",
                    f"history_turns={len(history)}",
                    f"state_file={Path(args.state_file).expanduser() if args.state_file else None}",
                    f"output={Path(args.output).expanduser()}",
                    f"crop={crop_box}",
                    f"resize={resize_to}",
                    f"format={args.format}",
                    f"prompt={prompt}",
                ]
            )
        )
        return 0

    try:
        client = genai.Client(api_key=api_key)
        if history or args.state_file:
            chat = client.chats.create(model=args.model, history=history)
            response = chat.send_message(build_contents(prompt, input_images))
            updated_history = chat.get_history()
        else:
            response = client.models.generate_content(
                model=args.model,
                contents=build_contents(prompt, input_images),
            )
            updated_history = history
        images, texts = extract_images_and_texts(response)
    except Exception as exc:
        print(f"Error: Gemini SDK request failed: {exc}", file=sys.stderr)
        return 1

    if not images:
        print("Error: Gemini response did not include any image parts.", file=sys.stderr)
        for text in texts:
            print(text, file=sys.stderr)
        return 1

    try:
        saved_paths = save_images(
            images=images,
            output=args.output,
            crop_box=crop_box,
            resize_to=resize_to,
            save_format=args.format,
        )
    except OSError as exc:
        print(f"Error: Failed to save image output: {exc}", file=sys.stderr)
        return 1

    try:
        save_state_history(args.state_file, args.model, updated_history)
    except (OSError, TypeError, ValueError) as exc:
        print(f"Error: Failed to save state file: {exc}", file=sys.stderr)
        return 1

    for path in saved_paths:
        print(f"Saved image: {path}")
    if args.state_file:
        print(f"Saved state: {Path(args.state_file).expanduser()}")
    for text in texts:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
