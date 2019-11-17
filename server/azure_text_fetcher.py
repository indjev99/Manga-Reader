# azure_text_fetcher.py

from azure_english_text_fetcher import analyze_english_text
from azure_japanese_text_fetcher import analyze_japanese_text

def analyze_text(image_url, in_lang):
    if in_lang == 'ja': return analyze_japanese_text(image_url)
    else: return analyze_english_text(image_url)

