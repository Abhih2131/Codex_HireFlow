from sqlalchemy import text
from app.db.session import SessionLocal


def run():
    db = SessionLocal()
    db.execute(text("insert into employees(employee_id,name,email,is_active,raw_json) values('E0001','Super Admin','admin@workplaceai.local',true,'{}') on conflict (employee_id) do nothing"))
    db.execute(text("insert into app_users(employee_id,email,role,is_active) values('E0001','admin@workplaceai.local','Super Admin',true) on conflict do nothing"))
    db.execute(text("insert into configs(key,json_value) values('default_stages', :v) on conflict (key) do update set json_value=excluded.json_value"), {"v": '{"requisition":["Draft","Submitted","Approval Pending","Returned","Approved","Assigned","Closed"],"application":["New","PreScreenPending","Screening","HMReview","InterviewR1","InterviewR2","HRInterview","Selected","PreOfferDocsPending","DocsVerified","OfferDraft","OfferApprovalPending","OfferSent","OfferAccepted","OfferRejected","OfferExpired"]}'})
    db.commit()
    db.close()


if __name__ == "__main__":
    run()
