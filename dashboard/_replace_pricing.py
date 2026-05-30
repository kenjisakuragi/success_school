"""
価格統一スクリプト(2026-05-22 桜木ブランド)

- 本科 ¥100,000 → ¥98,000
- VIP  ¥300,000 → ¥298,000
- 6名限定 → 1on1パーソナル

文脈付き複合パターンで誤爆を防ぐ(¥100,000 / ¥300,000 単独は触らない)。
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # success_school/

REPLACEMENTS: list[tuple[str, str]] = [
    # ── 本科 ¥100,000 → ¥98,000(文脈付き) ──
    ("¥100,000本科", "¥98,000本科"),
    ("本科 ¥100,000", "本科 ¥98,000"),
    ("Standard ¥100,000", "Standard ¥98,000"),
    ("Standard本科 ¥100,000", "Standard本科 ¥98,000"),
    ("本科Standard ¥100,000", "本科Standard ¥98,000"),
    ("¥100,000(Standard)", "¥98,000(Standard)"),
    ("¥100,000(分割", "¥98,000(分割"),
    ("¥100,000(税込)", "¥98,000(税込)"),
    ("¥100,000(税込) または ¥10,000 × 10回分割",
     "¥98,000(税込) または分割30回 ¥3,267/月〜"),
    ("¥100,000 ÷ 90日", "¥98,000 ÷ 90日"),
    ("¥100,000 ÷ 1名あたりLTV", "¥100,000 ÷ 1名あたりLTV"),  # サブスクLTV(変更しない)
    ("# ¥100,000", "# ¥98,000"),
    ("本科 ¥100,000-300,000", "本科 ¥98,000-298,000"),
    ("¥100,000(3ヶ月)", "¥98,000(3ヶ月)"),
    ("¥100,000-300,000(3ヶ月)", "¥98,000-298,000(3ヶ月)"),
    ("¥100,000本科第", "¥98,000本科第"),  # session_handoff
    ("¥100,000本科「", "¥98,000本科「"),
    ("¥100,000本科『", "¥98,000本科『"),
    ("¥100,000本科への", "¥98,000本科への"),
    ("¥100,000本科に ", "¥98,000本科に "),
    ("3ヶ月の伴走:        ¥100,000相当", "3ヶ月の伴走:        ¥98,000相当"),  # 価値スタック内
    ("3ヶ月の伴走サポート ............ ¥100,000相当",
     "3ヶ月の伴走サポート ............ ¥98,000相当"),
    ("3ヶ月の全体サポート ............ ¥100,000相当",
     "3ヶ月の全体サポート ............ ¥98,000相当"),
    ("3ヶ月12回のLIVE伴走 | ¥100,000相当",
     "3ヶ月12回のLIVE伴走 | ¥98,000相当"),
    ("これを今夜、¥100,000で。", "これを今夜、¥98,000で。"),
    ("¥213,000相当のパッケージを ¥100,000", "¥211,000相当のパッケージを ¥98,000"),
    ("¥212,000相当のパッケージを ¥100,000", "¥210,000相当のパッケージを ¥98,000"),
    ("価格は同じ¥100,000", "価格は同じ¥98,000"),
    ("価格 ¥100,000", "価格 ¥98,000"),
    ("# Standard本科 ¥100,000 → 12月末まで¥80,000",
     "# Standard本科 ¥98,000 → 12月末まで¥78,000"),
    ("Standard本科 ¥100,000 → 12月末まで¥80,000",
     "Standard本科 ¥98,000 → 12月末まで¥78,000"),
    ("- 本科Standard ¥100,000 → 12月末まで¥80,000",
     "- 本科Standard ¥98,000 → 12月末まで¥78,000"),
    ("¥100,000本科は価値価格", "¥98,000本科は価値価格"),
    ("¥100,000本科への", "¥98,000本科への"),
    ("PRICE_STANDARD: \"¥100,000\"", "PRICE_STANDARD: \"¥98,000\""),
    ("AI寄り添いコーチ Standard: 20名(¥100,000/月)",
     "AI寄り添いコーチ Standard: 20名(¥100,000/月)"),  # 別商品(コーチ商品) - 触らない
    ("Standard本科 ¥100,000 × 15名/月 = ¥1,500,000",
     "Standard本科 ¥98,000 × 15名/月 = ¥1,470,000"),
    ("¥100,000(3ヶ月12回・限定30名)",
     "¥98,000(3ヶ月12回・限定30名)"),
    ("12回プログラム ¥100,000", "12回プログラム ¥98,000"),

    # ── VIP ¥300,000 → ¥298,000(文脈付き) ──
    ("¥300,000(VIP)", "¥298,000(1on1 VIP)"),
    ("VIP ¥300,000", "1on1 VIP ¥298,000"),
    ("VIP: ¥300,000", "1on1 VIP: ¥298,000"),
    ("¥300,000(分割¥8,334", "¥298,000(分割¥8,278"),
    ("¥300,000(分割 ¥8,334", "¥298,000(分割 ¥8,278"),
    ("¥300,000(分割¥8334", "¥298,000(分割¥8,278"),
    ("¥300,000(分割 ¥8334", "¥298,000(分割 ¥8,278"),
    ("¥300,000 → 12月末まで¥250,000", "¥298,000 → 12月末まで¥248,000"),
    ("¥300,000(VIP)", "¥298,000(1on1 VIP)"),
    ("PRICE_VIP: \"¥300,000\"", "PRICE_VIP: \"¥298,000\""),
    ("¥300,000高単価", "¥298,000高単価"),
    ("¥100,000(Standard) / ¥300,000(VIP)",
     "¥98,000(Standard) / ¥298,000(1on1 VIP)"),
    ("¥300,000 × 3名/月 = ¥900,000",
     "¥298,000 × 3名/月 = ¥894,000"),
    ("AIマニフェスティング本科VIP | ¥300,000",
     "AIマニフェスティング 1on1 VIP | ¥298,000"),
    ("VIP本科 ¥300,000", "1on1 VIP ¥298,000"),
    ("AIマニフェスティング本科VIP ¥300,000",
     "AIマニフェスティング 1on1 VIP ¥298,000"),
    ("→ AIマニフェスティング本科VIP | ¥300,000",
     "→ AIマニフェスティング 1on1 VIP | ¥298,000"),

    # ── 6名限定 → 1on1パーソナル ──
    ("(6名限定)", "(1on1パーソナル)"),
    ("・6名限定", "・本科の中から1〜3名のみ"),
    ("6名限定での濃密な集合セッション", "本科に組み込まれた、桜木との完全1on1セッション"),
    ("**6名のみ**", "**本科の中から1〜3名**"),
    ("VIP詳細(6名限定)", "1on1 VIP詳細(本科内特別枠)"),
]

# 桜木プロダクト以外の ¥100,000 / ¥300,000 が含まれる「触らないファイル」
EXCLUDE_FILES = {
    "MASTER_DECISIONS_2026-05-22.md",  # 移行履歴
    "PHASE2_DECISIONS_2026-05-22.md",  # 移行履歴
    "_replace_master_v2.py",
    "_replace_pricing.py",
    "kindle_publishing_playbook.md",   # BookCoverデザイン費(無関係)
    "frame_7_coffee_per_day_for_kids.md",  # 受験家族
    "6month_sprint_to_3m.md",          # 月売上目標
    "business_expansion_roadmap.md",   # 受験家族
    "jv_proposal_v1.md",               # JV(受験事業)
    "jv_proposal_skeleton.md",         # JV(受験事業)
    "love_partnership_design_principles.md",  # 別商品提案
    "kindle_01_manuscript_part2.md",   # 旧書籍原稿
    "kindle_01_manuscript_part1.md",   # 旧書籍原稿
}

TARGET_EXTS = {".md", ".txt"}


def iter_target_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TARGET_EXTS:
            continue
        if p.name in EXCLUDE_FILES:
            continue
        files.append(p)
    return files


def apply_replacements(text: str) -> tuple[str, list[tuple[str, int]]]:
    stats: list[tuple[str, int]] = []
    new_text = text
    for old, new in REPLACEMENTS:
        if old == new:
            continue
        count = new_text.count(old)
        if count:
            new_text = new_text.replace(old, new)
            stats.append((old, count))
    return new_text, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args()

    files = iter_target_files()
    changed_files: list[tuple[Path, list[tuple[str, int]]]] = []
    grand: dict[str, int] = {}
    total = 0

    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new_text, stats = apply_replacements(text)
        if not stats:
            continue
        for o, c in stats:
            grand[o] = grand.get(o, 0) + c
            total += c
        changed_files.append((fp, stats))

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== 価格統一 [{mode}] ===")
    print(f"スキャン: {len(files)} / 変更対象: {len(changed_files)} / 計 {total} 置換\n")

    print("--- 用語別ヒット ---")
    for old, _ in REPLACEMENTS:
        c = grand.get(old, 0)
        if c:
            new = dict(REPLACEMENTS)[old]
            print(f"  {old!r:55s} -> {new!r}  : {c}")
    print()

    print("--- ファイル別 ---")
    for fp, stats in changed_files:
        rel = fp.relative_to(ROOT)
        breakdown = ", ".join(f"{o[:30]}...×{c}" if len(o) > 30 else f"{o}×{c}"
                              for o, c in stats)
        print(f"  {rel}  [{breakdown}]")

    if not args.apply:
        print("\n(dry-run。--apply で本実行)")
        return 0

    if not args.no_backup and total:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = ROOT.parent / f"_backup_pricing_{ts}"
        shutil.copytree(ROOT, backup)
        print(f"\nバックアップ: {backup}")

    for fp, _ in changed_files:
        text = fp.read_text(encoding="utf-8")
        new_text, _ = apply_replacements(text)
        fp.write_text(new_text, encoding="utf-8")
        print(f"  書き込み: {fp.relative_to(ROOT)}")

    print(f"\n完了: {len(changed_files)} ファイル / {total} 置換")
    return 0


if __name__ == "__main__":
    sys.exit(main())
