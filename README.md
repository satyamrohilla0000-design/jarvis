# Jarvis

A modular voice-controlled desktop assistant for Windows, built with Python.

Jarvis is designed around a scalable architecture that separates speech processing, command routing, and command execution into independent modules. Instead of relying on a large conditional (`if/elif`) chain, it uses a registry-based command router, making the codebase easier to maintain, test, and extend.

This repository contains the **Milestone A** implementation, which focuses on establishing a solid architectural foundation before introducing advanced AI capabilities in future milestones.

---

## Features

- Voice-controlled command execution
- Speech-to-Text using Google Speech Recognition
- Asynchronous Text-to-Speech
- Registry-based command routing
- Website automation
  - YouTube
  - Google
  - ChatGPT
- Wikipedia search
- Music playback through YouTube
- Current time announcement
- Visual Studio Code launcher
- Graceful application shutdown
- Modular package architecture
- Unit-tested components

---

## Technology Stack

- Python 3.13
- SpeechRecognition
- PyAudio
- pyttsx3
- pywhatkit
- wikipedia
- pytest

---

## Project Structure

```text
jarvis/
├── main.py
├── config/
│   └── settings.py
├── core/
│   ├── speech/
│   │   ├── stt.py
│   │   └── tts.py
│   └── commands/
│       ├── router.py
│       └── handlers/
│           ├── info.py
│           ├── system.py
│           └── web.py
├── utils/
│   └── logger.py
├── tests/
├── requirements.txt
└── README.md
```

---

## Installation

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
python main.py
```

---

## Running Tests

```bash
pytest
```

The test suite is hardware-independent and does not require a microphone or speakers.

---

## Supported Voice Commands

| Command | Description |
|----------|-------------|
| Open YouTube | Opens YouTube in the default browser |
| Open Google | Opens Google |
| Open ChatGPT | Opens ChatGPT |
| Play *song* | Plays the requested song on YouTube |
| What is *topic* | Performs a Wikipedia search |
| Who is *person* | Performs a Wikipedia search |
| Time | Announces the current system time |
| Open Code | Opens the configured Visual Studio Code workspace |
| Exit / Stop | Terminates Jarvis |

---

## Configuration

Application configuration is centralized in:

```text
config/settings.py
```

Update the `VS_CODE_PATH` value to match your local Visual Studio Code workspace if necessary.

---

## Architecture

Jarvis follows a modular pipeline:

```text
Microphone
      │
      ▼
Speech Recognition
      │
      ▼
Command Router
      │
      ├─────────────┐
      ▼             ▼
Web           System
Handler        Handler
      │
      ▼
Information Handler
      │
      ▼
Text-to-Speech
```

The routing layer is intentionally isolated from command implementations, allowing new commands to be added without modifying the core application flow.

---

## Extending Jarvis

To add a new command:

1. Implement a handler inside `core/commands/handlers/`.
2. Register the command in the module's `register()` function using the router.

Example:

```python
router.add("trigger phrase", handler=my_handler)
```

No modifications to the application's entry point are required.

---

## Current Scope

Milestone A includes the core voice assistant infrastructure:

- Modular project architecture
- Speech recognition
- Text-to-speech
- Command routing
- Website automation
- Wikipedia integration
- Music playback
- Automated testing

---

## Roadmap

Future milestones will introduce:

- Wake-word detection
- Offline speech recognition
- Large Language Model integration
- Persistent memory
- Face recognition
- Gesture control
- Desktop automation
- Plugin architecture
- AI vision
- Personal productivity features

---

## License

This project is licensed under the MIT License.

---

## Author

**Satyam**

BCA Student | Python Developer | Generative AI Enthusiast

Focused on building scalable AI applications, automation tools, and intelligent desktop assistants.
