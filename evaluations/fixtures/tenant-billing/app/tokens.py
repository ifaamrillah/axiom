"""Session and password-reset tokens."""

import random
import secrets
import string


def new_session_id():
    return secrets.token_urlsafe(32)


def new_reset_token():
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(24))
