"""md2html —— Markdown 转 HTML（只用标准库，不依赖任何第三方库）

用法：
    python md2html.py <file.md>            生成同名 .html
    python md2html.py <file.md> -o out.html
"""
import html
import os
import sys


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    out, i, buf = [], 0, ""
    while i < len(s):
        if s[i] == "`":
            j = s.find("`", i + 1)
            if j > 0:
                if buf:
                    out.append(buf)
                    buf = ""
                out.append("<code>%s</code>" % s[i + 1:j])
                i = j + 1
                continue
        if s.startswith("**", i):
            j = s.find("**", i + 2)
            if j > 0:
                if buf:
                    out.append(buf)
                    buf = ""
                out.append("<strong>%s</strong>" % s[i + 2:j])
                i = j + 2
                continue
        if s[i] == "[":
            j = s.find("](", i)
            if j > 0:
                k = s.find(")", j)
                if k > 0:
                    if buf:
                        out.append(buf)
                        buf = ""
                    out.append('<a href="%s">%s</a>' % (s[j + 2:k], s[i + 1:j]))
                    i = k + 1
                    continue
        buf += s[i]
        i += 1
    if buf:
        out.append(buf)
    return "".join(out)


def convert(md: str) -> str:
    body, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith("```"):
            code, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(html.escape(lines[i]))
                i += 1
            body.append("<pre><code>%s</code></pre>" % "\n".join(code))
            i += 1
            continue
        if ln.startswith("### "):
            body.append("<h3>%s</h3>" % inline(ln[4:]))
        elif ln.startswith("## "):
            body.append("<h2>%s</h2>" % inline(ln[3:]))
        elif ln.startswith("# "):
            body.append("<h1>%s</h1>" % inline(ln[2:]))
        elif ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append("<li>%s</li>" % inline(lines[i][2:]))
                i += 1
            body.append("<ul>%s</ul>" % "".join(items))
            continue
        elif ln.strip() and ln[0].isdigit() and ln[1:3] in (". ", ") "):
            items = []
            while i < len(lines) and lines[i][:1].isdigit() and lines[i][1:3] in (". ", ") "):
                items.append("<li>%s</li>" % inline(lines[i][3:]))
                i += 1
            body.append("<ol>%s</ol>" % "".join(items))
            continue
        elif ln.strip():
            body.append("<p>%s</p>" % inline(ln))
        i += 1
    return ("<!DOCTYPE html>\n<html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
            "<title>Markdown 转换结果</title><style>"
            "body{max-width:760px;margin:40px auto;padding:0 20px;font-family:"
            "-apple-system,'Microsoft YaHei',sans-serif;line-height:1.7;color:#222}"
            "h1,h2,h3{border-bottom:1px solid #eee;padding-bottom:6px}"
            "code{background:#f5f5f5;padding:2px 6px;border-radius:4px}"
            "pre{background:#f5f5f5;padding:14px;border-radius:6px;overflow:auto}"
            "a{color:#d5347a}</style></head><body>\n%s\n</body></html>" % "\n".join(body))


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    src = argv[0]
    dst = os.path.splitext(src)[0] + ".html"
    if "-o" in argv:
        k = argv.index("-o")
        if k + 1 < len(argv):
            dst = argv[k + 1]
    try:
        with open(src, "r", encoding="utf-8") as f:
            md = f.read()
    except OSError as e:
        print("读取失败：%s" % e)
        return 1
    with open(dst, "w", encoding="utf-8") as f:
        f.write(convert(md))
    print("已生成：%s" % dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
