from datetime import datetime, timezone
from api_intermediaire.modules.db_tools import get_db_session
from database.data.models import Token

def validate_token(token):
    with get_db_session() as session:
        record = session.query(Token).filter_by(token = token).first()
        if not record:
            return None

        if record.expires_at < datetime.now():
            session.delete_token(token)
            return None

        return record.user_id