import { useState, useEffect } from "react"

export default function Home() {
  const [input, setInput] = useState("")
  const [log, setLog] = useState<{ user: string; ai: string; confidence: number; reason: string }[]>([])

  const sendMessage = async () => {
    if (!input.trim()) return

    const res = await fetch("http://localhost:8000/chat", {
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

  useEffect(() => {
    const chatbox = document.getElementById("chat-log")
    if (chatbox) chatbox.scrollTop = chatbox.scrollHeight
  }, [log])

  return (
    <div className="chat-container">
      <h1 className="chat-title">ReflectLM</h1>
      <div id="chat-log" className="chat-log">
        {log.map((msg, i) => (
          <div key={i} className="chat-bubble user">
            <p><strong>🙋‍♀️ You:</strong> {msg.user}</p>
            <div className="chat-bubble ai">
              <p><strong>🤖 AI:</strong> {msg.ai}</p>
              <p className="meta">Confidence: {msg.confidence}% – {msg.reason}</p>
            </div>
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  )
}
