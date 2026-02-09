
# ScriptEase

ScriptEase is a small Windows desktop widget that rewrites, summarizes, or improves text using a **local** LLM (GGUF) via `ctransformers`.

## Requirements

- Windows
- Python 3.10+ (recommended)
- A downloaded GGUF model file (see **Model setup**)

## Install

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Model setup

ScriptEase expects this file to exist:

`models\mistral-7b-instruct-v0.2.Q4_K_M.gguf`

See [models/readme.md](models/readme.md) for the download link and placement steps.

## Run

Start the widget (it launches hidden):

```powershell
python runWidget.py
```

Hotkey:

- `Ctrl+Shift+A` — show and focus the widget

## How it works

- The widget listens to your clipboard; copied text appears in the input box.
- Choose one of the actions: **Rewrite**, **Summarize**, **Improve**.
- The model is loaded on first use (may take a moment), then the output appears in the lower box.
- Use **Copy Output** to copy results back to the clipboard.

## Configuration notes

The local model settings (context length, thread count, model filename) are in [core/llmEngine.py](core/llmEngine.py).

## Troubleshooting

- **Hotkey doesn’t trigger**: another app may be using `Ctrl+Shift+A`, or Windows permissions may block global hotkeys in some environments.
- **Model not found / load fails**: confirm the GGUF file path is exactly `models\mistral-7b-instruct-v0.2.Q4_K_M.gguf`.
