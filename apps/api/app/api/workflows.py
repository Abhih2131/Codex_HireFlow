from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.api.deps import require_roles
from app.models.models import GenericJsonTable
from app.services.audit import write_audit

router = APIRouter(tags=["workflow"])

class ReqIn(BaseModel):
    title: str
    bu: str | None = None
    location: str | None = None
    band: str | None = None
    headcount: int = 1
    hm_employee_id: str

@router.get("/requisitions")
def req_list(db: Session = Depends(get_db), user=Depends(require_roles("Super Admin","HR Admin","Recruiter","Hiring Manager"))):
    rows = db.execute(text("select id,title,status,hm_employee_id,recruiter_employee_id,created_at from requisitions order by id desc limit 200")).mappings().all()
    return [dict(r) for r in rows]

@router.post("/requisitions")
def req_create(payload: ReqIn, db: Session = Depends(get_db), user=Depends(require_roles("Super Admin","HR Admin","Recruiter","Hiring Manager"))):
    rec = db.execute(text("""
        insert into requisitions(status,hm_employee_id,title,bu,location,band,headcount,created_by,created_at,updated_at)
        values('Draft',:hm,:title,:bu,:loc,:band,:hc,:cb,now(),now()) returning id
    """), {"hm":payload.hm_employee_id,"title":payload.title,"bu":payload.bu,"loc":payload.location,"band":payload.band,"hc":payload.headcount,"cb":user.id}).scalar_one()
    db.execute(text("insert into requisition_versions(requisition_id,version_no,data_json,created_by,created_at,change_reason) values(:id,1,:d,:cb,now(),'Initial Draft')"), {"id":rec,"d":payload.model_dump_json(),"cb":user.id})
    db.commit()
    write_audit(db, "requisition", str(rec), "create", user.id, user.employee_id, after=payload.model_dump())
    return {"id": rec}

class StageMove(BaseModel):
    application_id: int
    to_stage: str
    notes: str | None = None

@router.post("/applications/move-stage")
def move_stage(payload: StageMove, db: Session = Depends(get_db), user=Depends(require_roles("Super Admin","HR Admin","Recruiter"))):
    app = db.execute(text("select stage,current_ctc,expected_ctc,notice_days,location_pref,availability_date from applications where id=:id"), {"id": payload.application_id}).mappings().first()
    if not app: raise HTTPException(404, "application not found")
    mandatory = ["current_ctc","expected_ctc","notice_days","location_pref","availability_date"]
    if payload.to_stage not in ["New","PreScreenPending"]:
        for m in mandatory:
            if app[m] is None:
                raise HTTPException(400, f"Missing mandatory field: {m}")
    db.execute(text("update applications set stage=:to,updated_at=now() where id=:id"), {"to": payload.to_stage, "id": payload.application_id})
    db.execute(text("insert into application_stage_history(application_id,from_stage,to_stage,moved_by,moved_at,notes) values(:id,:f,:t,:mb,now(),:n)"), {"id": payload.application_id, "f": app["stage"], "t": payload.to_stage, "mb": user.id, "n": payload.notes})
    db.commit()
    write_audit(db, "application", str(payload.application_id), "move_stage", user.id, user.employee_id, before={"stage": app["stage"]}, after={"stage": payload.to_stage})
    return {"ok": True}

@router.get("/audit")
def audit(db: Session = Depends(get_db), user=Depends(require_roles("Super Admin","HR Admin"))):
    rows = db.execute(text("select * from audit_logs order by id desc limit 200")).mappings().all()
    return [dict(r) for r in rows]

@router.get("/communications/log")
def comms(db: Session = Depends(get_db), user=Depends(require_roles("Super Admin","HR Admin","Recruiter"))):
    rows = db.execute(text("select * from communications_events order by id desc limit 200")).mappings().all()
    return [dict(r) for r in rows]
