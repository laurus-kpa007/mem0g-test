import React, { useState } from 'react';
import { chatAPI } from '../../services/api';
import './ChatInterface.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'system';
  timestamp: Date;
  memories?: any[];
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [userId] = useState('user_' + Date.now());
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!inputText.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage(inputText, userId);

      const systemMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.message,
        sender: 'system',
        timestamp: new Date(),
        memories: response.data.memories,
      };

      setMessages(prev => [...prev, systemMessage]);
    } catch (error) {
      console.error('메시지 전송 실패:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: '❌ 메시지 전송에 실패했습니다. API 서버를 확인해주세요.',
        sender: 'system',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>💬 대화형 메모리 테스트</h2>
        <p>메시지를 입력하면 자동으로 엔티티와 관계를 추출하여 그래프에 저장됩니다.</p>
        <div className="user-info">사용자 ID: <code>{userId}</code></div>
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>👋 안녕하세요! 메시지를 입력해보세요.</p>
            <div className="example-messages">
              <p><strong>예시:</strong></p>
              <ul>
                <li>"나는 서울에 살고 있어요"</li>
                <li>"Alice는 개발자이고 Bob은 디자이너야"</li>
                <li>"오늘 강남역에서 친구를 만났어"</li>
              </ul>
            </div>
          </div>
        ) : (
          messages.map(message => (
            <div key={message.id} className={`message ${message.sender}`}>
              <div className="message-content">
                <p>{message.text}</p>
                {message.memories && message.memories.length > 0 && (
                  <div className="related-memories">
                    <strong>관련 메모리 ({message.memories.length}개):</strong>
                    <ul>
                      {message.memories.slice(0, 3).map((mem, idx) => (
                        <li key={idx}>{mem.memory || JSON.stringify(mem)}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString('ko-KR')}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="message system loading">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
      </div>

      <div className="input-container">
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="메시지를 입력하세요... (Enter: 전송, Shift+Enter: 줄바꿈)"
          rows={3}
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading || !inputText.trim()}>
          {loading ? '전송 중...' : '전송'}
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
