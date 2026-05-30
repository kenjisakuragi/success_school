"""
命名統一スクリプト v2  (2026-05-22 桜木賢治ブランド)

旧用語 → 新用語(AIマニフェスティング / Manifest AI)に一括置換する。
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
    ("叶える5HARI", "桜木式 AIマニフェスティング"),
    ("5HARI", "AIマニフェスティング"),
    ("フューチャーレター・ノート", "AIマニフェスティング"),
    ("Sakuragi AI", "Manifest AI"),
    ("MIRAI AI", "Manifest AI"),
]

EXCLUDE_FILES = {
    "MASTER_DECISIONS_2026-05-22.md",
    "PHASE2_DECISIONS_2026-05-22.md",
    "_replace_master_v2.py",
}

TARGET_EXTS = {".md", ".txt"}


def iter_target_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in TARGET_EXTS:
            continue
        if p.name in EXCLUDE_FILES:
            continue
        files.append(p)
    return files


def apply_replacements(text: str) -> tuple[str, list[tuple[str, int]]]:
    """Return (new_text, [(old, count_in_this_file), ...])."""
    stats: list[tuple[str, int]] = []
    new_text = text
    for old, new in REPLACEMENTS:
        count = new_text.count(old)
        if count:
            new_text = new_text.replace(old, new)
            stats.append((old, count))
    return new_text, stats


def make_backup(root: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = root.parent / f"_backup_rename_{ts}"
    shutil.copytree(root, backup_dir)
    return backup_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="実際にファイルを書き換える(指定しなければ dry-run)")
    parser.add_argument("--no-backup", action="store_true",
                        help="--apply 時のバックアップをスキップ")
    args = parser.parse_args()

    files = iter_target_files()
    total_files_changed = 0
    total_replacements = 0
    grand_stats: dict[str, int] = {}
    changed_files: list[tuple[Path, list[tuple[str, int]]]] = []

    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"[skip-non-utf8] {fp.relative_to(ROOT)}")
            continue
        new_text, stats = apply_replacements(text)
        if not stats:
            continue
        total_files_changed += 1
        for old, c in stats:
            grand_stats[old] = grand_stats.get(old, 0) + c
            total_replacements += c
        changed_files.append((fp, stats))

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== 命名統一 v2 [{mode}] ===")
    print(f"対象ルート: {ROOT}")
    print(f"スキャン: {len(files)} ファイル")
    print(f"変更対象: {total_files_changed} ファイル / 計 {total_replacements} 置換\n")

    print("--- 用語別カウント ---")
    for old, _ in REPLACEMENTS:
        c = grand_stats.get(old, 0)
        new = dict(REPLACEMENTS)[old]
        print(f"  {old!r:40s} -> {new!r:30s}  : {c}")
    print()

    print("--- ファイル別 ---")
    for fp, stats in changed_files:
        rel = fp.relative_to(ROOT)
        breakdown = ", ".join(f"{o}×{c}" for o, c in stats)
        print(f"  {rel}  [{breakdown}]")
    print()

    if not args.apply:
        print("⚠️  dry-run。実行するには --apply を付ける。")
        return 0

    if total_replacements == 0:
        print("変更なし。終了。")
        return 0

    if not args.no_backup:
        backup = make_backup(ROOT)
        print(f"📦 バックアップ作成: {backup}")

    for fp, _ in changed_files:
        text = fp.read_text(encoding="utf-8")
        new_text, _ = apply_replacements(text)
        fp.write_text(new_text, encoding="utf-8")
        print(f"✅ {fp.relative_to(ROOT)}")

    print(f"\n✨ 完了: {total_files_changed} ファイル / {total_replacements} 置換")
    return 0


if __name__ == "__main__":
    sys.exit(main())
