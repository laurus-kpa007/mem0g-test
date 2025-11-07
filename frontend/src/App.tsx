import React, { useState, useEffect } from 'react';
import './App.css';
import ChatInterface from './components/Chat/ChatInterface';
import GraphViewer from './components/Graph/GraphViewer';
import MemoryExplorer from './components/Memory/MemoryExplorer';
import TestPanel from './components/Test/TestPanel';
import { api } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState<'chat' | 'graph' | 'memory' | 'test'>('chat');
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'error'>('checking');

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      await api.get('/ping');
      setApiStatus('connected');
    } catch (error) {
      console.error('API 연결 실패:', error);
      setApiStatus('error');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧠 Mem0g Testing Platform</h1>
        <p className="subtitle">그래프 기반 메모리 테스트 플랫폼 (한국어 최적화)</p>
        <div className={`status-indicator ${apiStatus}`}>
          {apiStatus === 'checking' && '⏳ API 확인 중...'}
          {apiStatus === 'connected' && '✅ API 연결됨'}
          {apiStatus === 'error' && '❌ API 연결 실패'}
        </div>
      </header>

      <nav className="tab-navigation">
        <button
          className={activeTab === 'chat' ? 'active' : ''}
          onClick={() => setActiveTab('chat')}
        >
          💬 채팅
        </button>
        <button
          className={activeTab === 'graph' ? 'active' : ''}
          onClick={() => setActiveTab('graph')}
        >
          🕸️ 그래프
        </button>
        <button
          className={activeTab === 'memory' ? 'active' : ''}
          onClick={() => setActiveTab('memory')}
        >
          📚 메모리
        </button>
        <button
          className={activeTab === 'test' ? 'active' : ''}
          onClick={() => setActiveTab('test')}
        >
          🧪 테스트
        </button>
      </nav>

      <main className="App-main">
        {activeTab === 'chat' && <ChatInterface />}
        {activeTab === 'graph' && <GraphViewer />}
        {activeTab === 'memory' && <MemoryExplorer />}
        {activeTab === 'test' && <TestPanel />}
      </main>

      <footer className="App-footer">
        <p>Powered by Mem0 + Ollama (Qwen2.5 + BGE-M3) + Neo4j + Qdrant</p>
      </footer>
    </div>
  );
}

export default App;
