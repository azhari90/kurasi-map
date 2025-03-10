# Kurasi Map

A curated map application with freemium features for discovering restaurants, cafes, venues, hospitals and more.

## Features

- Mobile-first interface with interactive map
- Curated locations across multiple categories (restaurants, cafes, sports venues, hospitals, etc.)
- Detailed information for each location (address, operating hours, contact info, etc.)
- User authentication and freemium model
- Category-based access restrictions for free users

## Tech Stack

- **Backend**: Python (FastAPI)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Frontend**: HTML, CSS, JavaScript
- **Map**: Leaflet.js

## Project Structure

```
kurasi-map/
├── app/                    # FastAPI application
│   ├── api/                # API endpoints
│   ├── core/               # Core application code
│   ├── db/                 # Database models and queries
│   ├── static/             # Static files (CSS, JS)
│   └── templates/          # HTML templates
├── migrations/             # Database migrations
├── scripts/                # Utility scripts
├── tests/                  # Test files
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.9+
- Supabase account

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/azhari90/kurasi-map.git
   cd kurasi-map
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and update with your Supabase credentials.

5. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

## Database Schema

- **locations**: Stores all location data
- **categories**: Different location categories
- **subscription_plans**: Available subscription plans
- **users**: User information
- **user_subscriptions**: Links users to their subscription plans

## License

MIT