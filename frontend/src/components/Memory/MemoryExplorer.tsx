import React, { useState } from 'react';
import { memoryAPI } from '../../services/api';
import './MemoryExplorer.css';

const MemoryExplorer: React.FC = () => {
  const [userId, setUserId] = useState('');
  const [memories, setMemories] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const loadAllMemories = async () => {
    if (!userId.trim()) {
      alert('사용자 ID를 입력해주세요');
      return;
    }

    setLoading(true);
    try {
      const response = await memoryAPI.getAll(userId, 100);
      setMemories(response.data || []);
    } catch (error) {
      console.error('메모리 로드 실패:', error);
      alert('메모리 로드에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const searchMemories = async () => {
    if (!userId.trim() || !searchQuery.trim()) {
      alert('사용자 ID와 검색어를 입력해주세요');
      return;
    }

    setLoading(true);
    try {
      const response = await memoryAPI.search(searchQuery, userId, 20);
      setMemories(response.data.results || []);
    } catch (error) {
      console.error('메모리 검색 실패:', error);
      alert('메모리 검색에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const deleteAllMemories = async () => {
    if (!userId.trim()) {
      alert('사용자 ID를 입력해주세요');
      return;
    }

    if (!window.confirm('정말 모든 메모리를 삭제하시겠습니까?')) {
      return;
    }

    setLoading(true);
    try {
      await memoryAPI.deleteAll(userId);
      setMemories([]);
      alert('모든 메모리가 삭제되었습니다.');
    } catch (error) {
      console.error('메모리 삭제 실패:', error);
      alert('메모리 삭제에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="memory-explorer">
      <div className="memory-header">
        <h2>📚 메모리 탐색기</h2>
        <p>저장된 메모리를 조회하고 검색합니다.</p>
      </div>

      <div className="memory-controls">
        <input
          type="text"
          placeholder="사용자 ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <button onClick={loadAllMemories} disabled={loading}>
          전체 조회
        </button>
      </div>

      <div className="search-controls">
        <input
          type="text"
          placeholder="검색어 입력"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button onClick={searchMemories} disabled={loading}>
          검색
        </button>
        <button onClick={deleteAllMemories} disabled={loading} className="danger">
          전체 삭제
        </button>
      </div>

      <div className="memory-list">
        {loading ? (
          <div className="loading-state">로딩 중...</div>
        ) : memories.length === 0 ? (
          <div className="empty-state">
            <p>📭 메모리가 없습니다</p>
          </div>
        ) : (
          <>
            <h3>메모리 목록 ({memories.length}개)</h3>
            {memories.map((memory, idx) => (
              <div key={idx} className="memory-item">
                <div className="memory-content">
                  {memory.memory || JSON.stringify(memory)}
                </div>
                {memory.created_at && (
                  <div className="memory-meta">
                    생성: {new Date(memory.created_at).toLocaleString('ko-KR')}
                  </div>
                )}
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
};

export default MemoryExplorer;
