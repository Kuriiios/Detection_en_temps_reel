from datetime import datetime, timezone
from api_intermediaire.modules.db_tools import get_db_session

def validate_token(token):
    with get_db_session() as session:
        record = session.get_token(token)

        if not record:
            return None

        if record.expires_at < datetime.now(timezone.utc):
            session.delete_token(token)
            return None

        return record.user_id