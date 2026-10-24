# -*- coding: utf-8 -*-
"""
build.py - 把 v86.wasm / BIOS / xterm.js / libv86.js 内联到 HTML
生成 b-local.html，双击可用。
"""

import base64
import os
import sys

# ---------- 配置 ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE_DIR, "b-local-template.html")
OUTPUT = os.path.join(BASE_DIR, "b-local.html")

WASM = os.path.join(BASE_DIR, "v86.wasm")
SEABIOS = os.path.join(BASE_DIR, "bios", "seabios.bin")
VGABIOS = os.path.join(BASE_DIR, "bios", "vgabios.bin")
LIBV86 = os.path.join(BASE_DIR, "libv86.js")

XTERM_JS = os.path.join(BASE_DIR, "xterm", "xterm.min.js")
XTERM_CSS = os.path.join(BASE_DIR, "xterm", "xterm.min.css")
XTERM_FIT_JS = os.path.join(BASE_DIR, "xterm", "xterm-addon-fit.min.js")


def read_b64(path):
    if not os.path.isfile(path):
        print(f"[×] 找不到：{path}")
        sys.exit(1)
    with open(path, "rb") as f:
        data = f.read()
    print(f"[+] {os.path.basename(path):35s} {len(data):>10,} 字节")
    return base64.b64encode(data).decode("ascii")


def read_text(path):
    if not os.path.isfile(path):
        print(f"[×] 找不到：{path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"[+] {os.path.basename(path):35s} {len(content):>10,} 字符")
    return content


def main():
    print("=== build.py: 生成 b-local.html ===\n")

    # 1. 读所有外部资源
    wasm_b64 = read_b64(WASM)
    seabios_b64 = read_b64(SEABIOS)
    vgabios_b64 = read_b64(VGABIOS)
    print()
    libv86_js = read_text(LIBV86)
    xterm_js = read_text(XTERM_JS)
    xterm_css = read_text(XTERM_CSS)
    xterm_fit_js = read_text(XTERM_FIT_JS)
    template = read_text(TEMPLATE)

    print("\n[·] 替换占位符...")

    # 2. 替换占位符
    html = template
    html = html.replace("___WASM_BASE64___", wasm_b64)
    html = html.replace("___SEABIOS_BASE64___", seabios_b64)
    html = html.replace("___VGABIOS_BASE64___", vgabios_b64)
    html = html.replace("___LIBV86_INLINE___", libv86_js)
    html = html.replace("___XTERM_JS___", xterm_js)
    html = html.replace("___XTERM_CSS___", xterm_css)
    html = html.replace("___XTERM_FIT_JS___", xterm_fit_js)

    # 3. 写出
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    size_mb = os.path.getsize(OUTPUT) / 1024 / 1024
    print(f"\n[√] 已生成：{OUTPUT}")
    print(f"    大小：{size_mb:.2f} MB")
    print()
    print("现在双击 b-local.html，把 alpine.iso 拖进去即可。")


if __name__ == "__main__":
    main()