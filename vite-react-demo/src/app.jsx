import { useState } from 'react';

function App() {
  // 计数器
  const [count, setCount] = useState(0);

  // 待办列表
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;
    setTodos((prev) => [
      ...prev,
      { id: Date.now(), text: text, done: false },
    ]);
    setInput('');
  };

  const removeTodo = (id) => {
    setTodos((prev) => prev.filter((t) => t.id !== id));
  };

  const toggleTodo = (id) => {
    setTodos((prev) =>
      prev.map((t) => (t.id === id ? { ...t, done: !t.done } : t))
    );
  };

  const remaining = todos.filter((t) => !t.done).length;

  return (
    <div className="page">
      <h1>Vite + React Demo</h1>

      {/* 计数器 */}
      <section className="card">
        <h2>计数器</h2>
        <div className="counter-value">{count}</div>
        <div className="counter-actions">
          <button onClick={() => setCount((c) => c + 1)}>+1</button>
          <button onClick={() => setCount((c) => c - 1)}>-1</button>
          <button onClick={() => setCount(0)}>重置</button>
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
