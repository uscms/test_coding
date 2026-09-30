"""csvreport —— CSV 统计报表（只用标准库）

用法：
    python csvreport.py <file.csv>              看表头、行数、每列的类型推断
    python csvreport.py <file.csv> --sum <列名> 对数值列求和/均值/最大/最小
"""
import csv
import os
import sys


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    src = argv[0]
    if not os.path.isfile(src):
        print("文件不存在：%s" % src)
        return 1
    with open(src, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("CSV 没有数据行。")
        return 1
    cols = list(rows[0].keys())
    print("文件：%s" % src)
    print("共 %d 行，%d 列：%s\n" % (len(rows), len(cols), "、".join(cols)))
    for c in cols:
        vals = [r[c] for r in rows if r[c] not in ("", None)]
        nums = []
        for v in vals:
            try:
                nums.append(float(v))
            except ValueError:
                pass
        if nums and len(nums) == len(vals):
            print("  %-16s 数值列：合计 %.2f，均值 %.2f，最大 %.2f，最小 %.2f"
                  % (c, sum(nums), sum(nums) / len(nums), max(nums), min(nums)))
        else:
            uniq = len(set(vals))
            print("  %-16s 文本列：%d 个非空值，%d 种不同取值" % (c, len(vals), uniq))
    if "--sum" in argv:
        k = argv.index("--sum")
        if k + 1 < len(argv):
            col = argv[k + 1]
            nums = []
            for r in rows:
                try:
                    nums.append(float(r[col]))
                except (ValueError, KeyError, TypeError):
                    pass
            if nums:
                print("\n列「%s」：合计 %.2f，均值 %.2f，最大 %.2f，最小 %.2f"
                      % (col, sum(nums), sum(nums) / len(nums), max(nums), min(nums)))
            else:
                print("\n列「%s」没有可统计的数值。" % col)
    return 0


if __name__ == "__main__":
    sys.exit(main())
