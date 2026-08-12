import json
from pathlib import Path

from db.db import Users
from logs.record_log import log_info, log_error

db = Users()
_MESSAGES_PATH = Path(__file__).resolve().parent.parent / "messages.json"


def translate(user_id, key):
    try:
        log_info("translate we are looking for a translation into the desired language")

        with open(_MESSAGES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        language_code = db.get_language(user_id) or "en-US"
        full_key = f"{key}{language_code}"

        if full_key not in data:
            # fallback to English if key missing for current language
            full_key = f"{key}en-US"

        return data.get(full_key, f"[{key}]")

    except Exception as e:
        log_error(f"error translation.py: {e}")
        return f"[{key}]"
