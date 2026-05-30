"""桜木プロフィールの「外資系」→「日系企業」一括修正"""
import io, sys
from pathlib import Path

# Windows console UTF-8出力
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 順番が重要(長いパターンから処理)
replacements = [
    # 「外資系企業」系
    ("外資系企業20年勤務", "日系企業で20年勤務"),
    ("外資系企業 20年勤務", "日系企業で20年勤務"),
    ("外資系企業で20年勤務", "日系企業で20年勤務"),
    ("外資系企業に就職", "日系企業に就職"),
    ("外資系企業20年", "日系企業で20年"),
    ("外資系企業 20年", "日系企業で20年"),
    ("外資系企業で20年", "日系企業で20年"),
    ("外資系企業", "日系企業"),
    # 「外資系20年」「外資20年」系
    ("外資系20年勤務", "日系企業で20年勤務"),
    ("外資系20年", "日系企業で20年"),
    ("外資20年勤務", "日系企業で20年勤務"),
    ("外資20年", "日系企業で20年"),
    # 「外資の競争」「外資で働いて」「外資の~」系
    ("外資の終わらない競争", "日々の終わらない競争"),
    ("外資の競争", "日々の競争"),
    ("外資で働いて", "日系企業で働いて"),
    # フォールバック
    ("外資", "日系企業"),
]

base = Path(r"C:\Users\yanagi\antigravity\hikiyose_business\success_school\dashboard")

# Grep で見つかった全15ファイル
files = [
    "method/method_v3_slides.md",
    "method/sakuragi_method_v3_complete.md",
    "method/sakuragi_method_v2_5hari.md",  # 念のため
    "method/sakuragi_ai_loop_method.md",  # 念のため
    "method/method_competitive_analysis.md",  # 念のため
    "book/kindle_5hari_complete.md",
    "program/phase1_video_scripts.md",
    "program/3month_program_design.md",  # 念のため
    "events/2026_summit_preparation.md",
    "starter_kit/00_account_setup_checklist.md",
    "starter_kit/01_claude_project_prompts.md",
    "starter_kit/02_first_week_x_posts.md",
    "starter_kit/03_free_pdf_content.md",
    "starter_kit/04_landing_page_copy.md",
    "starter_kit/06_line_setup_guide.md",
    "starter_kit/08_first_content_pieces.md",
    "6month_solo_ai_action_plan.md",
    "funnel/seminar_1000yen_generator_spec.md",
    "funnel/sakuragi_seminar_1000yen_slides.md",
    "jv_mtg_2026-05-21_impact_analysis.md",  # 念のため
]

total_changes = 0
for fname in files:
    fpath = base / fname
    if not fpath.exists():
        print(f"  SKIP (not found): {fname}")
        continue
    text = fpath.read_text(encoding='utf-8')
    original = text
    file_changes = 0
    for old, new in replacements:
        count_before = text.count(old)
        if count_before > 0:
            text = text.replace(old, new)
            file_changes += count_before
    if text != original:
        fpath.write_text(text, encoding='utf-8')
        print(f"  UPDATED ({file_changes} hits): {fname}")
        total_changes += file_changes
    else:
        print(f"  no change: {fname}")

print(f"\nTotal replacements across all files: {total_changes}")
