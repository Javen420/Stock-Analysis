from datetime import date, datetime


def is_stale(last_updated) -> bool:
    """Return True if last_updated is from a previous calendar day (or None).

    Accepts a date, datetime, or ISO date string.
    Use this to decide whether to re-fetch stock data.
    """
    if last_updated is None:
        return True
    if isinstance(last_updated, str):
        last_date = datetime.fromisoformat(last_updated).date()
    elif isinstance(last_updated, datetime):
        last_date = last_updated.date()
    else:
        last_date = last_updated
    return last_date < date.today()
