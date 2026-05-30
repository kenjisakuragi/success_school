"""
VSL本番音声生成 ― Algieba 0.88 でFull 6ブロック WAV生成
(長文ブロックは自動分割対応)
"""
import base64
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib import request

API_KEY = os.environ.get("GOOGLE_TTS_API_KEY", "")  # 環境変数で渡す(キーをコードに直書きしない)
ENDPOINT = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"
HERE = Path(__file__).resolve().parent

VOICE = "ja-JP-Chirp3-HD-Algieba"
RATE = 0.88
SAMPLE_RATE = 24000
MAX_BYTES = 4500  # safety margin under 5000 byte API limit

BLOCKS = [
    ("01_hook.txt",     "final_01_hook"),
    ("02_problem.txt",  "final_02_problem"),
    ("03_story.txt",    "final_03_story"),
    ("04_solution.txt", "final_04_solution"),
    ("05_demo.txt",     "final_05_demo"),
    ("06_cta.txt",      "final_06_cta"),
]


def synthesize_wav(text: str) -> bytes:
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": "ja-JP", "name": VOICE},
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "sampleRateHertz": SAMPLE_RATE,
            "speakingRate": RATE,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read())
        return base64.b64decode(result["audioContent"])


def split_text(text: str, max_bytes: int = MAX_BYTES) -> list[str]:
    """段落区切り(空行)で分割し、各チャンクが max_bytes 以内になるようまとめる"""
    paragraphs = re.split(r"\n\s*\n", text.strip())
    chunks: list[str] = []
    current: list[str] = []
    current_bytes = 0
    for p in paragraphs:
        p_bytes = len((p + "\n\n").encode("utf-8"))
        if current and current_bytes + p_bytes > max_bytes:
            chunks.append("\n\n".join(current))
            current = [p]
            current_bytes = p_bytes
        else:
            current.append(p)
            current_bytes += p_bytes
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def concat_wav_files(chunks: list[bytes]) -> bytes:
    """複数のWAVバイト列を1つに連結(ヘッダーは最初のだけ残し、データを連結)"""
    if not chunks:
        return b""
    if len(chunks) == 1:
        return chunks[0]
    # WAV header is 44 bytes for LINEAR16. Concatenate data portions only.
    header = chunks[0][:44]
    data_parts = [chunks[0][44:]]
    for c in chunks[1:]:
        data_parts.append(c[44:])
    combined_data = b"".join(data_parts)
    # Update RIFF chunk size (bytes 4-7) and data subchunk size (bytes 40-43)
    total_data_size = len(combined_data)
    new_riff_size = (36 + total_data_size).to_bytes(4, "little")
    new_data_size = total_data_size.to_bytes(4, "little")
    new_header = header[:4] + new_riff_size + header[8:40] + new_data_size
    return new_header + combined_data


def main():
    print(f"VSL本番音声生成 開始")
    print(f"Voice : {VOICE}")
    print(f"Rate  : {RATE}")
    print(f"Format: WAV (LINEAR16) {SAMPLE_RATE}Hz")
    print()

    total_chars = 0
    total_bytes = 0
    for src_name, out_name in BLOCKS:
        src = HERE / src_name
        if not src.exists():
            print(f"  [SKIP] {src_name} not found")
            continue
        text = src.read_text(encoding="utf-8")
        char_count = len(text)
        chunks = split_text(text)
        out = HERE / f"{out_name}_Algieba_088.wav"
        print(f"-> {src_name} ({char_count:,} chars / {len(chunks)} chunks)")
        t0 = time.time()
        wavs: list[bytes] = []
        for i, chunk in enumerate(chunks, 1):
            ch_bytes = len(chunk.encode("utf-8"))
            print(f"   chunk {i}/{len(chunks)} ({ch_bytes:,} bytes) ", end="", flush=True)
            try:
                wav = synthesize_wav(chunk)
                wavs.append(wav)
                print(f"OK ({len(wav)/1024/1024:.2f}MB)")
            except Exception as e:
                msg = str(e)
                if hasattr(e, "read"):
                    try:
                        msg += " | " + e.read().decode()[:300]
                    except Exception:
                        pass
                print(f"FAIL: {msg}")
                wavs = []
                break
        if not wavs:
            print(f"   [SKIP] {src_name}\n")
            continue
        combined = concat_wav_files(wavs)
        out.write_bytes(combined)
        dt = time.time() - t0
        size_mb = len(combined) / 1024 / 1024
        print(f"   saved: {out.name} ({size_mb:.2f}MB, {dt:.1f}s)\n")
        total_chars += char_count
        total_bytes += len(combined)

    print("=" * 50)
    print(f"完了: 計 {total_chars:,} chars / {total_bytes/1024/1024:.2f}MB")
    print(f"コスト: ¥0 (Chirp3-HD 無料枠 1,000,000 chars/月 の {total_chars/10000:.2f}%)")


if __name__ == "__main__":
    main()
