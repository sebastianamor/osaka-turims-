# 🏯 Osaka Explorer – Tourist Web App

A full-featured tourism web application for visitors to Osaka, Japan.  
Built with **Python (Flask)** backend and **SQLite** database for user authentication.

---

## Features

- **Login / Register system** with SQLite (passwords hashed with SHA-256)
- **Explore page** with 12 famous Osaka locations (castles, food, hotels, parks, nightlife)
- **Interactive map** powered by OpenStreetMap / Leaflet.js
- **Favorites system** – save/unsave places per user account
- **Reviews system** – rate (1–5 stars) and comment on any location
- **Transport Guide** – IC cards, metro lines, practical tips
- **History of Osaka** – illustrated timeline from ancient Naniwa to today
- **3 languages** – English, Español, 中文 (switchable live)
- **Traditional Japanese aesthetic** – Shippori Mincho fonts, red & gold palette

---

## Setup Instructions

### 1. Install Python dependencies

```bash
pip install flask
```

### 2. Run the app

```bash
cd osaka_tourism
python app.py
```

### 3. Open in browser

```
http://localhost:5000
```

The SQLite database (`osaka.db`) is created automatically on first run.

---

## Project Structure

```
osaka_tourism/
├── app.py                  # Flask app + SQLite routes
├── requirements.txt
├── osaka.db                # Auto-created SQLite database
└── templates/
    ├── base.html           # Shared layout, nav, language switcher
    ├── index.html          # Homepage (hero, features, CTA)
    ├── login.html          # Login form
    ├── register.html       # Registration form
    ├── explore.html        # Main explore page (map + cards + reviews)
    ├── transport.html      # Transport guide
    └── history.html        # Historical timeline
```

---

## Database Schema (SQLite)

```sql
users (id, username, email, password[hashed], language, created_at)
favorites (id, user_id, place_id)
reviews (id, user_id, place_id, rating, comment, created_at)
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/favorites` | Get user's saved favorites |
| POST | `/api/favorites` | Add a favorite |
| DELETE | `/api/favorites` | Remove a favorite |
| GET | `/api/reviews?place_id=X` | Get reviews for a place |
| POST | `/api/reviews` | Submit a review |

---

## Languages

Switch language anytime using the language bar at the top.  
All place names, descriptions, UI labels and navigation translate in real-time.

---

## Tech Stack

- **Backend**: Python 3 + Flask
- **Database**: SQLite (via Python's built-in `sqlite3`)
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Map**: Leaflet.js + OpenStreetMap (free, no API key needed)
- **Fonts**: Google Fonts – Shippori Mincho + Noto Sans JP + Noto Serif JP
