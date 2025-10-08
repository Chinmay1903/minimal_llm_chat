# Minimal LLM Chat (FastAPI + React)
Minimal full‑stack app that fulfills the assignment requirements.


## Run locally


### 1) Backend
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env # fill DATABASE_URL & OPENAI_API_KEY
python -m backend.seed_models # creates table + seeds models
uvicorn backend.app:app --reload


### 2) Frontend
cd frontend && npm i && npm run dev
# or build: npm run build && copy dist/* to backend/static


## Endpoints
GET /api/models
POST /api/chat # body: { "model_id": "uuid", "message": "..." }


## Cost formula
cost = (input_tokens * cost_per_input_token) + (output_tokens * cost_per_output_token)


## Heroku deploy
heroku buildpacks:set heroku/python
heroku config:set OPENAI_API_KEY=...
heroku config:set CORS_ORIGINS="*"
git init && git add . && git commit -m "init"
git remote add heroku https://git.heroku.com/<your-app>.git
git push heroku HEAD:main
heroku run python -m backend.seed_models
