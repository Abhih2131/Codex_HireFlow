from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from app.db.session import SessionLocal
from app.api.auth import router as auth_router
from app.api.employees import router as employees_router
from app.api.appusers import router as appusers_router
from app.api.workflows import router as workflows_router

app = FastAPI(title="WorkplaceAI HireFlow API")
app.include_router(auth_router, prefix="/api")
app.include_router(employees_router, prefix="/api")
app.include_router(appusers_router, prefix="/api")
app.include_router(workflows_router, prefix="/api")

scheduler = BackgroundScheduler()


def check_expired_offers():
    db = SessionLocal()
    db.execute(text("update offers set status='Expired', updated_at=now() where status='OfferSent' and created_at + (validity_days || ' days')::interval < now()"))
    db.commit()
    db.close()


@app.on_event("startup")
def startup_event():
    scheduler.add_job(check_expired_offers, "interval", minutes=30)
    scheduler.start()


@app.get("/health")
def health():
    return {"ok": True}
