"""
YouTube 書き起こし自動取得スクリプト
================================
用途:対象動画のURLを urls.txt に書いて実行 → research/ に書き起こしを保存

実行方法:
  cd dashboard/funnel/content_factory
  python _fetch_transcripts.py pkg_01

事前準備(初回のみ):
  pip install youtube-transcript-api

urls.txt の書き方:
  https://www.youtube.com/watch?v=VIDEO_ID1
  # コメント行
  https://www.youtube.com/watch?v=VIDEO_ID2
  https://youtu.be/VIDEO_ID3
"""

import sys
import re
import os
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Error: youtube-transcript-api が未インストールです")
    print("  pip install youtube-transcript-api")
    sys.exit(1)

PKG_NAME = sys.argv[1] if len(sys.argv) > 1 else "pkg_01"
SCRIPT_DIR = Path(__file__).parent
RESEARCH_DIR = SCRIPT_DIR / "research"
URLS_FILE = RESEARCH_DIR / f"{PKG_NAME}_urls.txt"
OUTPUT_FILE = RESEARCH_DIR / f"{PKG_NAME}_transcripts.md"

RESEARCH_DIR.mkdir(parents=True, exist_ok=True)


def extract_video_id(url: str) -> str | None:
    """YouTube URLから動画IDを抽出"""
    patterns = [
        r"youtube\.com/watch\?v=([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/embed/([A-Za-z0-9_-]{11})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url.strip()):
        return url.strip()
    return None


def fetch_one(video_id: str) -> dict:
    """1動画の字幕を取得(英語優先・なければ自動翻訳)"""
    api = YouTubeTranscriptApi()
    try:
        # 英語優先
        transcript = api.fetch(video_id, languages=["en", "en-US", "en-GB", "ja"])
        segments = list(transcript)
        full_text = " ".join(s.text for s in segments).replace("\n", " ")
        return {
            "video_id": video_id,
            "language": transcript.language_code if hasattr(transcript, "language_code") else "?",
            "segment_count": len(segments),
            "full_text": full_text,
            "error": None,
        }
    except Exception as e:
        return {"video_id": video_id, "error": str(e)}


def main():
    if not URLS_FILE.exists():
        print(f"URLファイルがありません: {URLS_FILE}")
        print("テンプレートを作成します。下記に対象URLを書いてから再実行してください。")
        URLS_FILE.write_text(
            "# YouTube URL を1行ずつ記入(#で始まる行はコメント)\n"
            "# 例:\n"
            "# https://www.youtube.com/watch?v=VIDEO_ID\n",
            encoding="utf-8",
        )
        return

    urls = [
        line.strip()
        for line in URLS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not urls:
        print(f"{URLS_FILE} にURLがありません。記入してから再実行してください。")
        return

    print(f"対象動画数: {len(urls)}")
    results = []
    for i, url in enumerate(urls, 1):
        vid = extract_video_id(url)
        if not vid:
            print(f"[{i}/{len(urls)}] URL不正: {url}")
            results.append({"url": url, "error": "URL parse failed"})
            continue
        print(f"[{i}/{len(urls)}] {vid} 取得中...", end=" ", flush=True)
        r = fetch_one(vid)
        r["url"] = url
        results.append(r)
        if r.get("error"):
            print(f"FAIL ({r['error'][:60]})")
        else:
            print(f"OK ({r['segment_count']} segments, {len(r['full_text'])} chars)")

    # Markdownで保存
    out = [f"# 📜 {PKG_NAME} 書き起こし\n",
           f"取得日: {os.popen('date').read().strip()}\n",
           f"対象動画数: {len(urls)}\n",
           "---\n"]
    for i, r in enumerate(results, 1):
        out.append(f"\n## 動画{i}: {r.get('url')}\n")
        if r.get("error"):
            out.append(f"⚠️ 取得失敗: {r['error']}\n")
            continue
        out.append(f"- VideoID: `{r['video_id']}`")
        out.append(f"- 言語: `{r.get('language', '?')}`")
        out.append(f"- セグメント数: {r['segment_count']}")
        out.append(f"- 文字数: {len(r['full_text'])}\n")
        out.append("### 書き起こし全文\n")
        out.append("```")
        out.append(r["full_text"])
        out.append("```\n")

    OUTPUT_FILE.write_text("\n".join(out), encoding="utf-8")
    print(f"\n保存: {OUTPUT_FILE}")
    print(f"成功: {sum(1 for r in results if not r.get('error'))}/{len(results)}")


if __name__ == "__main__":
    main()
