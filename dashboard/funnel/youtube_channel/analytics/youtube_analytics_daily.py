"""
YouTube アナリティクス日次取得スクリプト(変数別スコア設計)
============================================================
4変数ゲーム(ジャンル・企画・サムネ・台本)の各スコアを日次記録する。

指標 → 変数の対応:
  CTR(impressionClickThroughRate) → サムネ/タイトル/企画 の良し悪し
  平均視聴率(averageViewPercentage) → 台本(特に冒頭)の良し悪し
  インプレッション(impressions)     → ジャンル一貫性/企画需要 の規模
  視聴回数・登録者増                 → 総合結果

実行方法:
  cd dashboard/funnel/youtube_channel/analytics
  python youtube_analytics_daily.py

初回のみ:
  pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
  client_secret.json をこのフォルダに置く(取得手順は _SETUP_GUIDE.md)

出力:
  analytics/daily_YYYY-MM-DD.md(その日のスナップショット)
  analytics/_history.csv(全日次データの累積・PDCA分析用)
"""

import os
import sys
import csv
import datetime
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
except ImportError:
    print("ライブラリ未インストール。下記を実行してください:")
    print("  pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
    sys.exit(1)

# ─────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / "token.json"
CLIENT_SECRET = SCRIPT_DIR / "client_secret.json"
HISTORY_CSV = SCRIPT_DIR / "_history.csv"

SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
]

# 集計期間(直近N日)
LOOKBACK_DAYS = 28
# 1動画あたりの「変数診断」しきい値(初期目安・データが溜まったら調整)
CTR_GOOD = 5.0       # CTR 5%以上 = サムネ/タイトル good
CTR_BAD = 2.0        # CTR 2%未満 = サムネ/タイトル 要改善
RETENTION_GOOD = 40.0  # 平均視聴率 40%以上 = 台本 good
RETENTION_BAD = 25.0   # 平均視聴率 25%未満 = 台本 要改善
# ─────────────────────────────────────────────


def get_authenticated_services():
    """OAuth認証(初回はブラウザ・以降はトークンキャッシュ)"""
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                print(f"client_secret.json がありません: {CLIENT_SECRET}")
                print("取得手順は _SETUP_GUIDE.md を参照してください。")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    yt_analytics = build("youtubeAnalytics", "v2", credentials=creds)
    yt_data = build("youtube", "v3", credentials=creds)
    return yt_analytics, yt_data


def get_channel_id(yt_data):
    res = yt_data.channels().list(part="id,snippet,statistics", mine=True).execute()
    item = res["items"][0]
    return item["id"], item["snippet"]["title"], item["statistics"]


def get_video_titles(yt_data, channel_id):
    """チャンネルの動画ID→タイトルのマップを取得"""
    titles = {}
    # アップロード済み再生リストを取得
    ch = yt_data.channels().list(part="contentDetails", id=channel_id).execute()
    uploads = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    page_token = None
    while True:
        pl = yt_data.playlistItems().list(
            part="snippet", playlistId=uploads, maxResults=50, pageToken=page_token
        ).execute()
        for it in pl["items"]:
            vid = it["snippet"]["resourceId"]["videoId"]
            titles[vid] = it["snippet"]["title"]
        page_token = pl.get("nextPageToken")
        if not page_token:
            break
    return titles


def fetch_video_metrics(yt_analytics, channel_id, start, end):
    """動画別の主要指標を取得"""
    res = yt_analytics.reports().query(
        ids=f"channel=={channel_id}",
        startDate=start,
        endDate=end,
        metrics="views,estimatedMinutesWatched,averageViewPercentage,"
                "subscribersGained,impressions,impressionClickThroughRate",
        dimensions="video",
        sort="-views",
        maxResults=50,
    ).execute()
    return res


