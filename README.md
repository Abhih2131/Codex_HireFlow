# WorkplaceAI HireFlow — Configure workflows. Not code.

## Quickstart
- Clone repo
- Windows: double click `run.bat`
- Mac/Linux: `./run.sh`

This will:
1. Start PostgreSQL in Docker
2. Setup Python venv + dependencies
3. Run Alembic migrations
4. Run seed (creates Super Admin: `admin@workplaceai.local`)
5. Start API on `http://localhost:8000`
6. Start Web on `http://localhost:3000`

## Login (DEV)
- Open `/login`
- Request OTP for `admin@workplaceai.local`
- Use OTP from UI/console (`123456` default)

## Stop
- Mac/Linux: `pkill -f uvicorn && pkill -f next`
- Windows: close spawned terminals
- DB: `docker compose down`

## Env
- API: `apps/api/.env.example`
- WEB: `apps/web/.env.example`

## Data import
- Place real excel at `data/employee_master.xlsx` (gitignored)
- Committed sanitized sample is `data/employee_master.sample.csv`
- `/employees` import accepts `.xlsx` (sheet `Master`) and `.csv`.
