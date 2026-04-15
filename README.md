# Sprechen — Personal German Tutor

## What is Sprechen?
A personal web app for learning German with AI pronunciation coaching and Goethe exam prep. Runs entirely on your machine — no cloud, no fees, no account management.

## Prerequisites
- Python 3.11+
- Node.js 18+
- ffmpeg (for audio conversion)

## API Key (free)
**Groq** (STT + AI conversations + pronunciation analysis): https://console.groq.com → API Keys → Create

One key covers everything — Whisper transcription, LLaMA conversations, and pronunciation feedback.

## Installation

### Step 1: Clone
```bash
git clone ... && cd sprechen
```

### Step 2: Set API key
```bash
cd sprechen-backend
cp .env.example .env
# Open .env and set GROQ_API_KEY
```

### Step 3: Start
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```
Browser opens automatically at http://localhost:5173

## Features
- **Pronunciation Coach**: Speak German sentences, get AI-powered feedback (Whisper + Groq LLM)
- **AI Conversations**: Practice in real scenarios (bakery, doctor, job interview, ...)
- **30 Lessons**: A1 to B2, fully in German
- **Vocabulary**: Spaced repetition (SM-2) with daily cards
- **Goethe Exam**: Simulator for Reading, Listening, Writing, Speaking — A1 to B2
- **Progress**: XP system, streaks, pronunciation trends, study heatmap, achievements

## Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `Alt+H` | Home |
| `Alt+L` | Lessons |
| `Alt+S` | Conversation |
| `Alt+V` | Vocabulary |
| `Alt+P` | Exam |
| `Alt+F` | Progress |
| `?` | Shortcut overview |

## Daily Usage
```bash
# Create backup
python scripts/backup.py

# View logs
tail -f logs/sprechen.log

# Reset database
rm sprechen.db && python scripts/seed_db.py
```

## Cost
| Service | Free tier |
|---------|-----------|
| Groq (Whisper + LLaMA) | 14,400 requests/day |
| Edge TTS | Unlimited |

No Azure account needed. Everything runs on the free Groq tier.

## Project Structure
```
sprechen/
├── sprechen-backend/   # FastAPI + SQLite
│   ├── core/           # config, cache, logger
│   ├── models/         # SQLAlchemy + Pydantic schemas
│   ├── services/       # business logic
│   ├── routers/        # HTTP routes
│   ├── data/           # lesson + exam seeds
│   └── scripts/        # start.sh, seed_db.py, backup.py
└── sprechen-web/       # React + Vite frontend
    └── src/
        ├── components/
        ├── pages/
        ├── hooks/
        └── store/
```
