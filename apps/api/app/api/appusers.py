from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import AppUser, Employee
from app.api.deps import require_roles
from app.services.audit import write_audit

router = APIRouter(prefix="/admin/appusers", tags=["appusers"])

class UserIn(BaseModel):
    employee_id: str
    email: str
    phone: str | None = None
    role: str
    is_active: bool = True

@router.get("")
def list_users(db: Session = Depends(get_db), user=Depends(require_roles("Super Admin", "HR Admin"))):
    return [{"id":u.id,"employee_id":u.employee_id,"email":u.email,"role":u.role,"is_active":u.is_active} for u in db.query(AppUser).all()]

@router.post("")
def upsert_user(payload: UserIn, db: Session = Depends(get_db), user=Depends(require_roles("Super Admin", "HR Admin"))):
    if not db.query(Employee).filter(Employee.employee_id == payload.employee_id).first():
        raise HTTPException(400, "employee_id not found")
    obj = db.query(AppUser).filter(AppUser.email == payload.email).first()
    before = None
    if obj:
        before = {"role": obj.role, "is_active": obj.is_active}
        for k,v in payload.model_dump().items(): setattr(obj,k,v)
    else:
        obj = AppUser(**payload.model_dump())
        db.add(obj)
    db.commit()
    write_audit(db, "app_user", str(obj.id), "upsert", user.id, user.employee_id, before, payload.model_dump())
    return {"ok": True}
