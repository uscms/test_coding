# 我不想撞墙（Vite + React）

一个用 Vite + React 写的经典贪吃蛇小游戏（本名叫「我不想撞墙」），纯前端、无后端、无第三方游戏库。

## 功能

- 方向键 / WASD 控制蛇移动，空格暂停/继续，回车开始
- 吃到红色食物加分、蛇身变长；撞墙或撞到自己则游戏结束
- 记录本局得分与历史最高分，每局结束自动存入得分记录（localStorage 持久化，可清空）
- 24×24 棋盘，帧间隔 110ms，难度适中

## 技术栈

- React 18（函数组件 + Hooks）
- Vite 5（dev server 与 build）
- 原生 CSS 网格渲染棋盘

## 文件结构

```
snake-game/
├── index.html          # 入口 HTML
├── package.json        # 依赖与脚本
├── vite.config.js      # Vite 配置（含 React 插件）
└── src/
    ├── main.jsx        # React 挂载入口
    ├── App.jsx         # 游戏主体（逻辑 + 渲染）
    └── index.css       # 全局样式
```

## 运行

```bash
cd snake-game
npm install     # 安装依赖（约几分钟）
npm run dev     # 启动开发服务器，终端会打印本地地址（通常 http://localhost:5173）
```

浏览器打开终端打印的地址即可玩。

## 构建

```bash
npm run build   # 产物输出到 dist/
npm run preview # 本地预览构建产物
```

## 玩法说明

| 按键 | 作用 |
|---|---|
| ↑ ↓ ← → 或 W S A D | 控制方向（不能 180° 掉头） |
| 空格 / 回车 | 开始 / 暂停 / 继续 |
| 点击按钮 | 同空格/回车，也可「再来一局」 |

## 注意

- 运行与验收请自行执行：`npm install` 和 `npm run dev`。
- 依赖与缓存只装在本目录（node_modules/），不会污染沙箱外环境。
