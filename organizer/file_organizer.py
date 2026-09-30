#!/usr/bin/env python3
"""
file_organizer.py — 按扩展名将目录下的文件归类到子目录。

用法:
    python3 file_organizer.py <目标目录> [--dry-run] [--apply]

不指定 --apply 时默认只打印计划（等价于 --dry-run）。
指定 --apply 时真正执行移动。
"""

import argparse
import sys
from pathlib import Path

# 扩展名 → 子目录名 映射
EXTENSION_MAP = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
        ".svg", ".webp", ".ico", ".heic", ".heif",
    },
    "Docs": {
        ".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx",
        ".ppt", ".pptx", ".csv", ".md", ".odt", ".ods", ".odp",
        ".rtf", ".tex", ".html", ".htm",
    },
    "Videos": {
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv",
        ".webm", ".m4v", ".mpg", ".mpeg", ".3gp",
    },
    "Music": {
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma",
        ".mid", ".m4a", ".opus", ".aiff",
    },
}
DEFAULT_CATEGORY = "Others"


def resolve_category(suffix: str) -> str:
    """根据文件后缀返回目标子目录名。"""
    suffix = suffix.lower()
    for cat, exts in EXTENSION_MAP.items():
        if suffix in exts:
            return cat
    return DEFAULT_CATEGORY


def unique_destination(dest_dir: Path, filename: str) -> Path:
    """若目标路径已存在，则自动追加 _1, _2, ... 后缀直到不冲突。"""
    target = dest_dir / filename
    if not target.exists():
        return target

    stem = target.stem
    suffix = target.suffix
    counter = 1
    while True:
        candidate = dest_dir / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def collect_files(target_dir: Path):
    """收集目标目录下的所有普通文件（不递归，跳过子目录）。"""
    files = []
    for entry in sorted(target_dir.iterdir()):
        if entry.is_file():
            files.append(entry)
    return files


def plan_moves(target_dir: Path):
    """生成移动计划列表: [(src, dst), ...]"""
    moves = []
    for src in collect_files(target_dir):
        # 跳过本工具自身和隐藏文件
        if src.name == "file_organizer.py":
            continue
        if src.name.startswith("."):
            continue

        category = resolve_category(src.suffix)
        dest_dir = target_dir / category
        dst = unique_destination(dest_dir, src.name)
        moves.append((src, dst))
    return moves


def execute_moves(moves, dry_run: bool):
    """执行移动或仅打印计划。"""
    if not moves:
        print("没有需要整理的文件。")
        return 0

    action = "将移动" if dry_run else "已移动"
    print(f"\n共 {len(moves)} 个文件 {action}:\n")

    for src, dst in moves:
        if dry_run:
            print(f"  [计划] {src.name}  →  {dst.parent.name}/{dst.name}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dst)
            print(f"  [完成] {src.name}  →  {dst.parent.name}/{dst.name}")

    if dry_run:
        print(f"\n[dry-run] 未实际移动任何文件。确认无误后请加 --apply 执行。")
    else:
        print(f"\n整理完成，共移动 {len(moves)} 个文件。")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="按扩展名将文件归类到子目录 (Images / Docs / Videos / Music / Others)"
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="要整理的目标目录路径",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将要做的操作，不实际移动文件（默认行为）",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="真正执行文件移动",
    )

    args = parser.parse_args()
    target_dir = args.directory

    # 校验目录
    if not target_dir.is_dir():
        print(f"错误: '{target_dir}' 不是有效目录。", file=sys.stderr)
        sys.exit(1)

    # 默认 dry-run，除非显式指定 --apply
    dry_run = not args.apply
    if args.dry_run and args.apply:
        print("错误: --dry-run 和 --apply 不能同时使用。", file=sys.stderr)
        sys.exit(1)

    # 生成计划
    moves = plan_moves(target_dir)

    # 执行
    exit_code = execute_moves(moves, dry_run)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
