# 🚀 ローカル作業キックスタートガイド

> **本ドキュメントの使い方:** ローカル環境(Claude Code, Cursor等)で作業を開始する際の「ずっと使えるスタートキット」
> **作成日:** 2026-05-16

---

# 📘 ステップ1: リポジトリクローン

```bash
# 作業ディレクトリ作成
mkdir -p ~/projects/hikiyose_business
cd ~/projects/hikiyose_business

# リポジトリクローン
git clone https://github.com/kenjisakuragi/success_school.git
cd success_school

# 作業ブランチに切り替え
git checkout claude/personal-management-dashboard-LKkCF

# 状態確認
git status
git log --oneline -10
```

---

# ⚙️ ステップ2: 推奨環境セットアップ

## 必須ツール
- **Claude Code**(もしくはCursor)
- VS Code
- Git
- Node.js (LP修正用)
- ブラウザ(Chrome/Edge)

## 推奨設定
```bash
# Claude Code設定例(~/.claude/settings.json)
{
  "projectRoot": "~/projects/hikiyose_business/success_school",
  "defaultModel": "claude-opus-4",
  "autoSync": true
}
```

## アカウント準備(今週中)

| サービス | 用途 | URL |
|---|---|---|
| ElevenLabs | AI音声生成 | elevenlabs.io |
| Vrew | 動画編集 | vrew.voyagerx.com |
| Canva Pro | ザブトン・サムネ | canva.com |
| Notion | ソースDB | notion.so |
| Brevo | メルマガ・ステップメール | brevo.com |
| YouTube Studio | チャンネル開設 | studio.youtube.com |
| Anthropic API | Claude API | console.anthropic.com |

---

# 📂 ステップ3: 推奨ローカルフォルダ構造

```
~/projects/hikiyose_business/
├─ success_school/        ★ GitHubリポジトリ(クローン済み)
│  ├─ dashboard/         ★ 全設計書(作業の中心)
│  └─ docs/              ★ LP
│
├─ production/          ⚭ 新規:動画制作作業ディレクトリ
│  ├─ scripts/          台本mdファイル
│  ├─ audio/            ElevenLabs生成mp3
│  ├─ video/            Vrew作業ファイル
│  ├─ images/           胖像画ストック
│  └─ thumbnails/       サムネデザイン
│
├─ reference/           ⚭ 参考資料
│  ├─ books/            偊人原書ファイル
│  ├─ audio/            オーディオブック
│  └─ papers/           脳科学論文
│
└─ sandbox/            ⚭ 試作・一時作業
   ├─ prompts/         プロンプト試作
   └─ experiments/     検証・効果チェック
```

---

# 📝 ステップ4: ローカル作業の最初の指示プロンプト

## コピペスタしてClaude Codeに貼り付けて使用

```
【プロンプトコピペスタスタート】—————————————————————————

こんにちは。本セッションでは、「引き寄せ博士」ブランドを中心とした
自己啓発・スピリチュアル系のYouTube + コンテンツビジネスを担当してもらいます。

【作業環境】
リポジトリ: kenjisakuragi/success_school
ブランチ: claude/personal-management-dashboard-LKkCF
作業中心: dashboard/フォルダ

【最初にしてもらうこと】
以下3つのファイルを順番に読んで、現状を把握してください。

1. dashboard/session_handoff.md(引き継ぎドキュメント・最重要)
2. dashboard/00_MASTER_BRIEF.md(全体サマリー)
3. dashboard/founder_profile_final.md(クライアントプロフィール)

読んだ上で、「現在の進捗状況をサマリーして、今日やらない
といけない作業3-4つを選択肢として提示」してください。

【重要ルール】
- 現在のブランチで作業、mainにはマージしない
- 重要決定は独断せずクライアントに3-4選択肢を提示して判断を仰ぐ
- コミットは日本語、Conventional Commits(feat:, fix:, docs:)を遵守
- 大きな変更はドキュメントも同時更新
- session_handoff.md の「タブー」・「トーンガイド」を厳守

【今週の優先タスク】3つを2-3選択肢として提示してください:

A. サンプル台本5〜10をフル拡張(現状トピックスクリプトのみ)
B. PoC 2週間検証計画を実施可能レベルに詳細化
C. ソースバンク初期Notion設計テンプレート作成
D. VrewとElevenLabsのセットアップ手順書作成
E. 100タイトルバンクからとりあえず作る10本を選定

クライアントからの追加指示を待ちましょう。

——————————————————————————————————————————
```

