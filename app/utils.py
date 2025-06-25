from datetime import datetime
import re

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip()) if text else ""

def parse_date(date_str):
    # Try multiple date formats
    for fmt in ("%B %d, %Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except Exception:
            continue
    return None
