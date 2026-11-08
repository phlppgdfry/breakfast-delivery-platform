"""Input contracts shared by the domain use cases."""


def number(payload, key, minimum, maximum, integer=False):
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key}: enter a finite number")
    if not minimum <= value <= maximum or (integer and int(value) != value):
        raise ValueError(
            f"{key}: expected {'integer ' if integer else ''}{minimum}–{maximum}"
        )
    return int(value) if integer else float(value)


def text(payload, key, maximum=120):
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"{key}: enter 1–{maximum} characters")
    return value.strip()


def record(records, payload):
    return next(r.copy() for r in records if r["id"] == payload.get("id"))


def metric(label, value, note):
    return {"label": label, "value": value, "note": note}
