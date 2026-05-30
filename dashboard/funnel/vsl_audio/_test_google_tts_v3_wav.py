"""
Google Cloud TTS v3 ― WAV高品質+抑揚改善
- Algieba ベースに rate 微調整(0.85/0.88/0.92/0.95)
- 未試行 MALE Chirp3-HD voices 5種
- 全て LINEAR16 (WAV) 24kHz
- テキストは句読点を増強した改良版
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

# 句読点を増強した改良テキスト(Hookパート抜粋)
# 戦略:適切な間 + 短文区切り + 「、」追加で自然な抑揚を引き出す
REFINED_TEXT = """あなたは、今までに、引き寄せの本を、何冊、読みましたか。

たぶん、5冊くらいでしょうか。

10冊、でしょうか。

それとも、20冊以上の方も、いらっしゃるかもしれません。

そして、はっきり、聞かせてください。

そのうち、本当に、人生が変わった本は、何冊、ありましたか。

…

おそらく、ゼロですよね。

「願えば叶う」と、書いてあった。

実践しました。

叶いませんでした。

「感謝すれば引き寄せられる」と、書いてあった。

やってみました。

何も、起きませんでした。

…

大丈夫です。

あなたのせいでは、ありません。

メソッドの、設計が、不完全だったのです。"""

VARIATIONS = [
    # Algieba の rate微調整(本命の候補)
    ("ALG_085", "ja-JP-Chirp3-HD-Algieba",        0.85, "Algieba rate0.85 最も落ち着き"),
    ("ALG_088", "ja-JP-Chirp3-HD-Algieba",        0.88, "Algieba rate0.88 ナレーター調"),
    ("ALG_092", "ja-JP-Chirp3-HD-Algieba",        0.92, "Algieba rate0.92 やや軽快"),
    ("ALG_095", "ja-JP-Chirp3-HD-Algieba",        0.95, "Algieba rate0.95 標準寄り"),
    # 未試行 MALE Chirp3-HD voices @ rate 0.9
    ("ENC_090", "ja-JP-Chirp3-HD-Enceladus",       0.90, "Enceladus(新)"),
    ("FEN_090", "ja-JP-Chirp3-HD-Fenrir",          0.90, "Fenrir(新)"),
    ("ORU_090", "ja-JP-Chirp3-HD-Orus",            0.90, "Orus(新)"),
    ("RAS_090", "ja-JP-Chirp3-HD-Rasalgethi",      0.90, "Rasalgethi(新)"),
    ("SAD_090", "ja-JP-Chirp3-HD-Sadaltager",      0.90, "Sadaltager(新)"),
    ("UMB_090", "ja-JP-Chirp3-HD-Umbriel",         0.90, "Umbriel(新)"),
]


def synthesize_wav(text: str, voice_name: str, speaking_rate: float) -> bytes:
    """WAV(LINEAR16・24kHz)で音声生成"""
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": "ja-JP", "name": voice_name},
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "sampleRateHertz": 24000,
            "speakingRate": speaking_rate,
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
        with request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return base64.b64decode(result["audioContent"])
    except Exception as e:
        msg = str(e)
        if hasattr(e, "read"):
            try:
                msg += " | " + e.read().decode()[:500]
            except Exception:
                pass
        print(f"  ERROR: {msg}", file=sys.stderr)
        return None


def main():
    print(f"Refined text length: {len(REFINED_TEXT)} chars")
    print(f"Output format: LINEAR16 (WAV) 24kHz")
    print()

    for tag, voice, rate, label in VARIATIONS:
        out = HERE / f"v3_{tag}_{voice.split('-')[-1]}.wav"
        print(f"-> {label}")
        t0 = time.time()
        audio = synthesize_wav(REFINED_TEXT, voice, rate)
        if audio is None:
            print()
            continue
        out.write_bytes(audio)
        dt = time.time() - t0
        size_mb = len(audio) / 1024 / 1024
        print(f"   saved: {out.name} ({size_mb:.2f}MB, {dt:.1f}s)")
        print()


if __name__ == "__main__":
    main()