def diagnose(ctr, retention):
    """4変数ゲームの診断"""
    diag = []
    if ctr is not None:
        if ctr >= CTR_GOOD:
            diag.append("サムネ/タイトル◎")
        elif ctr < CTR_BAD:
            diag.append("サムネ/タイトル要改善")
        else:
            diag.append("サムネ/タイトル△")
    if retention is not None:
        if retention >= RETENTION_GOOD:
            diag.append("台本◎")
        elif retention < RETENTION_BAD:
            diag.append("台本要改善(冒頭見直し)")
        else:
            diag.append("台本△")
    return " / ".join(diag)


def main():
    today = datetime.date.today()
    start = (today - datetime.timedelta(days=LOOKBACK_DAYS)).isoformat()
    end = today.isoformat()

    print("認証中...")
    yt_analytics, yt_data = get_authenticated_services()
    channel_id, channel_title, ch_stats = get_channel_id(yt_data)
    print(f"チャンネル: {channel_title}")

    titles = get_video_titles(yt_data, channel_id)
    metrics = fetch_video_metrics(yt_analytics, channel_id, start, end)

    rows = metrics.get("rows", [])
    headers = [h["name"] for h in metrics["columnHeaders"]]
    idx = {name: i for i, name in enumerate(headers)}

    # ── 日次Markdownレポート ──
    out = []
    out.append(f"# 📊 {channel_title} アナリティクス日次レポート")
    out.append(f"\n**日付:** {end}")
    out.append(f"**集計期間:** 直近{LOOKBACK_DAYS}日({start} 〜 {end})")
    out.append(f"**チャンネル登録者:** {ch_stats.get('subscriberCount','?')}")
    out.append(f"**総再生数:** {ch_stats.get('viewCount','?')}\n")
    out.append("---\n")
    out.append("# 🎮 動画別・4変数診断\n")
    out.append("| 動画 | 視聴 | CTR | 平均視聴% | 登録増 | 変数診断 |")
    out.append("|---|---|---|---|---|---|")

    history_rows = []
    for r in rows:
        vid = r[idx["video"]]
        title = titles.get(vid, vid)[:30]
        views = r[idx["views"]]
        ctr = r[idx.get("impressionClickThroughRate", -1)] if "impressionClickThroughRate" in idx else None
        ret = r[idx.get("averageViewPercentage", -1)] if "averageViewPercentage" in idx else None
        subs = r[idx.get("subscribersGained", -1)] if "subscribersGained" in idx else 0
        diag = diagnose(ctr, ret)
        ctr_s = f"{ctr:.1f}%" if ctr is not None else "─"
        ret_s = f"{ret:.1f}%" if ret is not None else "─"
        out.append(f"| {title} | {views} | {ctr_s} | {ret_s} | {subs} | {diag} |")
        history_rows.append([end, title, views, ctr, ret, subs])

    out.append("\n---\n")
    out.append("# 🔪 今日のPDCA示唆\n")
    out.append("```")
    out.append("CTR要改善が多い → サムネ/タイトルを勝ちパターン(pkg_11型)に寄せる")
    out.append("台本要改善が多い → 冒頭6秒〜30秒の見直し(Layer0/6秒ルール)")
    out.append("インプレ少ない   → 企画の需要・ジャンル一貫性を点検")
    out.append("```")
    out.append("\n※ AI(私)にこのファイルを渡せば、変数別の改善提案と次の企画を出します。\n")

    out_path = SCRIPT_DIR / f"daily_{end}.md"
    out_path.write_text("\n".join(out), encoding="utf-8")
    print(f"日次レポート保存: {out_path}")

    # ── 累積CSV(PDCA分析用)──
    new_file = not HISTORY_CSV.exists()
    with open(HISTORY_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["date", "title", "views", "ctr", "avg_view_pct", "subs_gained"])
        w.writerows(history_rows)
    print(f"累積CSV更新: {HISTORY_CSV}")
    print(f"取得動画数: {len(rows)}")


if __name__ == "__main__":
    main()
