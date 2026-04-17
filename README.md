# 水蛇座 Hydrus

![CI](https://github.com/anaellezou/hydrus/actions/workflows/ci.yml/badge.svg)

A minimalist JLPT study app — browse kanji, vocabulary, and grammar from N5 to N1.
/!\ For now, only N5 level is available /!\

---

## Stack

**Backend** — Python · Flask · SQLite · Docker  
**Frontend** — React · Vite · Styled Components  
**Infrastructure** — Docker Compose

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Run the app

```bash
git clone https://github.com/anaellezou/hydrus.git
cd hydrus
docker-compose up --build
```

The app will be available at **http://localhost:5173**

The database is created automatically on first launch.

---

## Project Structure

```
hydrus/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── kanji/
│   │   │   ├── vocabulary/
│   │   │   └── grammar/
│   │   ├── database/
│   │   └── resources/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── App.jsx
│   ├── public/
│   └── Dockerfile
└── docker-compose.yml
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/kanji/?level=N5` | List kanji, filter by level |
| GET | `/api/kanji/<id>` | Get kanji by ID |
| GET | `/api/vocabulary/?level=N5` | List vocabulary, filter by level |
| GET | `/api/vocabulary/<id>` | Get vocabulary by ID |
| GET | `/api/grammar/?level=N5` | List grammar points, filter by level |
| GET | `/api/grammar/<id>` | Get grammar point by ID |

---

## Development

### Backend only

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/database/create_db.py
python app.py
```

### Run tests

```bash
cd backend
pytest -v
```

---

## Environment Variables

Create a `.env` file in `backend/` based on `.env.example`:

```
SECRET_KEY=your_secret_key_here
```
