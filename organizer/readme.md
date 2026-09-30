# File Organizer

命令行文件整理工具：把指定目录下的文件按扩展名自动归类到子目录。

## 分类规则

| 子目录 | 包含的扩展名 |
|--------|-------------|
| `Images/` | .jpg .jpeg .png .gif .bmp .tiff .tif .svg .webp .ico .heic .heif |
| `Docs/` | .txt .pdf .doc .docx .xls .xlsx .ppt .pptx .csv .md .odt .ods .odp .rtf .tex .html .htm |
| `Videos/` | .mp4 .avi .mkv .mov .wmv .flv .webm .m4v .mpg .mpeg .3gp |
| `Music/` | .mp3 .wav .flac .aac .ogg .wma .mid .m4a .opus .aiff |
| `Others/` | 其余所有扩展名（或无扩展名） |

## 依赖

仅 Python 3 标准库，无需安装任何第三方包。

## 使用方法

```bash
# 进入项目目录
cd organizer/

# 1. 先预览（dry-run，默认行为）—— 只打印计划，不移动任何文件
python3 file_organizer.py /path/to/your/files

# 也可以用显式 --dry-run（效果相同）
python3 file_organizer.py /path/to/your/files --dry-run

# 2. 确认输出无误后，真正执行移动
python3 file_organizer.py /path/to/your/files --apply
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `directory` | （必填）要整理的目标目录路径 |
| `--dry-run` | 只打印将要做的操作，不实际移动文件（不写 `--apply` 时默认就是此行为） |
| `--apply` | 真正执行文件移动 |

> `--dry-run` 和 `--apply` 互斥，不能同时使用。

## 同名文件处理

若目标子目录中已存在同名文件，工具会自动在文件名后追加序号：

```
photo.jpg      → Images/photo.jpg
photo.jpg      → Images/photo_1.jpg   (第二个)
photo.jpg      → Images/photo_2.jpg   (第三个)
```

绝不会覆盖已有文件。

## 其他说明

- 只整理目标目录**第一层**的文件，不递归子目录。
- 跳过隐藏文件（以 `.` 开头的文件）。
- 工具自身（`file_organizer.py`）不会被移动。
- 若目标目录下无需整理的文件，会提示"没有需要整理的文件"。
