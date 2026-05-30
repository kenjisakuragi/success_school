# 📜 書き起こし取得フロー(案B採用)

**確定:** 2026-05-24
**目的:** 海外人気動画の実書き起こしを Kenji がローカルで自動取得 → AIが台本に反映

---

# 🔄 全体フロー

```
[1] Kenji: YouTube で対象動画を3-5本ピックアップ
            ↓
[2] Kenji: research/pkg_NN_urls.txt にURL貼り付け(1分)
            ↓
[3] Kenji: python _fetch_transcripts.py pkg_NN(30秒)
            ↓
[4] スクリプト: research/pkg_NN_transcripts.md に書き起こし保存
            ↓
[5] Kenji: 「pkg_NN の台本書いて」と私(AI)に投げる
            ↓
[6] 私: 実書き起こしを読み込んで台本生成
```

→ Kenji の所要時間 **3-5分** で実書き起こしベースの台本が作れる体制。

---

# 🛠 初回セットアップ(1回だけ)

## Pythonライブラリのインストール

```bash
pip install youtube-transcript-api
```

それだけです。

---

# 📋 運用手順(毎回)

## STEP 1:対象動画をピックアップ(5分)

```
YouTubeで検索キーワード:
  "scripting manifestation" / "manifesting tutorial"
  "369 method" / "lucky girl syndrome"
  "void state" / "whisper method" 等

選定基準:
  ・再生数が多い(10万以上推奨)
  ・直近2年以内に公開
  ・字幕(CC)がオンにできる(必須)
  ・3-5本ピックアップして多角的に
```

## STEP 2:URLを記入

`research/pkg_NN_urls.txt` を開いて、対象URLを1行ずつ書く:

```
# pkg_01 Lucky Girl Syndrome
https://www.youtube.com/watch?v=ABCDEFG1234
https://www.youtube.com/watch?v=HIJKLMN5678
https://youtu.be/OPQRSTU9012
# このような # で始まる行はコメントとして無視されます
```

## STEP 3:取得実行

```bash
cd dashboard/funnel/content_factory
python _fetch_transcripts.py pkg_01
```

実行結果の例:
```
対象動画数: 3
[1/3] ABCDEFG1234 取得中... OK (412 segments, 5234 chars)
[2/3] HIJKLMN5678 取得中... OK (387 segments, 4891 chars)
[3/3] OPQRSTU9012 取得中... OK (255 segments, 3120 chars)

保存: research/pkg_01_transcripts.md
成功: 3/3
```

## STEP 4:AIに台本生成を依頼

私(AI)に下記のように投げる:

```
pkg_01 の YouTube台本を、v3.1 仕様で書いて。

リサーチメモは research/pkg_01_transcripts.md にある。
書き起こしから「視聴者の典型的な悩みフック」と「核心メソッドの主張」を抽出して、
科学的にバンデューラの自己効力感に橋渡しして。
```

私が `research/pkg_01_transcripts.md` を読み込み、書き起こしを元に v3.1 仕様で台本を生成します。

---

# ⚠️ トラブルシューティング

## 「字幕が取得できません」と出る場合

```
原因:
  ・対象動画に英語字幕がない(自動生成も無効化されている)
  ・地域制限がかかっている
  ・動画が非公開・削除済み

対策:
  ・別の動画に差し替え
  ・urls.txt から該当行を削除して再実行
```

## SSL証明書エラーが出る場合

```
PowerShellの場合は、環境変数で証明書バンドルを指定:
  $env:REQUESTS_CA_BUNDLE = "C:\path\to\ca-bundle.crt"

または、企業ネットワーク外で実行
```

---

# 📊 リサーチメモ更新ルール(v3.1)

`research/pkg_NN_source.md` は引き続き「桜木式翻訳マップ」として使う:

```markdown
# pkg_NN リサーチメモ v3.1

## 1. 対象動画リスト
(pkg_NN_urls.txt と pkg_NN_transcripts.md を参照)

## 2. 書き起こしから抽出した「典型的主張」(AIが整理)
- 主張1:[書き起こしから]
- 主張2:[書き起こしから]

## 3. 視聴者の典型的悩み(コメント欄から推測 or 書き起こしから)
- 悩み1:〇〇できない
- 悩み2:〇〇が続かない

## 4. 桜木式翻訳マップ
- 海外メソッド → 心理学用語
- 該当する研究(8研究リストから)

## 5. タイトル候補(5型から)
- [採用]
- [差し替え1]
- [差し替え2]
```

---

# 🎯 なぜ案Bを採用したか

```
✅ Kenji の作業時間が最小(3-5分)
✅ 実書き起こしを参照するので、台本の説得力が桁違い
✅ ライブラリは無料・著作権問題なし(字幕は公開データ)
✅ Pythonさえあれば動く(WinでもMacでも)
✅ pkg_NN 単位でバッチ処理可能
✅ サンドボックス制約を回避(ローカル実行)

❌ 私(AI)が直接YouTubeにアクセスする方法は、
   サンドボックスのSSL/権限制限で不安定だった
```

---

*書き起こし取得フロー v1.0 / 2026-05-24 / 案B確定*
