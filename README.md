# Map Recommendations API

A real-time location-based recommendations API built with FastAPI. The goal is to provide personalized place recommendations based on user preferences and enable social features like chat between users.

## Project Vision

- **Real-time map** with location recommendations
- **Personalized suggestions** based on user likes and preferences
- **WebSocket chat** to exchange place recommendations with other users
- **Google Maps integration** for discovering interesting places

---

## Current Status

### Implemented

- [x] User authentication (register, login, JWT tokens)
- [x] User management (list, get by ID)
- [x] Database models (User, Location, Preference, Message)
- [x] Google Maps service (nearby places, place details, geocoding)
- [x] Security (password hashing, JWT validation)

### Pending

- [ ] Maps API endpoints
- [ ] Preferences CRUD endpoints
- [ ] Location tracking endpoints
- [ ] Recommendation engine
- [ ] WebSocket chat implementation
- [ ] Real-time location sharing

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern async web framework |
| **SQLAlchemy** | ORM for database operations |
| **SQLite** | Database (dev) / PostgreSQL (prod ready) |
| **python-jose** | JWT token generation and validation |
| **passlib + bcrypt** | Secure password hashing |
| **Google Maps API** | Places, geocoding, place details |
| **WebSockets** | Real-time communication (ready) |
| **Pydantic** | Data validation and serialization |

---

## Project Structure

```
map-recommendations-app/
├── app/
│   ├── api/                    # API route handlers
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── users.py            # User management endpoints
│   │   └── maps.py             # Maps endpoints (pending)
│   │
│   ├── core/                   # Core infrastructure
│   │   ├── config.py           # App settings and env variables
│   │   ├── database.py         # SQLAlchemy engine and session
│   │   ├── security.py         # Password hashing, JWT functions
│   │   └── deps.py             # Dependency injection (auth)
│   │
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── user.py             # User model
│   │   ├── location.py         # Location model
│   │   ├── preference.py       # Preference model
│   │   └── message.py          # Message model
│   │
│   ├── schemas/                # Pydantic validation schemas
│   │   ├── user.py             # User schemas
│   │   ├── location.py         # Location schemas
│   │   ├── preference.py       # Preference schemas
│   │   └── message.py          # Message schemas
│   │
│   ├── services/               # Business logic layer
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── user_service.py     # User operations
│   │   └── maps_services.py    # Google Maps API wrapper
│   │
│   └── main.py                 # FastAPI application entry point
│
├── .env                        # Environment variables (not in git)
├── .gitignore                  # Git ignore patterns
├── requirements.txt            # Python dependencies
├── app.db                      # SQLite database file
└── README.md                   # This file
```

---

## Database Models

### User
Stores user account information.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| email | String | Unique email address |
| username | String | Unique username |
| hashed_password | String | Bcrypt hashed password |
| is_active | Boolean | Account status (default: true) |
| created_at | DateTime | Registration timestamp |

**Relationships:** preferences, locations, sent_messages, received_messages

### Location
Stores user location history.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| latitude | Float | GPS latitude |
| longitude | Float | GPS longitude |
| timestamp | DateTime | When location was recorded |
| place_name | String | Optional place name |

### Preference
Stores user interests for recommendations.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| category | String | Main category (restaurants, museums, parks) |
| subcategory | String | Specific preference (italian food, modern art) |

### Message
Stores chat messages between users.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| sender_id | Integer | Foreign key to User (sender) |
| receiver_id | Integer | Foreign key to User (receiver) |
| content | String | Message text |
| timestamp | DateTime | When message was sent |
| is_read | Boolean | Read status (default: false) |

---

## API Endpoints

### Authentication `/api/v1/auth`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | No | Create new user account |
| POST | `/login` | No | Get JWT access token |
| GET | `/me` | Yes | Get current user info |

### Users `/api/v1/users`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | Yes | List all users (paginated) |
| GET | `/{user_id}` | Yes | Get user by ID |

### Maps `/api/v1/maps` (Pending)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/nearby` | Yes | Get nearby places |
| GET | `/place/{place_id}` | Yes | Get place details |
| GET | `/geocode` | Yes | Convert address to coordinates |

### Preferences (Pending)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/preferences` | Yes | Get user preferences |
| POST | `/preferences` | Yes | Add a preference |
| DELETE | `/preferences/{id}` | Yes | Remove a preference |

### Messages / Chat (Pending)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| WS | `/ws/chat` | Yes | WebSocket chat connection |
| GET | `/messages/{user_id}` | Yes | Get message history |

---

## Services

### AuthService
Handles user authentication and token creation.

```python
authenticate_user(db, credentials)  # Verify email/password
create_token(user_email)            # Generate JWT token
```

### UserService
Handles user CRUD operations.

```python
get_user_by_email(db, email)        # Find user by email
get_user_by_username(db, username)  # Find user by username
get_user_by_id(db, user_id)         # Find user by ID
create_user(db, user_data)          # Create new user
get_all_users(db, skip, limit)      # List users with pagination
```

### MapsService
Wrapper for Google Maps API.

```python
get_nearby_places(lat, lng, radius, place_type, keyword)
# Returns: place_id, name, address, types, rating, location, open_now, photos

get_place_details(place_id)
# Returns: name, address, phone, website, rating, price_level, hours, reviews

geocode_address(address)
# Returns: formatted_address, location (lat/lng), place_id
```

---

## Setup and Installation

### Prerequisites
- Python 3.10+
- Google Maps API key

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd map-recommendations-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Google Maps
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Database
DATABASE_URL=sqlite:///./app.db

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Usage Examples

### Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Access Protected Endpoint

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <your_access_token>"
```

---

## Future Roadmap

### Phase 1: Core Features
- [ ] Implement maps API endpoints
- [ ] Add preference management endpoints
- [ ] Create location tracking endpoints

### Phase 2: Recommendations
- [ ] Build recommendation algorithm
- [ ] Match user preferences with nearby places
- [ ] Implement rating and favorites system

### Phase 3: Social Features
- [ ] WebSocket chat implementation
- [ ] Real-time location sharing
- [ ] Place sharing between users
- [ ] Friend system

### Phase 4: Enhancements
- [ ] Push notifications
- [ ] Advanced filtering and search
- [ ] User reviews and ratings
- [ ] Route planning

---

## License

This project is private and under development.

---

## Author

Created as a learning project for building real-time location-based applications with FastAPI.
