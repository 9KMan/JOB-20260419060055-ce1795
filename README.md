# AI + React + Supabase MVP — Deployment & Integration (AWS)

## Overview

This is a production-ready MVP for an AI-powered application using React frontend with Supabase backend and AWS deployment.

## Tech Stack

- **Frontend**: React 18 + Vite + TypeScript
- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15 via Supabase
- **AI**: OpenAI API integration
- **Deployment**: AWS (ECS, RDS, S3, CloudFront)
- **Container**: Docker + Docker Compose

## Project Structure

```
├── backend/           # FastAPI backend service
│   ├── app/
│   │   ├── main.py           # FastAPI application entry
│   │   ├── api/              # API routes
│   │   ├── models/           # Pydantic models
│   │   ├── services/         # Business logic
│   │   └── core/             # Config, security
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/          # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── services/
│   ├── package.json
│   └── Dockerfile
├── aws/               # AWS infrastructure as code
│   ├── ecs-task-definition.json
│   ├── docker-compose.yml
│   └── buildspec.yml
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- AWS CLI configured

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker Deployment

```bash
docker-compose up --build
```

## Features

- [x] User authentication with Supabase Auth
- [x] AI-powered content generation
- [x] Real-time data sync with Supabase
- [x] AWS ECS container deployment
- [x] PostgreSQL database with migrations
- [x] Comprehensive test suite
- [x] CI/CD pipeline with AWS CodeBuild

## Environment Variables

See `.env.example` files in backend and frontend directories.

## License

MIT