---

# 🔥 ステップ5: 必読ドキュメントチェックリスト

クライアントと以下を事前に共有してもらうと効率UP:

## 学長強推(読ませたいファイル)
- [ ] `dashboard/session_handoff.md`
- [ ] `dashboard/00_MASTER_BRIEF.md`
- [ ] `dashboard/founder_profile_final.md`
- [ ] `dashboard/100m_systemization_checklist.md`

## YouTube関連作業の際
- [ ] `dashboard/youtube/script_production_system_5layers.md`
- [ ] `dashboard/youtube/simple_format_production_design.md`
- [ ] `dashboard/youtube/sample_scripts_10.md`
- [ ] `dashboard/youtube/100_video_titles_2segments.md`
- [ ] `dashboard/youtube/great_minds_safe_30_list.md`

## セミナー/本科関連の際
- [ ] `dashboard/funnel/seminar_design_v3_integrated.md`
- [ ] `dashboard/funnel/seminar_slides_v2_spi_women.md`
- [ ] `dashboard/funnel/upsell_slides_v2_spi_women.md`
- [ ] `dashboard/program/dream_program_12sessions_v2_spi_women.md`

## サブスク関連の際
- [ ] `dashboard/subscription/subscription_satisfaction_design.md`
- [ ] `dashboard/subscription/ai_voice_implementation_plan.md`
- [ ] `dashboard/subscription/subscription_kpi_dashboard.md`

## 不労所得関連の際
- [ ] `dashboard/passive_income/passive_income_5_tier_design.md`
- [ ] `dashboard/passive_income/24month_roadmap.md`
- [ ] `dashboard/passive_income/online_course_design.md`
- [ ] `dashboard/passive_income/udemy_5_course_outline.md`

## 書籍執筆の際
- [ ] `dashboard/book/kindle_01_manuscript_part1.md`
- [ ] `dashboard/book/kindle_01_manuscript_part2.md`
- [ ] `dashboard/book/kindle_01_prologue_v2.md`
- [ ] `dashboard/kindle_publishing_playbook.md`

---

# 🎯 ステップ6: 1セッションの効果的な進め方

## 「今日何をやるか」を陸明確に
```
例1: 「今日はサンプル台本5、6、7をフル拡張したい」
例2: 「今日はNotionソースDBの初期設計を作りたい」
例3: 「今日はJV提案資料をライブ説明可能レベルに仕上げたい」
```

## 1セッションの推奨長さ
- 30-90分 がベスト
- 1つのジャンルに集中
- 3-5個のサブタスクデ進める

## セッション終わりのチェック
```
クライアント: 「今日の作業のサマリーと、次回もしされる作業を
         3つの選択肢として提示して、session_handoff.mdを
         更新してください」
```

---

# 🛑 ステップ7: トラブルシューティング

## クライアントがブランドから逸脱しそうになったら
```
「session_handoff.md の「タブー」セクションを一度見直して、
もう一度検討してくれますか」
```

## 重要決定をクライアントに守り許されそうになったら
```
「これは事業の主軸に関わる重要決定だと思うので、
多法重と選択肢を提示して、効果とトレードオフを明示するように
お願いします」
```

## 作業がぜんぜん進まないとき
```
「一ダス、一現在の仕業をストップして、「どこで詰まっているか」
を明記して、代替アプローチ2-3つを提示して下さい」
```

---

# 📞 ステップ8: サポート・参考資料

## 公式ドキュメント
- Claude Code: https://docs.claude.com/claude-code
- Anthropic API: https://docs.anthropic.com
- ElevenLabs: https://elevenlabs.io/docs
- Vrew: https://vrew.voyagerx.com/ja

