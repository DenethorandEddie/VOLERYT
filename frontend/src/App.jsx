import React from 'react';
import SearchBar from './components/SearchBar/SearchBar';
import FilterPanel from './components/FilterPanel/FilterPanel';
import NicheStats from './components/NicheStats/NicheStats';
import ResultsTable from './components/ResultsTable/ResultsTable';
import ExportButton from './components/ExportButton/ExportButton';
import LoadingSpinner from './components/LoadingSpinner/LoadingSpinner';
import { useSearch } from './hooks/useSearch';
import { useFilters } from './hooks/useFilters';
import './styles/index.css';

function App() {
  const { results, loading, error, performSearch } = useSearch();
  const { filters, updateFilter } = useFilters();

  const handleSearch = async (niche) => {
    try {
      await performSearch(niche, filters);
    } catch (err) {
      console.error('Search error:', err);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🎬 YouTube Niche Analyzer</h1>
        <p>Find low-competition YouTube niches with data-driven insights</p>
      </header>

      <div className="container">
        <div className="card">
          <SearchBar onSearch={handleSearch} loading={loading} />
        </div>

        <FilterPanel filters={filters} onFilterChange={updateFilter} />

        {error && (
          <div className="card">
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {loading && (
          <div className="card">
            <LoadingSpinner message="Analyzing YouTube niche... This may take a moment." />
          </div>
        )}

        {results && !loading && (
          <>
            <NicheStats results={results} />

            <div className="card">
              <ResultsTable channels={results.channels} />
              <ExportButton channels={results.channels} />
            </div>

            {results.quota_remaining !== null && results.quota_remaining !== undefined && (
              <div className="info-message">
                API Quota Remaining: {results.quota_remaining} units | Quota Used: {results.quota_used} units
              </div>
            )}
          </>
        )}

        {!results && !loading && !error && (
          <div className="card">
            <div className="info-message">
              <h3>How to use:</h3>
              <ol style={{ marginLeft: '20px', marginTop: '10px' }}>
                <li>Enter a niche keyword (e.g., "basketball highlights", "cooking tutorials")</li>
                <li>Adjust filters for channel age and video count</li>
                <li>Click "Search Niche" to analyze</li>
                <li>Review results and export data as CSV or JSON</li>
              </ol>
              <p style={{ marginTop: '16px', fontStyle: 'italic' }}>
                <strong>Note:</strong> Channel age is calculated from the first video upload, not channel creation date.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
