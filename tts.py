"""Server-side Mandarin TTS via edge-tts (Microsoft Edge's neural voices,
free, no API key). Disk-cached so repeat requests for the same text/voice/
rate never re-hit the network.
"""
import hashlib
import os

import edge_tts

CACHE_DIR = os.path.join(os.path.dirname(__file__), "tts_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Standard Putonghua (Beijing/Mainland) neural voices. Xiaoxiao is the
# default — Microsoft's most natural-sounding standard Mandarin female voice,
# widely used as the reference "Beijing accent" voice. Yunxi offered as an
# alternate male voice.
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"
ALLOWED_VOICES = {"zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural"}


def _rate_str(rate: float) -> str:
    """rate is a playback-speed multiplier (1.0 = normal), matching the old
    speechSynthesis rate convention — convert to edge-tts's percent-delta format."""
    pct = round((rate - 1.0) * 100)
    pct = max(-50, min(50, pct))
    return f"{pct:+d}%"


def cache_path(text: str, voice: str, rate: float) -> str:
    key = f"{voice}|{rate}|{text}".encode("utf-8")
    digest = hashlib.sha256(key).hexdigest()
    return os.path.join(CACHE_DIR, f"{digest}.mp3")


async def synthesize(text: str, voice: str = DEFAULT_VOICE, rate: float = 1.0) -> str:
    """Returns a path to a cached mp3 file for this text/voice/rate, generating
    it via edge-tts first if not already cached."""
    if voice not in ALLOWED_VOICES:
        voice = DEFAULT_VOICE
    path = cache_path(text, voice, rate)
    if not os.path.exists(path):
        communicate = edge_tts.Communicate(text, voice=voice, rate=_rate_str(rate))
        tmp_path = path + ".tmp"
        await communicate.save(tmp_path)
        os.replace(tmp_path, path)
    return path
