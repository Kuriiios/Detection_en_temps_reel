from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api_intermediaire.modules.db_tools import get_db_session
from api_intermediaire.modules.exceptions import Unauthorized
from api_intermediaire.middleware.tokens import validate_token
from database.data.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = validate_token(token)
    if not user_id:
        raise Unauthorized("Invalid or expired token")

    with get_db_session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise Unauthorized("User not found")
        # Extract needed fields
        user_data = {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
            "city": user.city.name,
        }
        return user_data