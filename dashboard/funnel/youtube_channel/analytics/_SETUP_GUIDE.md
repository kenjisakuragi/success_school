# ⚙️ アナリティクス自動取得 セットアップ手順

**所要:** 初回15-30分(以降は完全自動)
**目的:** YouTube アナリティクスを毎日自動取得し、4変数別スコアを記録する

---

# 🔑 初回セットアップ(1回だけ)

## STEP 1:Google Cloud プロジェクト作成

```
1. https://console.cloud.google.com/ にログイン
2. 上部「プロジェクトを選択」→「新しいプロジェクト」
3. 名前:「引き寄せラボ Analytics」→ 作成
```

## STEP 2:API を有効化

```
1. 左メニュー「APIとサービス」→「ライブラリ」
2. 検索して、以下2つを有効化:
   ・YouTube Analytics API
   ・YouTube Data API v3
```

## STEP 3:OAuth 同意画面の設定

```
1. 「APIとサービス」→「OAuth同意画面」
2. ユーザータイプ:外部 → 作成
3. アプリ名:「引き寄せラボ Analytics」
4. サポートメール:自分のGmail
5. テストユーザーに、自分のGoogleアカウント(引き寄せラボchannel保有)を追加
   ※ これを忘れるとアクセスできない
6. 保存
```

## STEP 4:認証情報(client_secret.json)発行

```
1. 「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「OAuthクライアントID」
3. アプリの種類:「デスクトップアプリ」
4. 名前:任意 → 作成
5. 「JSONをダウンロード」
6. ダウンロードしたファイルを「client_secret.json」に改名
7. このファイルを analytics/ フォルダに置く
   (youtube_analytics_daily.py と同じ場所)
```

## STEP 5:ライブラリインストール

```bash
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

## STEP 6:初回実行(ブラウザ認証)

```bash
cd dashboard/funnel/youtube_channel/analytics
python youtube_analytics_daily.py

→ ブラウザが開く → 引き寄せラボのGoogleアカウントでログイン
→ 「このアプリは確認されていません」→ 詳細 → 続行(自分のアプリなので安全)
→ 権限を許可
→ token.json が自動生成される(以降はブラウザ認証不要)
```

成功すると:
```
daily_2026-MM-DD.md が生成される
_history.csv が生成される
```

---

# 🔁 毎日の自動実行(タスクスケジューラ登録)

## Windows タスクスケジューラ

```
1. 「タスクスケジューラ」を開く
2. 「基本タスクの作成」
3. 名前:「引き寄せラボ Analytics 日次」
4. トリガー:毎日 → 朝7:00
5. 操作:プログラムの開始
   プログラム:python(またはpythonの絶対パス)
   引数:youtube_analytics_daily.py
   開始(作業フォルダ):
     C:\Users\yanagi\antigravity\hikiyose_business\success_school\dashboard\funnel\youtube_channel\analytics
6. 完了
```

→ 以降、毎朝7:00に自動でその日のレポートが生成されます。

---

# 🤖 PDCAの回し方(AIとの連携)

```
[毎朝・自動] スクリプトが daily_YYYY-MM-DD.md を生成
       ↓
[Kenji] 私(AI)に「今日の分析して」と一声 or ファイルを見せる
       ↓
[AI] daily_*.md + _history.csv を読んで:
     ・変数別(サムネ/タイトル/台本/企画)の勝敗を診断
     ・_PERFORMANCE_INSIGHTS.md を更新
     ・次に作るべき pkg と「検証する1変数」を提案
       ↓
[AI] pkg_NN を制作 → Kenjiがアップ → ループ
```

---

# 🛠 トラブルシューティング

```
「client_secret.json がありません」
  → STEP 4 のファイルを analytics/ に置く

「アクセスがブロックされました」
  → STEP 3 のテストユーザーに自分のアカウントを追加したか確認

「impressionClickThroughRate が取れない」
  → 動画公開直後はインプレ・CTRが未集計の場合あり(数日待つ)

SSL証明書エラー
  → pip install --upgrade certifi
```

---

# 📊 取得される指標と変数の対応

```
CTR(impressionClickThroughRate)  → サムネ/タイトル/企画 の診断
平均視聴率(averageViewPercentage) → 台本(特に冒頭)の診断
インプレッション(impressions)     → ジャンル一貫性/企画需要 の規模
視聴回数・登録者増                 → 総合結果

しきい値(初期目安・要調整):
  CTR 5%以上=◎ / 2%未満=要改善
  平均視聴率 40%以上=◎ / 25%未満=要改善
```

---

*アナリティクス・セットアップ手順 / 2026-05-25*
