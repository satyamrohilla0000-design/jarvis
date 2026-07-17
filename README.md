# Jarvis

A voice-controlled desktop assistant for Windows.

This is the Milestone A rebuild: same features as the original single-file
version (open YouTube/Google/ChatGPT, tell the time, Wikipedia lookups,
play a song, open VS Code, exit), refactored into a proper package with
async/thread-safe speech and a registry-based command router instead of
one long if/elif chain. Gesture control, face detection, wake word, and
the rest of the roadmap land in later milestones.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python main.py
```

PyAudio can fail to build from source on Windows. If `pip install` errors
on it, install a prebuilt wheel instead (search "PyAudio Windows wheel"
for your Python version) or install via `pipwin install pyaudio`.

## Project layout

```
jarvis/
├── main.py                  # entry point
├── config/settings.py       # all constants live here
├── core/
│   ├── speech/tts.py        # async speech queue
│   ├── speech/stt.py        # microphone + Google STT
│   └── commands/
│       ├── router.py        # registry-based dispatch
│       └── handlers/        # one module per command group
├── utils/logger.py
└── tests/                   # no hardware required to run these
```

## Running tests

```bash
pytest
```

## Adding a new command

Add a handler function to the relevant file in `core/commands/handlers/`
(or a new file), then call `router.add("trigger phrase", handler=your_func)`
in that module's `register()` function.
