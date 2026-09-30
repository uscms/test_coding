"""dirtree —— 目录分析器（只用标准库）

用法：
    python dirtree.py <目录>              统计文件数/目录数/总大小，列出最大的 5 个文件
    python dirtree.py <目录> --ext        额外按扩展名分组统计
"""
import os
import sys


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return "%.1f %s" % (n, unit)
        n /= 1024.0
    return "%.1f GB" % n


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    target = argv[0]
    if not os.path.isdir(target):
        print("不是目录或不存在：%s" % target)
        return 1
    files, dirs, total, by_ext = [], 0, 0, {}
    for cur, ds, fs in os.walk(target):
        dirs += len(ds)
        for name in fs:
            fp = os.path.join(cur, name)
            try:
                sz = os.path.getsize(fp)
            except OSError:
                continue
            files.append((sz, fp))
            total += sz
            ext = os.path.splitext(name)[1].lower() or "(无扩展名)"
            e = by_ext.setdefault(ext, [0, 0])
            e[0] += 1
            e[1] += sz
    print("目录：%s" % target)
    print("文件 %d 个，子目录 %d 个，总大小 %s" % (len(files), dirs, human(total)))
    print("\n最大的 5 个文件：")
    for sz, fp in sorted(files, reverse=True)[:5]:
        print("  %-10s %s" % (human(sz), fp))
    if "--ext" in argv:
        print("\n按扩展名统计：")
        for ext, (cnt, sz) in sorted(by_ext.items(), key=lambda x: -x[1][1])[:10]:
            print("  %-12s %d 个  %s" % (ext, cnt, human(sz)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
