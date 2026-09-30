# 命令行待办清单（todo）

单文件 Python 小工具，只用标准库，无需安装任何依赖。
数据保存在本目录下的 `todo.json`（自动创建，格式为 JSON 列表）。

## 环境要求

- Python 3.6+（建议 3.8+）

## 使用方式

```bash
python3 todo.py <子命令> [参数]
```

四个子命令说明如下：

### 1. `add` —— 新增一条待办

```bash
python3 todo.py add 买牛奶
```

- 参数：待办内容（直接跟在 `add` 后面，可以包含空格，无需引号；含特殊字符时用引号包住）。
- 自动分配自增 id（从 1 开始），并打印出新增条目的 id。

### 2. `list` —— 列出所有待办

```bash
python3 todo.py list
```

- 输出格式：`[x] 或 [ ] [id] 内容 (已完成/待办)`，`x` 表示已完成。
- 没有待办时会提示"当前没有待办。"。

### 3. `done` —— 将指定 id 的待办标记为已完成

```bash
python3 todo.py done 1
```

- 参数：待办的数字 id。
- 完成后再次 `list` 即可看到状态变化。

### 4. `rm` —— 删除指定 id 的待办

```bash
python3 todo.py rm 1
```

- 参数：待办的数字 id。
- 删除后该条目从 `todo.json` 中移除（id 不会回收复用，新条目继续用更大的 id）。

## 完整示例

```bash
python3 todo.py add 写周报
python3 todo.py add 买菜
python3 todo.py list
# [ ] [1] 写周报  (待办)
# [ ] [2] 买菜  (待办)

python3 todo.py done 1
python3 todo.py list
# [x] [1] 写周报  (已完成)
# [ ] [2] 买菜  (待办)

python3 todo.py rm 2
python3 todo.py list
# [x] [1] 写周报  (已完成)
```

## 数据文件

`todo.json` 与脚本放在同一目录，结构示例：

```json
[
  {"id": 1, "text": "写周报", "done": true},
  {"id": 2, "text": "买菜", "done": false}
]
```

不需要时可以安全删除该文件，下次运行会自动重建。
