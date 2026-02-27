from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import AuthOtp, AppUser
from app.core.config import settings
from app.utils.security import hash_text, verify_text, create_access_token
from app.services.audit import write_audit

router = APIRouter(prefix="/auth", tags=["auth"])

class OtpRequest(BaseModel):
    identifier: str

class OtpVerify(BaseModel):
    identifier: str
    code: str

@router.post("/otp/request")
def request_otp(payload: OtpRequest, db: Session = Depends(get_db)):
    code = settings.dev_otp
    rec = AuthOtp(
        identifier=payload.identifier,
        code_hash=hash_text(code),
        expires_at=datetime.utcnow() + timedelta(minutes=settings.otp_ttl_minutes),
    )
    db.add(rec)
    db.commit()
    print(f"DEV OTP for {payload.identifier}: {code}")
    return {"message": "OTP sent", "dev_otp": code}

@router.post("/otp/verify")
def verify_otp(payload: OtpVerify, db: Session = Depends(get_db)):
    otp = db.query(AuthOtp).filter(AuthOtp.identifier == payload.identifier).order_by(AuthOtp.id.desc()).first()
    if not otp or otp.expires_at < datetime.utcnow() or not verify_text(payload.code, otp.code_hash):
        raise HTTPException(400, "Invalid OTP")
    user = db.query(AppUser).filter(AppUser.email == payload.identifier).first()
    if not user:
        raise HTTPException(403, "You must be provisioned")
    token = create_access_token({"sub": user.id, "role": user.role})
    write_audit(db, "auth", str(user.id), "login")
    return {"access_token": token, "user": {"id": user.id, "role": user.role, "employee_id": user.employee_id}}
