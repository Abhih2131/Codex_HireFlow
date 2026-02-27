@echo off
where python >nul 2>nul || (echo python missing & exit /b 1)
where node >nul 2>nul || (echo node missing & exit /b 1)
where docker >nul 2>nul || (echo docker missing & exit /b 1)
call docker-up.bat
cd apps\api
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m scripts.seed
start "HireFlow API" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8000"
cd ..\web
npm install
start "HireFlow Web" cmd /k "npm run dev"
echo API: http://localhost:8000 WEB: http://localhost:3000
