import time


def timestamp_is_expired(expiry_date: int | None) -> bool:
    if expiry_date is None:
        return False

    return expiry_date < time.time()