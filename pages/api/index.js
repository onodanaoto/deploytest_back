import { useState } from 'react';

export default function Home() {
  const [date, setDate] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/api/ask-date', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ date }),
    });
    const data = await res.json();
    setResponse(data);
  };

  return (
    <div>
      <h1>今日は何の日？</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
        <button type="submit">送信</button>
      </form>
      {response && (
        <div>
          <h2>結果</h2>
          <p>{response.text}</p>
          {response.image && <img src={response.image} alt="関連画像" />}
        </div>
      )}
    </div>
  );
}
