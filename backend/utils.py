import re

def clean_text(text):
    """
    Cleans the input text by:
    - Lowercasing
    - Removing URLs, mentions, hashtags, punctuation
    - Normalizing whitespace
    """
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

