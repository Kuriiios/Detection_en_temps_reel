from datetime import datetime
from database.data.models import User, Token
from api_intermediaire.modules.db_tools import get_db_session
from api_intermediaire.modules.exceptions import Unauthorized

def auth_middleware(request):
    with get_db_session() as session:
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise Unauthorized("Missing token")

        token = auth_header.split(" ", 1)[1]

        token_record = session.query(Token).filter_by(token = token).first()

        if not token_record:
            raise Unauthorized("Invalid token")

        if token_record.expires_at < datetime.now():
            raise Unauthorized("Token expired")

        request.user = session.query(User).filter_by(token = token_record).first()