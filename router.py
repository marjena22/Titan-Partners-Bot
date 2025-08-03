# routes the answers to a manager

DEFAULT_MANAGER = ("marjena", 425186135)   # (username, chat_id)
STREAMER_MANAGER  = ("marjena", 425186135)
WEBMASTER_MANAGER = ("marjena", 425186135)

def pick_manager(payload: dict):
    role = payload.get("role")
    if role == "streamer":
        return STREAMER_MANAGER
    if role == "webmaster":
        return WEBMASTER_MANAGER
    return DEFAULT_MANAGER