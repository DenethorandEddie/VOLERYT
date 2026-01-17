import React from 'react';
import './NicheStats.css';

const NicheStats = ({ results }) => {
  if (!results) return null;

  const { total_channels_found, niche_pool_size, analysis } = results;

  const getCompetitionColor = (level) => {
    switch (level) {
      case 'ideal':
        return '#10B981';
      case 'good':
        return '#3B82F6';
      case 'competitive':
        return '#F59E0B';
      case 'saturated':
        return '#EF4444';
      default:
        return '#6B7280';
    }
  };

  const getCompetitionLabel = (level) => {
    switch (level) {
      case 'ideal':
        return 'Ideal Niche';
      case 'good':
        return 'Good Niche';
      case 'competitive':
        return 'Competitive';
      case 'saturated':
        return 'Saturated';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className="niche-stats">
      <h3 className="stats-title">Niche Analysis Results</h3>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{total_channels_found}</div>
          <div className="stat-label">Channels Found</div>
          <div className="stat-hint">
            {total_channels_found <= 5 ? '✓ Excellent!' : total_channels_found <= 10 ? '✓ Good' : '⚠ High'}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-value">{niche_pool_size}</div>
          <div className="stat-label">Videos in Niche Pool</div>
          <div className="stat-hint">
            {niche_pool_size <= 50 ? '✓ Excellent!' : niche_pool_size <= 100 ? '✓ Good' : '⚠ High'}
          </div>
        </div>

        <div className="stat-card competition-card" style={{ borderColor: getCompetitionColor(analysis.competition_level) }}>
          <div className="competition-badge" style={{ backgroundColor: getCompetitionColor(analysis.competition_level) }}>
            {getCompetitionLabel(analysis.competition_level)}
          </div>
          <div className="stat-label">Competition Level</div>
        </div>
      </div>

      <div className="analysis-reasons">
        <h4>Analysis Details:</h4>
        <ul>
          {analysis.reasons.map((reason, index) => (
            <li key={index}>{reason}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default NicheStats;
