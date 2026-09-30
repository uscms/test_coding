"""jsonfmt —— 命令行 JSON 工具（只用标准库）

用法：
    python jsonfmt.py <file.json>            格式化打印（缩进 2 空格）
    python jsonfmt.py <file.json> --minify   压缩成一行
    python jsonfmt.py <file.json> --check    只校验是否合法
"""
import json
import sys


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    path, flags = argv[0], set(argv[1:])
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print("读取失败：%s" % e)
        return 1
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print("JSON 不合法：%s" % e)
        return 1
    if "--check" in flags:
        print("JSON 合法")
        return 0
    if "--minify" in flags:
        print(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
