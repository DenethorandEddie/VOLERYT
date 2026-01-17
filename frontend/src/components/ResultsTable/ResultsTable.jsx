import React, { useState } from 'react';
import TierBadge from '../TierBadge/TierBadge';
import './ResultsTable.css';

const ResultsTable = ({ channels }) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [expandedRow, setExpandedRow] = useState(null);

  if (!channels || channels.length === 0) {
    return (
      <div className="no-results">
        <p>No channels found matching your criteria.</p>
      </div>
    );
  }

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedChannels = [...channels].sort((a, b) => {
    if (!sortConfig.key) return 0;

    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];

    if (aValue < bValue) {
      return sortConfig.direction === 'asc' ? -1 : 1;
    }
    if (aValue > bValue) {
      return sortConfig.direction === 'asc' ? 1 : -1;
    }
    return 0;
  });

  const toggleExpand = (index) => {
    setExpandedRow(expandedRow === index ? null : index);
  };

  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  return (
    <div className="results-table-container">
      <h3 className="results-title">Found {channels.length} Channels</h3>

      <div className="table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('channel_name')}>
                Channel Name {sortConfig.key === 'channel_name' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
              </th>
              {channels[0]?.detected_niche && (
                <th onClick={() => handleSort('detected_niche')}>
                  Detected Niche {sortConfig.key === 'detected_niche' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                </th>
              )}
              <th onClick={() => handleSort('tier')}>
                Tier {sortConfig.key === 'tier' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('age_days')}>
                Age {sortConfig.key === 'age_days' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('video_count')}>
                Videos {sortConfig.key === 'video_count' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('subscriber_count')}>
                Subscribers {sortConfig.key === 'subscriber_count' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('total_views')}>
                Total Views {sortConfig.key === 'total_views' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sortedChannels.map((channel, index) => (
              <React.Fragment key={channel.channel_id}>
                <tr className={expandedRow === index ? 'expanded' : ''}>
                  <td>
                    <div className="channel-info">
                      {channel.thumbnail_url && (
                        <img src={channel.thumbnail_url} alt={channel.channel_name} className="channel-thumbnail" />
                      )}
                      <div>
                        <div className="channel-name">{channel.channel_name}</div>
                        <div className="channel-age-desc">{channel.age_description} old</div>
                      </div>
                    </div>
                  </td>
                  {channel.detected_niche && (
                    <td>
                      <div className="detected-niche">{channel.detected_niche}</div>
                      {channel.keywords && channel.keywords.length > 0 && (
                        <div className="small-text niche-keywords">
                          {channel.keywords.slice(0, 3).join(', ')}
                        </div>
                      )}
                    </td>
                  )}
                  <td>
                    <TierBadge tier={channel.tier} color={channel.tier_color} />
                  </td>
                  <td>
                    <div>{channel.age_days} days</div>
                    <div className="small-text">{channel.first_upload_date}</div>
                  </td>
                  <td className="number-cell">{channel.video_count}</td>
                  <td className="number-cell">{formatNumber(channel.subscriber_count)}</td>
                  <td className="number-cell">
                    <div>{formatNumber(channel.total_views)}</div>
                    <div className="small-text">{formatNumber(channel.avg_views_per_video)} avg</div>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <a href={channel.channel_url} target="_blank" rel="noopener noreferrer" className="btn-link">
                        View
                      </a>
                      {channel.viral_videos.length > 0 && (
                        <button onClick={() => toggleExpand(index)} className="btn-expand">
                          {expandedRow === index ? 'Hide' : 'Viral Videos'}
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
                {expandedRow === index && channel.viral_videos.length > 0 && (
                  <tr className="expanded-row">
                    <td colSpan={channel.detected_niche ? "8" : "7"}>
                      <div className="viral-videos">
                        <h4>Viral Videos:</h4>
                        <ul>
                          {channel.viral_videos.map((video) => (
                            <li key={video.video_id}>
                              <strong>{video.title}</strong>
                              <br />
                              Views: {formatNumber(video.view_count)} | Published: {video.published_at}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ResultsTable;
