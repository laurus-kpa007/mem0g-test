import React, { useState } from 'react';
import { testAPI } from '../../services/api';
import './TestPanel.css';

const TestPanel: React.FC = () => {
  const [testText, setTestText] = useState('');
  const [entities, setEntities] = useState<any[]>([]);
  const [relationships, setRelationships] = useState<any[]>([]);
  const [benchmarkResult, setBenchmarkResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runEntityTest = async () => {
    if (!testText.trim()) {
      alert('테스트 텍스트를 입력해주세요');
      return;
    }

    setLoading(true);
    try {
      const response = await testAPI.extractEntities(testText);
      setEntities(response.data.entities || []);
      setRelationships(response.data.relationships || []);
    } catch (error) {
      console.error('엔티티 추출 실패:', error);
      alert('엔티티 추출에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const runBenchmark = async () => {
    setLoading(true);
    try {
      const response = await testAPI.runBenchmark();
      setBenchmarkResult(response.data);
    } catch (error) {
      console.error('벤치마크 실패:', error);
      alert('벤치마크에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="test-panel">
      <div className="test-header">
        <h2>🧪 테스트 패널</h2>
        <p>Mem0g의 다양한 기능을 테스트합니다.</p>
      </div>

      <div className="test-section">
        <h3>엔티티 추출 테스트</h3>
        <p>텍스트에서 엔티티와 관계를 추출합니다.</p>

        <textarea
          value={testText}
          onChange={(e) => setTestText(e.target.value)}
          placeholder="테스트할 텍스트를 입력하세요&#10;예: Alice는 서울에서 Bob을 만났다."
          rows={4}
        />

        <button onClick={runEntityTest} disabled={loading}>
          {loading ? '처리 중...' : '엔티티 추출'}
        </button>

        {entities.length > 0 && (
          <div className="result-box">
            <h4>추출된 엔티티 ({entities.length}개)</h4>
            <div className="entity-list">
              {entities.map((entity, idx) => (
                <div key={idx} className="entity-badge">
                  {entity.name || entity.text} ({entity.type})
                </div>
              ))}
            </div>
          </div>
        )}

        {relationships.length > 0 && (
          <div className="result-box">
            <h4>추출된 관계 ({relationships.length}개)</h4>
            <div className="relationship-list">
              {relationships.map((rel, idx) => (
                <div key={idx} className="relationship-item">
                  {rel.source} → [{rel.type}] → {rel.target}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="test-section">
        <h3>성능 벤치마크</h3>
        <p>메모리 추가 및 검색 성능을 측정합니다.</p>

        <button onClick={runBenchmark} disabled={loading}>
          {loading ? '실행 중...' : '벤치마크 실행'}
        </button>

        {benchmarkResult && (
          <div className="result-box">
            <h4>벤치마크 결과</h4>
            <div className="benchmark-results">
              <div className="benchmark-item">
                <span>메모리 추가:</span>
                <strong>{benchmarkResult.add_memory_ms}ms</strong>
              </div>
              <div className="benchmark-item">
                <span>메모리 검색:</span>
                <strong>{benchmarkResult.search_memory_ms}ms</strong>
              </div>
              <div className="benchmark-item">
                <span>상태:</span>
                <strong className="success">{benchmarkResult.status}</strong>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TestPanel;