## トラブル時の参考ファイル
- `dashboard/session_handoff.md` (人守ルール)
- `dashboard/00_MASTER_BRIEF.md` (全体把握)
- `dashboard/100m_systemization_checklist.md` (何を選ぶかの原則)

---

# 🏁 今すぐローカル作業を始める3ステップ

## 1つ目:リポジトリをクローン(3分)
```bash
git clone https://github.com/kenjisakuragi/success_school.git
cd success_school
git checkout claude/personal-management-dashboard-LKkCF
```

## 2つ目:Claude Codeを起動(1分)
```bash
cd success_school
claude
```

## 3つ目:上記「ステップ4のプロンプト」をコピペスト(1分)
初期プロンプトを貼り付けてEnter。クライアントが現状を把握して提案を返します。

---

# 💡 推奨セッションスケジュール(例)

## 週末(会社休みの日)
- 週末1回・90分:重要作業集中(台本レビュー、戦略検討等)
- セッション后に、session_handoff.mdを更新

## 平日夜
- 30分セッション(タスク進捗・レビュー)
- 1つのサブタスクに集中

## 朝の30分
- AI生成タスクを代して、学長は認可のみ
- 例:台本作成・サムネ生成・ステップメール作成等

---

# 📦 現在のファイルサムリー(参照用)

## 計画・戦略(8ファイル)
- session_handoff.md ★スタート点
- 00_MASTER_BRIEF.md
- founder_profile_final.md
- 100m_systemization_checklist.md
- business_principles.md
- todo.md
- knowledge_base.md
- today_decisions_2026-05-15.md

## YouTubeを動画量産関連(7ファイル)
- youtube/100_video_titles_2segments.md
- youtube/great_minds_safe_30_list.md
- youtube/mass_production_system.md
- youtube/simple_format_production_design.md
- youtube/sample_scripts_10.md
- youtube/script_production_system_5layers.md

## ファネル(セミナー・本科・サブスク・不労)
- funnel/seminar_design_v3_integrated.md ⚭NEW(本日)
- funnel/seminar_slides.md
- funnel/seminar_slides_v2_spi_women.md
- funnel/upsell_slides.md
- funnel/upsell_slides_v2_spi_women.md
- program/dream_program_12sessions.md
- program/dream_program_12sessions_v2_spi_women.md
- subscription/subscription_satisfaction_design.md
- subscription/ai_voice_implementation_plan.md
- subscription/subscription_kpi_dashboard.md
- passive_income/passive_income_5_tier_design.md
- passive_income/24month_roadmap.md
- passive_income/online_course_design.md
- passive_income/udemy_5_course_outline.md

## 書籍執筆(5ファイル)
- book/kindle_01_manuscript_part1.md
- book/kindle_01_manuscript_part2.md
- book/kindle_01_prologue_v2.md
- book/chapter_3_why_hidden.md
- book/kindle_02_general_outline_part1.md

## LP・GitHub Pages公開用(2ファイル)
- docs/index.html
- docs/SETUP.md

## メソッド体系(7ファイル)
- method/00_overview.md
- method/01_cognitive_dissonance.md
- method/02_references.md
- method/03_ai_integration.md
- method/04_synthesis.md
- method/references/daigo.md
- method/references/napoleon_hill.md

## セールスフレーム(5ファイル)
- urgency_framing_strategy.md
- environment_pacemaker_frame.md
- frame_7_coffee_per_day_for_kids.md
- selling_frames_catalog.md
- copy_candidates.md

## オペレーション・取材・コピー(10ファイル+)
- jv_proposal_v1.md
- backend_products_pricing.md
- customer_acquisition_strategy.md
- money_flow_blueprint.md
- business_expansion_roadmap.md
- positioning_keywords.md
- positioning_risk_assessment.md
- daily_happiness_goals.md
- founder_achievements_fixed.md
- kindle_publishing_playbook.md
- dream_program_v1.md

**合計:50+ 設計ファイル**

---

*本ドキュメントを使えば、クライアントはどのセッションでも、どこからでも、作業を再開できる。*
