import { useCallback, useEffect, useRef, useState } from 'react';

const COLS = 24;          // 列数
const ROWS = 24;         // 行数
const CELL = 20;         // 每格像素
const TICK_MS = 110;     // 游戏帧间隔（毫秒）

const DIR = {
  up: { x: 0, y: -1 },
  down: { x: 0, y: 1 },
  left: { x: -1, y: 0 },
  right: { x: 1, y: 0 },
};

// 取反方向，用于禁止 180° 掉头
const OPPOSITE = { up: 'down', down: 'up', left: 'right', right: 'left' };

function randFood(occupied) {
  // 从所有未被蛇身占据的格子里随机取一个作为食物
  const free = [];
  for (let x = 0; x < COLS; x++) {
    for (let y = 0; y < ROWS; y++) {
      if (!occupied.some((s) => s.x === x && s.y === y)) free.push({ x, y });
    }
  }
  if (free.length === 0) return null; // 蛇占满棋盘，理论上游戏已赢
  return free[Math.floor(Math.random() * free.length)];
}

function initialSnake() {
  const mid = Math.floor(COLS / 2);
  return [
    { x: mid, y: mid },
    { x: mid - 1, y: mid },
    { x: mid - 2, y: mid },
  ];
}

export default function App() {
  const [snake, setSnake] = useState(initialSnake);
  const [food, setFood] = useState(() => randFood(initialSnake()));
  const [score, setScore] = useState(0);
  const [best, setBest] = useState(0);
  const [status, setStatus] = useState('ready'); // ready | playing | paused | over | win
  const [grid, setGrid] = useState({ cols: COLS, rows: ROWS });

  // 用 ref 保存最新值，供定时器 / 键盘回调读取，避免闭包陷阱
  const snakeRef = useRef(snake);
  const foodRef = useRef(food);
  const dirRef = useRef('right');          // 当前真实方向
  const pendingDirRef = useRef('right');   // 本次按键期望转向（一帧最多转一次）
  const statusRef = useRef(status);

  snakeRef.current = snake;
  foodRef.current = food;
  statusRef.current = status;

  const startGame = useCallback(() => {
    const s = initialSnake();
    dirRef.current = 'right';
    pendingDirRef.current = 'right';
    setSnake(s);
    setFood(randFood(s));
    setScore(0);
    setStatus('playing');
  }, []);

  // 键盘控制
  useEffect(() => {
    const onKey = (e) => {
      const k = e.key;
      let d = null;
      if (k === 'ArrowUp' || k === 'w' || k === 'W') d = 'up';
      else if (k === 'ArrowDown' || k === 's' || k === 'S') d = 'down';
      else if (k === 'ArrowLeft' || k === 'a' || k === 'A') d = 'left';
      else if (k === 'ArrowRight' || k === 'd' || k === 'D') d = 'right';
      else if (k === ' ' || k === 'Enter') {
        e.preventDefault();
        // 空格/回车：ready 或 over/win 时开始（或重新开始），playing 时暂停
        if (statusRef.current === 'playing') setStatus('paused');
        else startGame();
        return;
      }

      if (d) {
        e.preventDefault();
        if (statusRef.current === 'ready') startGame();
        // 只能相对当前真实方向转向，且不能掉头
        if (d !== OPPOSITE[dirRef.current]) pendingDirRef.current = d;
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [startGame]);

  // 游戏主循环
  useEffect(() => {
    if (status !== 'playing') return;
    const timer = setInterval(() => {
      // 应用本帧转向
      dirRef.current = pendingDirRef.current;
      const dir = DIR[dirRef.current];

      const s = snakeRef.current;
      const head = s[0];
      const nx = head.x + dir.x;
      const ny = head.y + dir.y;

      // 撞墙
      if (nx < 0 || ny < 0 || nx >= COLS || ny >= ROWS) {
        setStatus('over');
        return;
      }
      // 撞自己（即将进入的尾格若会被移走则不算，简化处理：整条都算障碍）
      const body = s;
      if (body.some((p, i) => i < body.length - 1 && p.x === nx && p.y === ny)) {
        setStatus('over');
        return;
      }

      const ate = foodRef.current && nx === foodRef.current.x && ny === foodRef.current.y;
      const newSnake = [ { x: nx, y: ny }, ...s ];
      if (ate) {
        setScore((sc) => {
          const ns = sc + 1;
          setBest((b) => Math.max(b, ns));
          return ns;
        });
        setFood(randFood(newSnake)); // 蛇不变长，食物更新
      } else {
        newSnake.pop(); // 没吃到，移动
        setSnake(newSnake);
      }
    }, TICK_MS);
    return () => clearInterval(timer);
  }, [status]);

  // 渲染用的棋盘坐标映射
  const cells = [];
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      cells.push({ x, y });
    }
  }
  const snakeSet = new Set(snake.map((p) => `${p.x},${p.y}`));
  const headKey = `${snake[0].x},${snake[0].y}`;

  return (
    <div className="wrap">
      <h1>贪吃蛇</h1>
      <div className="hud">
        <div>得分 <b>{score}</b></div>
        <div>最高 <b>{best}</b></div>
      </div>

      <div
        className="board"
        style={{
          gridTemplateColumns: `repeat(${COLS}, ${CELL}px)`,
          gridTemplateRows: `repeat(${ROWS}, ${CELL}px)`,
        }}
      >
        {cells.map((c) => {
          const key = `${c.x},${c.y}`;
          let cls = 'cell';
          if (snakeSet.has(key)) {
            cls = key === headKey ? 'cell head' : 'cell body';
          }
          if (food && c.x === food.x && c.y === food.y) cls = 'cell food';
          return <div key={key} className={cls} />;
        })}

        {status !== 'playing' && (
          <div className="overlay">
            <div className="overlay-text">
              {status === 'over' && <>撞墙啦，得分 {score}</>}
              {status === 'paused' && <>已暂停</>}
              {status === 'ready' && <>按 空格 / 方向键 开始</>}
            </div>
            <button className="btn" onClick={startGame}>
              {status === 'over' ? '再来一局' : status === 'paused' ? '继续' : '开始游戏'}
            </button>
            {status === 'paused' && (
              <button className="btn ghost" onClick={() => setStatus('playing')}>
                恢复
              </button>
            )}
          </div>
        )}
      </div>

      <div className="tips">
        <span>↑↓←→ / WASD 控制方向，空格暂停，回车开始</span>
      </div>
    </div>
  );
}
