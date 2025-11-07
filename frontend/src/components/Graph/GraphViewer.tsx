import React, { useState } from 'react';
import { graphAPI } from '../../services/api';
import './GraphViewer.css';

const GraphViewer: React.FC = () => {
  const [userId, setUserId] = useState('');
  const [nodes, setNodes] = useState<any[]>([]);
  const [edges, setEdges] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const loadGraph = async () => {
    if (!userId.trim()) {
      alert('사용자 ID를 입력해주세요');
      return;
    }

    setLoading(true);
    try {
      const [graphRes, statsRes] = await Promise.all([
        graphAPI.visualize(userId, 100),
        graphAPI.getStats(userId),
      ]);

      setNodes(graphRes.data.nodes || []);
      setEdges(graphRes.data.edges || []);
      setStats(statsRes.data);
    } catch (error) {
      console.error('그래프 로드 실패:', error);
      alert('그래프 로드에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="graph-viewer">
      <div className="graph-header">
        <h2>🕸️ 그래프 시각화</h2>
        <p>사용자의 메모리를 그래프 형태로 시각화합니다.</p>
      </div>

      <div className="graph-controls">
        <input
          type="text"
          placeholder="사용자 ID 입력"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <button onClick={loadGraph} disabled={loading}>
          {loading ? '로딩 중...' : '그래프 로드'}
        </button>
      </div>

      {stats && (
        <div className="graph-stats">
          <div className="stat-card">
            <div className="stat-value">{stats.node_count}</div>
            <div className="stat-label">노드</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.edge_count}</div>
            <div className="stat-label">엣지</div>
          </div>
        </div>
      )}

      <div className="graph-container">
        {nodes.length === 0 ? (
          <div className="empty-state">
            <p>🔍 그래프 데이터가 없습니다</p>
            <p>사용자 ID를 입력하고 로드 버튼을 클릭하세요</p>
          </div>
        ) : (
          <div className="node-list">
            <h3>노드 목록 ({nodes.length}개)</h3>
            {nodes.map(node => (
              <div key={node.id} className="node-item">
                <div className="node-name">{node.name}</div>
                <div className="node-type">{node.type}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default GraphViewer;
