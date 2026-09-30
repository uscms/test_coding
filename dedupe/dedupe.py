"""dedupe —— 按内容哈希找出重复文件（只用标准库）

用法：
    python dedupe.py <目录>               列出重复文件分组
    python dedupe.py <目录> --delete      删除重复项（每组保留一个），删除前会再确认
"""
import hashlib
import os
import sys


def sha256(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    target = argv[0]
    if not os.path.isdir(target):
        print("不是目录或不存在：%s" % target)
        return 1
    groups = {}
    for cur, _ds, fs in os.walk(target):
        for name in fs:
            fp = os.path.join(cur, name)
            try:
                if os.path.getsize(fp) == 0:
                    continue
                groups.setdefault(sha256(fp), []).append(fp)
            except OSError:
                pass
    dups = {k: v for k, v in groups.items() if len(v) > 1}
    if not dups:
        print("没有发现重复文件。")
        return 0
    print("发现 %d 组重复文件：\n" % len(dups))
    for _k, paths in dups.items():
        print("  重复组（保留 %s）：" % paths[0])
        for p in paths[1:]:
            print("      可删除 %s" % p)
    if "--delete" in argv:
        ans = input("\n确认删除每组的重复项？输入 yes 继续：")
        if ans.strip().lower() != "yes":
            print("已取消，未删除任何文件。")
            return 0
        n = 0
        for _k, paths in dups.items():
            for p in paths[1:]:
                try:
                    os.remove(p)
                    n += 1
                except OSError as e:
                    print("删除失败 %s：%s" % (p, e))
        print("已删除 %d 个重复文件。" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
