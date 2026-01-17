# 🎬 YouTube Niche Analyzer

A full-stack web application to analyze YouTube niches and find low-competition opportunities for content creators.

## Features

- 🔍 **Niche Search**: Search for channels by niche keyword
- 📊 **Competition Analysis**: Analyze channel count and video pool size
- 🏆 **Tier-Based Scoring**: S+, Great, Good, Average, Possible tiers based on channel age
- 📈 **Viral Video Detection**: Identify viral videos using statistical analysis
- 📥 **Export Functionality**: Export results to CSV or JSON
- ⚡ **Real-time Quota Tracking**: Monitor YouTube API quota usage

## Niche Criteria

### Channel Age Tiers (from first upload)
- **S+ Tier**: ≤7 days (1 week)
- **Great**: ≤30 days (1 month)
- **Good**: ≤60 days (2 months)
- **Average**: ≤90 days (3 months)
- **Possible**: ≤150 days (5 months)

### Competition Levels
- **Ideal**: ≤5 channels AND ≤50 videos in niche pool
- **Good**: ≤10 channels AND ≤100 videos in niche pool
- **Competitive**: ≤20 channels AND ≤200 videos
- **Saturated**: >20 channels OR >200 videos

### Important Notes
- Channel age is calculated from **first upload date**, NOT channel creation date
- English channels only
- Maximum 15 videos per channel (ideal for new niches)

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **YouTube Data v3 API**: Channel and video data
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **React**: UI library
- **Axios**: HTTP client
- **CSS3**: Styling with gradients and animations

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- YouTube Data v3 API key

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your YouTube API key
```

5. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/health`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env if needed (default: http://localhost:8000)
```

4. Run the development server:
```bash
npm start
```

The app will be available at `http://localhost:3000`

## Usage

1. **Enter Niche Keyword**: Type a niche keyword (e.g., "basketball highlights", "cooking tutorials")

2. **Adjust Filters**:
   - Maximum channel age (7-180 days)
   - Maximum videos per channel (1-50)

3. **Search**: Click "Search Niche" to analyze

4. **Review Results**:
   - View channel statistics
   - Check tier ratings
   - See viral videos
   - Analyze competition metrics

5. **Export Data**: Download results as CSV or JSON

## API Endpoints

### Search Niche
```
POST /api/v1/search/niche
```
Request:
```json
{
  "niche": "basketball highlights",
  "max_channel_age_days": 180,
  "max_videos_per_channel": 15,
  "max_results": 50
}
```

### Health Check
```
GET /api/v1/health
```

### Quota Info
```
GET /api/v1/quota
```

### Export CSV
```
POST /api/v1/export/csv
```

### Export JSON
```
POST /api/v1/export/json
```

## API Quota Management

- Daily limit: 10,000 units
- Search cost: ~115 units per query
- Maximum ~85 searches per day
- Results are cached for 24 hours

## Project Structure

```
VOLERYT/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration
│   │   ├── services/
│   │   │   ├── youtube_api.py   # YouTube API client
│   │   │   ├── niche_analyzer.py # Analysis algorithm
│   │   │   └── quota_manager.py  # Quota tracking
│   │   ├── api/routes/
│   │   │   ├── search.py        # Search endpoints
│   │   │   └── export.py        # Export endpoints
│   │   ├── schemas/             # Pydantic models
│   │   └── utils/               # Utilities
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main app component
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks
│   │   ├── services/            # API client
│   │   └── styles/              # CSS files
│   └── package.json
│
└── README.md
```

## Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

### Code Formatting

Backend:
```bash
black app/
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Support

For issues and questions:
- Open an issue on GitHub
- Check API documentation at `/docs`

## Acknowledgments

- YouTube Data API v3
- FastAPI framework
- React library
