"""Central configuration: constants, paths, and tunables.

Nothing else in the app should hardcode a value that belongs here.
"""

ASSISTANT_NAME = "Jarvis"

# --- Text-to-speech ---
TTS_RATE = 175
TTS_VOLUME = 1.0
VOICE_INDEX = 0  # index into pyttsx3's available voices list

# --- Speech-to-text ---
AMBIENT_NOISE_DURATION = 1.0  # seconds, calibrated once at startup (not every loop)
STT_TIMEOUT = 8  # seconds to wait for speech to start before giving up
STT_PHRASE_TIME_LIMIT = 12  # max seconds for a single phrase

# --- Web targets ---
YOUTUBE_URL = "https://youtube.com"
GOOGLE_URL = "https://google.com"
CHATGPT_URL = "https://chat.openai.com"

# --- Local paths ---
# TODO(Phase 13): move machine-specific paths like this into a .env or a
# user config file instead of committing them here.
VS_CODE_PATH = r"C:\jarvis project"
