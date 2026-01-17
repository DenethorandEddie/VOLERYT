import React, { useState } from 'react';
import { exportToCSV, exportToJSON } from '../../services/api';
import './ExportButton.css';

const ExportButton = ({ channels }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState(null);

  if (!channels || channels.length === 0) {
    return null;
  }

  const handleExport = async (format) => {
    setIsExporting(true);
    setError(null);

    try {
      if (format === 'csv') {
        await exportToCSV(channels);
      } else if (format === 'json') {
        await exportToJSON(channels);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="export-button-container">
      <div className="export-buttons">
        <button
          className="export-btn export-csv"
          onClick={() => handleExport('csv')}
          disabled={isExporting}
        >
          {isExporting ? 'Exporting...' : 'Export CSV'}
        </button>
        <button
          className="export-btn export-json"
          onClick={() => handleExport('json')}
          disabled={isExporting}
        >
          {isExporting ? 'Exporting...' : 'Export JSON'}
        </button>
      </div>
      {error && <div className="export-error">{error}</div>}
    </div>
  );
};

export default ExportButton;
