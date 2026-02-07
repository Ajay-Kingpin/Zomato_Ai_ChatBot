# Phase 6 - Web Frontend

Modern web interface for the Zomato AI Recommendation System.

## Features

- **Modern UI**: Built with Flask and Tailwind CSS
- **Real-time AI**: Integrated with Groq LLM for recommendations
- **Interactive Form**: City suggestions, budget input, dietary preferences
- **Live Statistics**: Dataset overview and system status
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: User-friendly error messages and loading states

## Usage

### Start the Web Server
```bash
python phase6/app.py
```

The application will start on `http://localhost:5000`

### API Endpoints

- `GET /` - Main web interface
- `GET /health` - Health check endpoint
- `GET /api/cities` - Get available cities
- `GET /api/stats` - Get dataset statistics  
- `POST /api/recommendations` - Get AI recommendations

### API Request Format
```json
POST /api/recommendations
{
    "city": "Bangalore",
    "price": 800,
    "diet": "veg"
}
```

### API Response Format
```json
{
    "success": true,
    "recommendations": "Formatted recommendation text..."
}
```

## Dependencies

Phase 6 requires Flask for the web framework:
```bash
pip install flask
```

## Testing

Run the web frontend tests:
```bash
python -m pytest phase6/tests/ -v
```

## Features in Detail

### User Interface
- Clean, modern design with Tailwind CSS
- Animated loading states and transitions
- Responsive grid layout
- City auto-suggestions
- Form validation and error handling

### Backend Integration
- Uses Phase 5's complete recommendation system
- RESTful API design
- JSON request/response format
- Comprehensive error handling
- Health check endpoints

### AI Integration
- Real-time LLM recommendations
- Budget and dietary filtering
- Professional formatting of results
- Statistical insights and analytics

## Architecture

```
phase6/
├── app.py              # Flask web application
├── templates/
│   └── index.html      # Main web interface
├── tests/
│   └── test_web_frontend.py  # Web tests
└── __init__.py
```

The web frontend integrates all previous phases to provide a complete user experience for restaurant recommendations powered by AI.
