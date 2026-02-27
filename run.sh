#!/usr/bin/env bash
set -e
command -v python3 >/dev/null || { echo "python3 missing"; exit 1; }
command -v node >/dev/null || { echo "node missing"; exit 1; }
command -v docker >/dev/null || { echo "docker missing"; exit 1; }
./docker-up.sh
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../../api.log 2>&1 &
cd ../web
npm install
npm run dev > ../../web.log 2>&1 &
echo "API: http://localhost:8000 WEB: http://localhost:3000"
echo "Logs: api.log web.log. Stop: pkill -f uvicorn; pkill -f next"
wait
