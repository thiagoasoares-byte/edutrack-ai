Overdue Service

This is a small Flask wrapper that exposes an endpoint to return distinct overdue `subject_id`s for a given `user_id`.

Environment variables:
- `DB_URL` - the SQLAlchemy connection URL for your database (required)
- `PORT` - optional, default 8080

Install dependencies (you can add them to your workspace `requirements.txt` or install from the helper file `requirements.overdue.txt`):

pip install -r requirements.overdue.txt

Or add to your main `requirements.txt`:

flask
sqlalchemy
psycopg2-binary

Run locally:

export DB_URL="postgresql://user:pass@host:5432/dbname"
python script/overdue_service.py

Endpoint:
GET /overdue_subjects?user_id=<id>
Response JSON: { "subject_ids": [1,2,3] }

Security: Protect this service (network restriction or token) before calling it from Xano in production.
