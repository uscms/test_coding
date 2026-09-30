import { useEffect, useRef, useState } from 'react';

// 极简音效引擎：基于 Web Audio，无第三方库、无音频文件
function createSoundEngine() {
  let ctx = null;

  function getCtx() {
    if (!ctx) {
      const AC =
        window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      ctx = new AC();
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function beep(freq, duration, type, volume) {
    const c = getCtx();
    if (!c) return;
    const osc = c.createOscillator();
    const gain = c.createGain();
    osc.type = type || 'sine';
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(volume, c.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + duration);
    osc.connect(gain);
    gain.connect(c.destination);
    osc.start();
    osc.stop(c.currentTime + duration);
  }

  return {
    tick() {
      beep(600, 0.08, 'square', 0.06); // 计数器点击
    },
    add() {
      beep(880, 0.12, 'sine', 0.12); // 添加待办
    },
    check() {
      beep(520, 0.09, 'triangle', 0.1); // 勾选
    },
    remove() {
      beep(220, 0.15, 'sawtooth', 0.08); // 删除
    },
    unlock() {
      beep(440, 0.05, 'sine', 0.05);
    },
  };
}

function App() {
  // 计数器
  const [count, setCount] = useState(0);

  // 待办列表
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  // 主题（默认深色）
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('vite-demo-theme');
    return saved || 'dark';
  });

  // 音效开关（默认开）
  const [soundOn, setSoundOn] = useState(() =>
    localStorage.getItem('vite-demo-sound') !== 'off'
  );
  const soundOnRef = useRef(soundOn);
  const soundRef = useRef(createSoundEngine());

  useEffect(() => {
    document.body.classList.toggle('theme-dark', theme === 'dark');
    document.body.classList.toggle('theme-light', theme === 'light');
    localStorage.setItem('vite-demo-theme', theme);
  }, [theme]);

  useEffect(() => {
    soundOnRef.current = soundOn;
    localStorage.setItem('vite-demo-sound', soundOn ? 'on' : 'off');
  }, [soundOn]);

  // 浏览器要求首次音效必须由用户交互触发，这里在第一次点击时解锁 AudioContext
  const unlockOnce = useRef(false);
  function unlockAudio() {
    if (!unlockOnce.current) {
      soundRef.current.unlock();
      unlockOnce.current = true;
    }
  }
  const play = (fn) => {
    if (soundOnRef.current) fn(soundRef.current);
  };

  const bump = (delta) => {
    unlockAudio();
    setCount((c) => c + delta);
    play((s) => s.tick());
  };

  const addTodo = (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;
    unlockAudio();
    setTodos((prev) => [
      ...prev,
      { id: Date.now(), text: text, done: false },
    ]);
    setInput('');
    play((s) => s.add());
  };

  const removeTodo = (id) => {
    setTodos((prev) => prev.filter((t) => t.id !== id));
    play((s) => s.remove());
  };

  const toggleTodo = (id) => {
    setTodos((prev) =>
      prev.map((t) => (t.id === id ? { ...t, done: !t.done } : t))
    );
    play((s) => s.check());
  };

  const remaining = todos.filter((t) => !t.done).length;

  return (
    <div className="page">
      <h1>Vite + React Demo</h1>

      <div className="top-controls">
        <button
          className="ctrl-btn"
          onClick={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}
        >
          {theme === 'dark' ? '☀️ 浅色模式' : '🌙 深色模式'}
        </button>
        <button
          className="ctrl-btn"
          onClick={() => setSoundOn((s) => !s)}
          aria-pressed={soundOn}
        >
          {soundOn ? '🔊 音效开' : '🔇 音效关'}
        </button>
      </div>

      {/* 计数器 */}
      <section className="card">
        <h2>计数器</h2>
        <div className="counter-value">{count}</div>
        <div className="counter-actions">
          <button onClick={() => bump(1)}>+1</button>
          <button onClick={() => bump(-1)}>-1</button>
          <button onClick={() => { unlockAudio(); setCount(0); play((s) => s.tick()); }}>
            重置
          </button>
        </div>
      </section>

      {/* 待办列表 */}
      <section className="card">
        <h2>待办列表</h2>
        <form className="todo-form" onSubmit={addTodo}>
          <input
            type="text"
            placeholder="输入待办事项，回车添加"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            aria-label="待办事项"
          />
          <button type="submit">添加</button>
        </form>

        {todos.length === 0 ? (
          <p className="empty">还没有待办事项，先添加一条吧</p>
        ) : (
          <ul className="todo-list">
            {todos.map((t) => (
              <li key={t.id} className={t.done ? 'todo-item done' : 'todo-item'}>
                <label className="todo-label">
                  <input
                    type="checkbox"
                    checked={t.done}
                    onChange={() => toggleTodo(t.id)}
                  />
                  <span className={t.done ? 'todo-text done' : 'todo-text'}>
                    {t.text}
                  </span>
                </label>
                <button
                  className="btn-remove"
                  onClick={() => removeTodo(t.id)}
                  aria-label={'删除「' + t.text + '」'}
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        )}

        {todos.length > 0 && (
          <p className="todo-summary">
            共 {todos.length} 项，还剩 {remaining} 项未完成
          </p>
        )}
      </section>
    </div>
  );
}

export default App;
