#!/usr/bin/env python3
"""命令行待办清单（todo）。

单文件实现，只使用 Python 标准库。
数据保存在本脚本同目录下的 todo.json。

子命令：
    add  新增一条待办
    list 列出所有待办
    done 将指定 id 的待办标记为已完成
    rm   删除指定 id 的待办
"""

import argparse
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo.json")


def load_todos():
    """读取待办列表；文件不存在或为空时返回空列表。"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if not isinstance(data, list):
                print("错误：todo.json 格式不正确（应为列表）。", file=sys.stderr)
                sys.exit(1)
            return data
    except json.JSONDecodeError as e:
        print(f"错误：todo.json 无法解析（{e}）。", file=sys.stderr)
        sys.exit(1)


def save_todos(todos):
    """把待办列表写回 todo.json。"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)
        f.write("\n")


def next_id(todos):
    """计算下一个可用的自增 id（从 1 开始）。"""
    if not todos:
        return 1
    return max(item.get("id", 0) for item in todos) + 1


def find_todo(todos, todo_id):
    """按 id 查找待办，找不到就报错退出。"""
    for item in todos:
        if item.get("id") == todo_id:
            return item
    print(f"错误：找不到 id 为 {todo_id} 的待办。", file=sys.stderr)
    sys.exit(1)


def cmd_add(args):
    todos = load_todos()
    todo = {
        "id": next_id(todos),
        "text": args.text,
        "done": False,
    }
    todos.append(todo)
    save_todos(todos)
    print(f"已添加 [{todo['id']}] {args.text}")


def cmd_list(args):
    todos = load_todos()
    if not todos:
        print("当前没有待办。")
        return
    for item in todos:
        mark = "x" if item.get("done") else " "
        status = "已完成" if item.get("done") else "待办"
        print(f"[{mark}] [{item['id']}] {item['text']}  ({status})")


def cmd_done(args):
    todos = load_todos()
    item = find_todo(todos, args.id)
    item["done"] = True
    save_todos(todos)
    print(f"已将 [{args.id}] {item['text']} 标记为已完成。")


def cmd_rm(args):
    todos = load_todos()
    item = find_todo(todos, args.id)
    todos.remove(item)
    save_todos(todos)
    print(f"已删除 [{args.id}] {item['text']}。")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="todo.py",
        description="命令行待办清单，数据保存在同目录的 todo.json。",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="新增一条待办")
    p_add.add_argument("text", help="待办内容")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="列出所有待办")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="将指定 id 的待办标记为已完成")
    p_done.add_argument("id", type=int, help="待办 id")
    p_done.set_defaults(func=cmd_done)

    p_rm = sub.add_parser("rm", help="删除指定 id 的待办")
    p_rm.add_argument("id", type=int, help="待办 id")
    p_rm.set_defaults(func=cmd_rm)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
