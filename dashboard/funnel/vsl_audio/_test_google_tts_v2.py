"""
Google Cloud TTS 音声生成 - 感情表現強化版

3 つのアプローチで感情・抑揚を強化:
A. Chirp3-HD + 速度/ピッチ細かい調整
B. Neural2 + SSML(emphasis, break, prosody)
C. Wavenet + SSML
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

# Hookパート(プレーンテキスト版)
PLAIN_TEXT = """あなたは今までに、引き寄せの本を、何冊、読みましたか?

たぶん、5冊くらいでしょうか。10冊? それとも、20冊以上の方も、いらっしゃるかもしれません。

そして、はっきり聞かせてください。

そのうち、本当に人生が変わった本は、何冊ありましたか?

おそらく、ゼロですよね。

「願えば叶う」と書いてあった。実践しました。叶いませんでした。

「感謝すれば引き寄せられる」と書いてあった。やってみました。何も起きませんでした。

大丈夫です。あなたのせいでは、ありません。

メソッドの設計が、不完全だったのです。"""

# 同じ内容を SSML で感情マークアップ
SSML_TEXT = """<speak>
<prosody rate="0.95" pitch="-1st">
あなたは今までに、引き寄せの本を、<emphasis level="moderate">何冊</emphasis>、読みましたか?<break time="800ms"/>

たぶん、<emphasis level="reduced">5冊くらい</emphasis>でしょうか。<break time="400ms"/>
10冊? <break time="300ms"/>
それとも、<emphasis level="moderate">20冊以上</emphasis>の方も、いらっしゃるかもしれません。<break time="1000ms"/>

そして、<break time="400ms"/><emphasis level="strong">はっきり</emphasis>、聞かせてください。<break time="800ms"/>

そのうち、<break time="300ms"/><emphasis level="strong">本当に</emphasis>人生が変わった本は、<emphasis level="moderate">何冊</emphasis>、ありましたか?<break time="1500ms"/>

<prosody rate="0.9">おそらく、<emphasis level="strong">ゼロ</emphasis>ですよね。</prosody><break time="1200ms"/>
</prosody>

<prosody rate="1.0">
<emphasis level="moderate">「願えば叶う」</emphasis>と書いてあった。<break time="300ms"/>実践しました。<break time="500ms"/><prosody pitch="-2st">叶いませんでした。</prosody><break time="800ms"/>

<emphasis level="moderate">「感謝すれば引き寄せられる」</emphasis>と書いてあった。<break time="300ms"/>やってみました。<break time="500ms"/><prosody pitch="-2st">何も起きませんでした。</prosody><break time="1500ms"/>
</prosody>

<prosody rate="0.85" pitch="-2st">
<emphasis level="strong">大丈夫です。</emphasis><break time="600ms"/>あなたのせいでは、<emphasis level="strong">ありません。</emphasis><break time="1200ms"/>

メソッドの<emphasis level="moderate">設計</emphasis>が、不完全だったのです。
</prosody>
</speak>"""

VARIATIONS = [
    # A. Chirp3-HD with rate only (no pitch - not supported)
    ("A1_Chirp3HD-Charon_slow",   PLAIN_TEXT, "ja-JP-Chirp3-HD-Charon",  0.9, 0.0, False, "Chirp3-HD Charon 速度0.9 (重み)"),
    ("A2_Chirp3HD-Algieba_slow",  PLAIN_TEXT, "ja-JP-Chirp3-HD-Algieba", 0.9, 0.0, False, "Chirp3-HD Algieba 速度0.9"),
    ("A3_Chirp3HD-Achird",        PLAIN_TEXT, "ja-JP-Chirp3-HD-Achird",  0.95, 0.0, False, "Chirp3-HD Achird 速度0.95"),
    ("A4_Chirp3HD-Algenib",       PLAIN_TEXT, "ja-JP-Chirp3-HD-Algenib", 0.95, 0.0, False, "Chirp3-HD Algenib 速度0.95"),
    ("A5_Chirp3HD-Iapetus",       PLAIN_TEXT, "ja-JP-Chirp3-HD-Iapetus", 0.95, 0.0, False, "Chirp3-HD Iapetus 速度0.95"),
    # 既に成功した分はスキップ
]


def synthesize(text: str, voice_name: str, speaking_rate: float, pitch: float, is_ssml: bool) -> bytes:
    input_field = {"ssml": text} if is_ssml else {"text": text}
    payload = {
        "input": input_field,
        "voice": {"languageCode": "ja-JP", "name": voice_name},
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": speaking_rate,
            "pitch": pitch,
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
        msg = str(e)
        if hasattr(e, "read"):
            try:
                msg += " | " + e.read().decode()[:500]
            except Exception:
                pass
        print(f"  ERROR: {msg}", file=sys.stderr)
        return None


def main():
    print(f"Plain text source length: {len(PLAIN_TEXT)} chars")
    print(f"SSML text source length : {len(SSML_TEXT)} chars (markup含む)")
    print()

    for tag, text, voice, rate, pitch, is_ssml, label in VARIATIONS:
        out = HERE / f"v2_{tag}.mp3"
        print(f"-> {label}")
        t0 = time.time()
        audio = synthesize(text, voice, rate, pitch, is_ssml)
        if audio is None:
            print()
            continue
        out.write_bytes(audio)
        dt = time.time() - t0
        print(f"   saved: {out.name} ({len(audio):,} bytes, {dt:.1f}s)")
        print()


if __name__ == "__main__":
    main()
