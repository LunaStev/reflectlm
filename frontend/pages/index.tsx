import { useState } from "react"

export default function Home() {
  const [input, setInput] = useState("")
  const [log, setLog] = useState<{ user: string; ai: string; confidence: number; reason: string }[]>([])

  const sendMessage = async () => {
    if (!input.trim()) return

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    })

    const data = await res.json()
    setLog(prev => [...prev, {
      user: input,
      ai: data.response,
      confidence: data.confidence,
      reason: data.reason
    }])
    setInput("")
  }

  return (
    <div style={{ padding: 40, fontFamily: "sans-serif" }}>
      <h1>ReflectLM Chat</h1>
      <div style={{ marginBottom: 20 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="메시지를 입력하세요"
          style={{ width: "80%", padding: 10 }}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage} style={{ padding: "10px 20px", marginLeft: 10 }}>보내기</button>
      </div>
      <div>
        {log.map((msg, i) => (
          <div key={i} style={{ marginBottom: 20 }}>
            <p><strong>🙋‍♀️ 당신:</strong> {msg.user}</p>
            <p><strong>🤖 AI:</strong> {msg.ai}</p>
            <p><em>신뢰도: {msg.confidence}% – {msg.reason}</em></p>
            <hr />
          </div>
        ))}
      </div>
    </div>
  )
}
