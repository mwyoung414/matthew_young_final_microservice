from typing import Dict, Optional
import time
import jwt

class JWTService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.token_expire_time = 3600  # 1 hour
        self.refresh_token_expire_time = 86400  # 24 hours

    def create_token(self, user_id: int, username: str, role: str) -> Dict[str, str]:
        payload = {
            "user_id": user_id,
            "username": username,
            "role": role,
            "exp": int(time.time()) + self.token_expire_time,
            "iat": int(time.time())
        }

        refresh_payload = {
            "user_id": user_id,
            "role": role,
            "username": username,
            "exp": int(time.time()) + self.refresh_token_expire_time,
            "iat": int(time.time())
        }

        access_token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm="HS256")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": self.token_expire_time
        }
        
    def verify_token(self, token: str) -> Optional[Dict[str, str]]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
    def refresh_token(self, token: str) -> Optional[Dict[str, str]]:
        payload = self.verify_token(token)
        if payload is None:
            return None
        user_id = payload["user_id"]

        return self.create_token(user_id, payload["username"], payload["role"])