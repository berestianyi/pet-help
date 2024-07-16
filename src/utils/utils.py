import re
from unidecode import unidecode


def text_to_slug(text: str) -> str:
    text = unidecode(text)

    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\W+', '-', text)

    text = text.strip('-')

    text = text.lower()
    text = text[:80]

    return text
