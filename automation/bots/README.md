# automation/bots/

AIコーチBot・FAQ Bot等の実装ファイル群。

## 想定構造
- `lv2_ai_coach/`:LV2購入者向け30日伴走Bot
- `lv3_community_bot/`:LV3コミュニティ専用無制限Bot
- `faq_bot/`:LV2向け24h FAQ Bot
- `line_official/`:LINE公式アカウントのステップ配信

## 実装方針
- プロンプトは `automation/prompts/` を参照
- API利用は最小限の構成(Anthropic SDK / Claude API)
- 月次でログを review して、応答品質を改善

詳細:CLAUDE.md §9
