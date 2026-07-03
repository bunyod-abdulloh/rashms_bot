# bot/utils/tg_token.py
import hmac
import hashlib
import time
from data.config import BOT_TOKEN

def generate_tg_token(user_id: int) -> str:
    timestamp = int(time.time())
    message = f"{user_id}:{timestamp}"
    sig = hmac.new(
        BOT_TOKEN.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{user_id}:{timestamp}:{sig}"
