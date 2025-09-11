import re

_ws_re = re.compile(r"\s+")
_multi_dash_re = re.compile(r"-{2,}")

def norm_spec_name(src: str) -> str:
    """
    Нормализуем строку специальности для сравнения/поиска:
    - трим
    - схлопываем пробелы
    - заменяем повторные дефисы на один
    - приводим к нижнему регистру
    """
    if not src:
        return ""
    s = src.strip()
    s = _multi_dash_re.sub("-", s)
    s = _ws_re.sub(" ", s)
    return s.lower()
