from datetime import datetime, timezone

from flask_login import current_user

from app import app, db
from app.routes import authentication  # noqa: F401 # This is added to resolve unused import warning
from app.routes import web  # noqa: F401 # This is added to resolve unused import warning


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
