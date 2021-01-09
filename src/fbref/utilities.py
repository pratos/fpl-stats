from pipetools import pipe


def format_age(age: str) -> str:
    try:
        spl = age.split("-")
        return f"{spl[0]} years and {spl[1]} days"
    except Exception:
        return "Age not known"


def to_float(text: str) -> float:
    if not text:
        return 0.0
    else:
        return text > pipe | str | float


def get_proxy_format(proxy_element: str):
    return f"http://{proxy_element['proxy_address']}:{proxy_element['ports']['http']}:{proxy_element['username']}:{proxy_element['password']}"
