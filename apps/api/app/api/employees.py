import json
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.db.session import get_db
from app.models.models import Employee
from app.api.deps import require_roles
from app.services.audit import write_audit

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("")
def list_employees(q: str = "", db: Session = Depends(get_db), user=Depends(require_roles("Super Admin", "HR Admin", "Recruiter", "Hiring Manager"))):
    query = db.query(Employee)
    if q:
        query = query.filter(Employee.name.ilike(f"%{q}%"))
    rows = query.limit(200).all()
    return [{"employee_id": r.employee_id, "name": r.name, "email": r.email, "bu": r.bu, "location": r.location, "band": r.band} for r in rows]


def _load_employee_sheet(file: UploadFile) -> pd.DataFrame:
    name = (file.filename or "").lower()
    if name.endswith(".csv"):
        return pd.read_csv(file.file)
    try:
        return pd.read_excel(file.file, sheet_name="Master")
    except Exception as exc:
        raise HTTPException(400, f"Invalid file. Upload .xlsx (Master sheet) or .csv. Details: {exc}")


@router.post("/import")
def import_employees(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(require_roles("Super Admin", "HR Admin"))):
    df = _load_employee_sheet(file)
    if "employee_id" not in df.columns:
        raise HTTPException(400, "employee_id missing")
    errs, seen, inserted, updated = [], set(), 0, 0
    for idx, row in df.iterrows():
        eid = str(row.get("employee_id", "")).strip()
        if not eid or eid == "nan":
            errs.append(f"row {idx+2}: employee_id blank")
            continue
        if eid in seen:
            errs.append(f"row {idx+2}: duplicate employee_id {eid}")
            continue
        seen.add(eid)
    if errs:
        raise HTTPException(400, {"errors": errs})

    for _, row in df.iterrows():
        data = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}
        eid = str(data.get("employee_id"))
        rec = db.query(Employee).filter(Employee.employee_id == eid).first()
        mapped = {
            "name": data.get("name"), "email": data.get("email"), "bu": data.get("bu"),
            "function": data.get("function"), "dept": data.get("dept"), "location": data.get("location"),
            "band": data.get("band"), "manager_employee_id": data.get("manager_employee_id"),
            "is_active": bool(data.get("is_active", True)), "raw_json": json.loads(json.dumps(data, default=str))
        }
        if rec:
            for k, v in mapped.items():
                setattr(rec, k, v)
            updated += 1
        else:
            db.add(Employee(employee_id=eid, **mapped))
            inserted += 1
    db.commit()
    write_audit(db, "employees", "bulk", "import", actor_user_id=user.id, actor_employee_id=user.employee_id)
    return {"inserted": inserted, "updated": updated, "skipped": 0, "errors": []}
