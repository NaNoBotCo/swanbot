import re

def extract_tickers(text: str) -> list:
    """
    Extract all $TICKER strings from user input.
    """
    matches = re.findall(r"\$[A-Z]{1,5}", text.upper())
    return [m[1:] for m in matches]
