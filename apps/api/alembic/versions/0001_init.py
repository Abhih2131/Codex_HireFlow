"""init

Revision ID: 0001
Revises: 
Create Date: 2026-02-27
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('employees',
        sa.Column('employee_id', sa.String(), primary_key=True),
        sa.Column('name', sa.String()), sa.Column('email', sa.String()), sa.Column('bu', sa.String()), sa.Column('function', sa.String()),
        sa.Column('dept', sa.String()), sa.Column('location', sa.String()), sa.Column('band', sa.String()), sa.Column('manager_employee_id', sa.String()),
        sa.Column('is_active', sa.Boolean(), server_default='true'), sa.Column('raw_json', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')))
    op.create_table('app_users', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('employee_id', sa.String(), sa.ForeignKey('employees.employee_id')),
        sa.Column('email', sa.String()), sa.Column('phone', sa.String()), sa.Column('role', sa.String()), sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')))
    op.create_table('auth_otps', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('identifier', sa.String()), sa.Column('code_hash', sa.String()),
        sa.Column('expires_at', sa.DateTime()), sa.Column('attempts', sa.Integer(), server_default='0'), sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')))
    op.create_table('audit_logs', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('entity_type', sa.String()), sa.Column('entity_id', sa.String()), sa.Column('action', sa.String()),
        sa.Column('actor_user_id', sa.Integer()), sa.Column('actor_employee_id', sa.String()), sa.Column('before_json', postgresql.JSONB()), sa.Column('after_json', postgresql.JSONB()),
        sa.Column('override_reason', sa.Text()), sa.Column('ip', sa.String()), sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')))

    # business tables
    op.execute("create table requisitions (id serial primary key, current_version_id int, status varchar, hm_employee_id varchar, recruiter_employee_id varchar, title varchar, bu varchar, location varchar, band varchar, headcount int default 1, created_by int, created_at timestamp default now(), updated_at timestamp default now())")
    op.execute("create table requisition_versions (id serial primary key, requisition_id int references requisitions(id), version_no int, data_json jsonb, created_by int, created_at timestamp default now(), change_reason text)")
    op.execute("create table approval_flows (id serial primary key, entity_type varchar, entity_id int, mode varchar default 'seq', sla_hours int default 48, created_at timestamp default now())")
    op.execute("create table approvals (id serial primary key, flow_id int references approval_flows(id), step_no int, approver_employee_id varchar, status varchar default 'pending', acted_at timestamp, comments text)")
    op.execute("create table candidates (id serial primary key, full_name varchar, email varchar, phone varchar, resume_file_id varchar, parsed_json jsonb, created_at timestamp default now())")
    op.execute("create table applications (id serial primary key, requisition_id int references requisitions(id), candidate_id int references candidates(id), stage varchar, status varchar, current_ctc numeric, expected_ctc numeric, notice_days int, location_pref varchar, availability_date date, created_at timestamp default now(), updated_at timestamp default now())")
    op.execute("create table application_stage_history (id serial primary key, application_id int references applications(id), from_stage varchar, to_stage varchar, moved_by int, moved_at timestamp default now(), notes text)")
    op.execute("create table interviews (id serial primary key, application_id int references applications(id), round_name varchar, scheduled_at timestamp, panel_employee_ids jsonb, status varchar, created_at timestamp default now())")
    op.execute("create table interview_scorecards (id serial primary key, interview_id int references interviews(id), reviewer_employee_id varchar, ratings_json jsonb, recommendation varchar, submitted_at timestamp)")
    op.execute("create table document_checklists (id serial primary key, requisition_id int references requisitions(id), checklist_json jsonb)")
    op.execute("create table candidate_documents (id serial primary key, application_id int references applications(id), doc_type varchar, file_id varchar, status varchar, verified_by varchar, verified_at timestamp, comments text)")
    op.execute("create table offers (id serial primary key, application_id int references applications(id), status varchar, validity_days int default 7, current_version_id int, created_at timestamp default now(), updated_at timestamp default now())")
    op.execute("create table offer_versions (id serial primary key, offer_id int references offers(id), version_no int, ctc_json jsonb, template_id varchar, pdf_file_id varchar, created_by int, created_at timestamp default now(), override_justification text)")
    op.execute("create table communications_events (id serial primary key, channel varchar, \"to\" varchar, subject varchar, body text, status varchar, related_entity_type varchar, related_entity_id varchar, created_at timestamp default now())")
    op.execute("create table configs (key varchar primary key, json_value jsonb, updated_at timestamp default now())")
    op.create_table('generic_json_records', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('kind', sa.String()), sa.Column('ref_id', sa.String()), sa.Column('payload', postgresql.JSONB(), server_default='{}'), sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')), sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')))


def downgrade() -> None:
    for t in ['generic_json_records','configs','communications_events','offer_versions','offers','candidate_documents','document_checklists','interview_scorecards','interviews','application_stage_history','applications','candidates','approvals','approval_flows','requisition_versions','requisitions','audit_logs','auth_otps','app_users','employees']:
        op.execute(f'drop table if exists {t} cascade')
