import os
import yaml
from functools import lru_cache


@lru_cache(64)
def t(phrase: str, locale: str) -> str:
    if locale not in ["ru", "uk", "en"]:
        locale = "en"

    path = os.path.join("locales", f"{locale}.yaml")
    with open(path, encoding="utf-8") as file:
        phrases = yaml.safe_load(file)

    return phrases.get(phrase, phrase)
