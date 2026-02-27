from sqlalchemy.orm import Session
from app.models.models import AuditLog


def write_audit(db: Session, entity_type: str, entity_id: str, action: str, actor_user_id=None, actor_employee_id=None, before=None, after=None, override_reason=None, ip=None):
    log = AuditLog(
        entity_type=entity_type,
        entity_id=str(entity_id),
        action=action,
        actor_user_id=actor_user_id,
        actor_employee_id=actor_employee_id,
        before_json=before,
        after_json=after,
        override_reason=override_reason,
        ip=ip,
    )
    db.add(log)
    db.commit()
