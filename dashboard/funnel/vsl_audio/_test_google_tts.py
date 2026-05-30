"""
Google Cloud TTS 音声生成テスト

01_hook.txt を 5 種類の音声で生成し、聴き比べる。
"""
import base64
import json
import os
import sys
import time
from pathlib import Path
from urllib import request

API_KEY = os.environ.get("GOOGLE_TTS_API_KEY", "")  # 環境変数で渡す(キーをコードに直書きしない)
ENDPOINT = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"

HERE = Path(__file__).resolve().parent
TEXT_FILE = HERE / "01_hook.txt"

# 5 voices to compare (all MALE for 桜木 — 40代男性)
VOICES = [
    # Chirp3-HD (top tier)
    ("ja-JP-Chirp3-HD-Charon",  "Chirp3-HD男性A・Charon"),
    ("ja-JP-Chirp3-HD-Algieba", "Chirp3-HD男性B・Algieba"),
    ("ja-JP-Chirp3-HD-Alnilam", "Chirp3-HD男性C・Alnilam"),
    # Neural2 (mid tier)
    ("ja-JP-Neural2-D", "Neural2男性D"),
    # Wavenet (standard)
    ("ja-JP-Wavenet-D", "Wavenet男性D"),
]


def synthesize(text: str, voice_name: str) -> bytes:
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": "ja-JP", "name": voice_name},
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": 1.0,
            "pitch": 0.0,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return base64.b64decode(result["audioContent"])
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        if hasattr(e, "read"):
            print(f"  Response: {e.read().decode()[:500]}", file=sys.stderr)
        raise


def main():
    text = TEXT_FILE.read_text(encoding="utf-8")
    char_count = len(text)
    print(f"Text source: {TEXT_FILE.name}")
    print(f"Char count : {char_count}")
    print()

    for voice_name, label in VOICES:
        out = HERE / f"test_{voice_name.replace('ja-JP-', '')}.mp3"
        print(f"-> {label}")
        print(f"   voice: {voice_name}")
        t0 = time.time()
        try:
            audio = synthesize(text, voice_name)
        except Exception:
            print()
            continue
        out.write_bytes(audio)
        dt = time.time() - t0
        print(f"   saved: {out.name} ({len(audio):,} bytes, {dt:.1f}s)")
        print()

    # Cost calculation
    chirp_chars = char_count * 3  # 3 Chirp3-HD voices
    neural_chars = char_count * 1
    wavenet_chars = char_count * 1
    total = chirp_chars + neural_chars + wavenet_chars
    print("=" * 50)
    print(f"Total characters consumed: {total:,}")
    print(f"  Chirp3-HD:  {chirp_chars:,} chars (free tier: 1,000,000/month)")
    print(f"  Neural2:    {neural_chars:,} chars (free tier: 1,000,000/month)")
    print(f"  Wavenet:    {wavenet_chars:,} chars (free tier: 1,000,000/month)")
    print()
    print(f"Cost: $0.00 (all under free tier)")


if __name__ == "__main__":
    main()
