# Alpine Linux in Browser · 浏览器里的真 Linux

> 在浏览器里跑一个**真正的 Alpine Linux**，不依赖任何插件、不联网、纯 WebAssembly。
> 基于 [v86](https://github.com/copy/v86) x86 模拟器 + Alpine 3.24.2 i686。

![License](https://img.shields.io/badge/license-MIT-blue)
![Alpine](https://img.shields.io/badge/Alpine-3.24.2-0d597f)
![v86](https://img.shields.io/badge/v86-WASM-orange)

---

## 这是什么

打开一个网页，等几秒，你就有了一台**跑在浏览器里的 x86 虚拟机**，里面是真实的
Alpine Linux 3.24.2（32 位 i686 内核），可以直接：

- `uname -a` 看到真实内核版本
- `ps` 看到 OpenRC 调度的真实进程
- `cat /proc/cpuinfo` 看到 v86 模拟出的 CPU
- 登录 `root`（无密码），敲任何 busybox / ash 支持的命令

这不是容器、不是模拟 shell、不是假的输出——**每一条 x86 指令都真的在虚拟 CPU 上执行**。

---

## 在线体验
[click
](index.html)

打开后：

1. 等待 5~15 秒（首次加载 ISO 约 49 MB，之后走浏览器缓存）
2. 出现 **SeaBIOS** → **ISOLINUX 蓝色菜单**
3. 直接按**回车**
4. 停在 `localhost login:` 时，输入 `root`，密码**直接回车**
5. 进入 `localhost:~#`，开始玩

---

## 特性

| 特性 | 说明 |
|---|---|
| 真实 x86 内核 | Alpine Linux 3.24.2，kernel 6.12 `i686` |
| 完全离线 | 不需要网络，所有文件本地加载 |
| 零依赖 | 一个 `b.html` + v86 引擎 + BIOS + ISO |
| 可保存状态 | 点"💾 保存"可 dump 整个 VM 快照 |
| 可选联网 | 通过 WISP 中继，能 `apk add` 装包 |
| 支持全屏 | 点"⛶ 全屏"进沉浸式终端 |

---

## 本地运行

### 目录结构

```
v86/
├── b.html
├── libv86.js
├── v86.wasm
├── bios/
│   ├── seabios.bin
│   └── vgabios.bin
└── images/
    └── alpine.iso        ← Alpine 3.24.2 virt x86，约 49 MB
```

### 启动本地 HTTP 服务器

**不要双击 `b.html`**，`file://` 协议下浏览器会拒绝加载 `.wasm` 和 `.iso`。
必须起本地 HTTP 服务：

```bash
# Python 3
python -m http.server 8080

# 或者 Node.js
npx http-server -p 8080
```

然后浏览器访问：

```
http://localhost:8080/b.html
```

### 获取 Alpine ISO

从 Alpine 官方下载 **32 位 virt 版**（v86 只能跑 i686，不能跑 x86_64）：

```
https://dl-cdn.alpinelinux.org/alpine/v3.24/releases/x86/alpine-virt-3.24.2-x86.iso
```

国内镜像（更快）：

```
https://mirrors.aliyun.com/alpine/v3.24/releases/x86/alpine-virt-3.24.2-x86.iso
https://mirrors.tuna.tsinghua.edu.cn/alpine/v3.24/releases/x86/alpine-virt-3.24.2-x86.iso
```

下载后重命名为 `alpine.iso`，放进 `images/` 目录。

### 获取 v86 引擎

从 v86 官方仓库或 Release 下载 `libv86.js` 和 `v86.wasm`：

```
https://github.com/copy/v86/releases
```

把 `libv86.js` 放在根目录，`v86.wasm` 也放根目录。

### 获取 BIOS

```
https://github.com/copy/v86/tree/master/bios
```

下载 `seabios.bin` 和 `vgabios.bin`，放进 `bios/` 目录。

---

## 联网（可选）

默认情况下虚拟机**没有网络**。如果要开启联网：

在 `b.html` 里，`new V86({...})` 中加上：

```javascript
net_device: { type: "virtio" },
network_relay_url: "wss://relay.rybakit.ru/",
```

启动 Alpine 后，在 shell 里执行：

```sh
ip link set eth0 up
udhcpc -i eth0
ip addr show eth0
ping -c 3 8.8.8.8
apk update
apk add nano
```

> ⚠️ `relay.rybakit.ru` 是第三方公共中继，流量经过它。
> **不要在虚拟机里输入任何密码、账号或敏感信息。**
> 仅供测试学习使用。

---

## 常见问题

**Q: 为什么不能用 64 位（x86_64）的 Alpine？**

v86 模拟的 CPU 是 i686（32 位），无法执行 64 位指令，必须用 x86 版内核。

**Q: 为什么必须用 HTTP 服务器，不能直接双击？**

`file://` 协议下浏览器有跨域安全策略，会拒绝加载本地的 `.wasm`、`.bin`、`.iso` 文件。

**Q: 卡在 "This kernel requires an x86-64 CPU" 怎么办？**

你下载的是 64 位 ISO。换成 `alpine-virt-x.x.x-x86.iso`。

**Q: 重启后我装的东西都没了？**

默认从光盘启动，根文件系统在内存里。要持久化需要在 `V86({...})` 里挂一块虚拟硬盘并运行 `setup-alpine` 安装到硬盘。

**Q: 报错 `V86Starter is not defined`？**

新版 v86 使用 `V86` 类而不是旧的 `V86Starter`。把 `b.html` 里所有 `V86Starter` 改成 `V86`。

---

## 第三方许可证

This project bundles or depends on the following third-party components.
Each component remains under its own license; the original license texts
are preserved in their respective directories.

本项目打包或依赖以下第三方组件。每个组件遵循其原始许可证，
相关许可证原文均保留在对应目录中。

---

### 1. v86

- **License:** Apache License 2.0
- **Source:** https://github.com/copy/v86
- **Files:** `libv86.js`, `v86.wasm`
- **Copyright:** Copyright (c) 2013-2026 Fabian Hemmer and contributors

Apache-2.0 允许商用、修改、再分发与闭源集成，需保留许可证与 NOTICE 文件。

---

### 2. Alpine Linux 3.24.2 (x86)

- **License:** Multiple (per-package, follows upstream)
- **Source:** https://alpinelinux.org/
- **ISO:** `images/alpine.iso`
- **License archive inside ISO:** `/usr/share/licenses/`
- **Alpine project's own code:** Mostly MIT
- **Full license list:** https://gitlab.alpinelinux.org/alpine/aports

Alpine Linux 是一个自由、开源的操作系统发行版，其 ISO 镜像可以自由
再分发。系统内每个软件包（Linux kernel, BusyBox, musl, OpenRC,
apk-tools 等）分别遵循各自的上游许可证，详情请参阅 ISO 内的
`/usr/share/licenses/` 目录以及每个软件包的 `APKBUILD` 文件。

---

### 3. SeaBIOS

- **License:** GNU Lesser General Public License v3.0 (LGPL-3.0)
- **Source:** https://www.seabios.org/
- **Files:** `bios/seabios.bin`
- **Copyright:** Copyright (C) 2008-2026 Kevin O'Connor and contributors
- **License text:** see `bios/COPYING.LESSER`

---

### 4. VGA BIOS (vgabios)

- **License:** GNU Lesser General Public License v3.0 (LGPL-3.0)
- **Source:** https://github.com/copy/v86/tree/master/bios
- **Files:** `bios/vgabios.bin`
- **License text:** see `bios/COPYING.LESSER`

---

### 5. This project's own code / 本项目自有代码

- **License:** MIT
- **Files:** `b.html`, `README.md`, `fix_v86.py` and other custom scripts
- **Copyright:** Copyright (c) 2026 James2026

MIT 许可证全文见仓库根目录的 [`LICENSE`](./LICENSE) 文件。

---

### 6. Optional: WISP network relay / 可选的网络中继

If you enable networking (`network_relay_url`), the emulated machine's TCP
traffic is forwarded through a third-party WISP relay. This relay is **not**
part of this project and has its own terms of service.

如果启用了网络功能（`network_relay_url`），虚拟机内的 TCP 流量会经过
第三方 WISP 中继服务器。该中继**不属于本项目**，其使用条款由中继提供方
决定。请勿在虚拟机中输入敏感信息（密码、账号等）。

Default relay used: `wss://relay.rybakit.ru/`

---

### Summary table / 汇总表

| Component | License | Files |
|---|---|---|
| v86 | Apache-2.0 | `libv86.js`, `v86.wasm` |
| Alpine Linux 3.24.2 | Multiple (per-package) | `images/alpine.iso` |
| SeaBIOS | LGPL-3.0 | `bios/seabios.bin` |
| VGA BIOS | LGPL-3.0 | `bios/vgabios.bin` |
| This project | MIT | `b.html`, etc. |

---

All third-party components are free / open-source software and can be
redistributed. If you believe any attribution is missing or incorrect,
please open an issue.

所有第三方组件均为自由 / 开源软件，可自由再分发。
如发现遗漏或错误，请提交 issue。

---

## Credits

- [v86](https://github.com/copy/v86) — x86 virtualization in JavaScript / WebAssembly
- [Alpine Linux](https://alpinelinux.org/) — a security-oriented, lightweight Linux distribution
- [SeaBIOS](https://www.seabios.org/) — open-source x86 BIOS implementation

---

## License

MIT © 2026 [James2026](https://gitee.com/james2026)
```
MIT License

Copyright (c) 2026 James2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```