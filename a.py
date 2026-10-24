# -*- coding: utf-8 -*-
"""
fix_v86.py
把 b.html 里所有 V86Starter 替换成 V86，以适配新版 v86 引擎。
用法：把这个文件和 b.html 放同一目录，然后双击运行（或 python fix_v86.py）。
"""

import os
import sys

# ---------- 配置 ----------
TARGET_FILE = "b.html"          # 要修改的文件
OLD = "V86Starter"              # 旧 API 名
NEW = "V86"                     # 新 API 名
BACKUP = True                   # 是否备份原文件为 b.html.bak


def main():
    # 脚本所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, TARGET_FILE)

    if not os.path.isfile(file_path):
        print(f"[×] 找不到文件：{file_path}")
        print("    请把 fix_v86.py 和 b.html 放在同一个目录下再运行。")
        sys.exit(1)

    # 用 UTF-8 读取（b.html 保存时如果是 UTF-8，中文不会乱码）
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        print("[×] 文件不是 UTF-8 编码，尝试用 GBK 读取…")
        try:
            with open(file_path, "r", encoding="gbk") as f:
                content = f.read()
        except Exception as e:
            print(f"[×] 读取失败：{e}")
            sys.exit(1)

    # 统计替换次数
    count = content.count(OLD)
    if count == 0:
        print(f"[i] 文件中没有找到 '{OLD}'，可能已经改过了。")
        sys.exit(0)

    # 备份
    if BACKUP:
        backup_path = file_path + ".bak"
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] 原文件已备份为：{os.path.basename(backup_path)}")

    # 替换
    new_content = content.replace(OLD, NEW)

    # 写回
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[√] 替换完成：'{OLD}' → '{NEW}'，共替换 {count} 处。")
    print(f"    文件已更新：{file_path}")
    print("    现在回到浏览器按 Ctrl + Shift + R 硬刷新即可。")


if __name__ == "__main__":
    main()
