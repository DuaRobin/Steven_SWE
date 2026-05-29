import React, { useState, useRef, useEffect } from 'react';
import type { ChatMessage } from './types/interfaces';
import './ChatApp.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const service_endpoint = "http://localhost:8080/chat";
const ChatApp: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const [controller, setController] = useState<AbortController | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    const abortController = new AbortController();
    setController(abortController);
    const userMsg: ChatMessage = { role: 'user', text: inputValue };
    const assistantMsg: ChatMessage = { 
        role: 'assistant', 
        text: '', 
        streaming: true, 
        citations: [],
        confidence: 0.0,
        is_grounded: false,
        user_aborted: false
    };

    setMessages((prev) => [...prev, userMsg, assistantMsg]);
    setInputValue('');

    try {
      const response = await fetch(service_endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjA2YzdjNDc2NzliODA4ZmNlZGY3MzkxZDdiMWUzNjU3YmNhMzBkYmIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEwNzM5MzcxMzY1MzE5OTA4OTExIiwiZW1haWwiOiJyb2Jpbi5kdWFAaG90bWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IjBXd3dGSHF5aUlLdmZTN1hWYnVfenciLCJpYXQiOjE3ODAwNzkzNTAsImV4cCI6MTc4MDA4Mjk1MH0.Aj3OIfIO5bGyj4cMtzdHOySzIOvgqQOGSsvfEjIRnFGXV9oPHNC9orANjEurgBRVK8-j2QMnLE4lbiDB2j6fLZLZw1BMeKG70kc6Yr9FJokVWz1UqIIVrsK2qk-pvLcTp4VKkk2FgrG4-65nfJYTrWUrUJzXJa9Fp9fQNqjQzfhvKY8S5zXI2tujgEZiE9PWCJbUPI48ZU_YTHCn0uqbYq3mJJkEiP8TIAmR-1Le7tp5_ykwppTe2Na2Sp8BhbvI5iiyULWXdOaNw6mXXd6avt4MwivWihBbm8vm019YBzosqN9TxMOTzxVQKHqRFq1XuOPmGZKAyB7mwD_VACIBqw` },
        body: JSON.stringify({ message: inputValue }),
        signal: abortController.signal
      });

      if (!response.body) throw new Error("No response body available");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedText = '';
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const payload = line.replace('data: ', '').trim();

            if (payload === '[DONE]') {
              setMessages((prev) => {
                const newMsgs = [...prev];
                newMsgs[newMsgs.length - 1].streaming = false;
                return newMsgs;
              });
              break;
            }

            try {
              const parsed = JSON.parse(payload);
              if (parsed.delta !== undefined) {
                accumulatedText += parsed.delta;
                setMessages((prev) => {
                  const newMsgs = [...prev];
                  newMsgs[newMsgs.length - 1].text = accumulatedText;
                  return newMsgs;
                });
              }
              if (parsed.answer){
                setMessages((prev) => {
                  const newMsgs = [...prev];
                  const lastMsg = newMsgs[newMsgs.length - 1];
                  if (parsed.citations) lastMsg.citations = parsed.citations;
                  if (parsed.confidence !== undefined) lastMsg.confidence = parsed.confidence;
                  if (parsed.is_grounded !== undefined) lastMsg.is_grounded = parsed.is_grounded;
                  lastMsg.streaming = false;
                  return newMsgs;
                });
              }
            } catch (e) {
              console.error("Error parsing SSE chunk JSON:", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("API Fetch error:", error);
    } finally {
      setController(null);
    }
  };

  const abortStreaming = async () => {
    if (controller) {
      controller.abort();
      // Set Last Message Status to Not Streaming
      setMessages((prev) => {
        const newMsgs = [...prev];
        if (newMsgs.length > 0) {
          newMsgs[newMsgs.length - 1].streaming = false;
          newMsgs[newMsgs.length - 1].user_aborted = true;
        }
        return newMsgs;
      });
      setController(null);
    }
  };

  const isStreaming = controller !== null;

  return (
    <div className="chat-container">
      <h2>Medicare Policy Assistant</h2>
      <h2>(Student: Robin Dua)</h2>
      <div className="message-list">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div>
              {msg.text}
              {msg.streaming && (
                <span className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </span>
              )}
            </div>
            
            {msg.citations && msg.citations.length > 0 && (
              <div className="citations-container">
                <strong>Citations:</strong>
                {msg.citations.map((cit, cIdx) => (
                  <div key={cIdx} className="citation-item">
                    [{cIdx + 1}] {cit.source_uri} — "{cit.quote}"
                  </div>
                ))}
              </div>
            )}
            {msg.role === 'assistant' && !msg.streaming && !msg.user_aborted && (
              <div className="message-footer">
                <strong>Confidence:</strong> {typeof msg.confidence === 'number' ? msg.confidence.toFixed(2) : msg.confidence} | <strong>Grounded:</strong> {msg.is_grounded ? 'Yes' : 'No'}
              </div>
            )}
            {msg.user_aborted &&(
              <div className="message-footer aborted">
                <strong>Request Aborted By User.</strong>
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="input-container">
        <input 
          type="text" 
          value={inputValue} 
          onChange={(e) => setInputValue(e.target.value)} 
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask a question about the CMS Manual..."
          className="chat-input"
          disabled={isStreaming}
        />
        <button onClick={sendMessage} className="chat-button" disabled={isStreaming}>
            <i className="bi bi-send-fill"></i>
        </button>
        {isStreaming && (
          <button onClick={abortStreaming} className="stop-streaming-button">
            <i className="bi bi-stop-circle"></i>
          </button>
        )}
      </div>
    </div>
  );
}

export default ChatApp;