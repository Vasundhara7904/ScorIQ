from langdetect import detect
from datetime import datetime
from transformers import pipeline

from processing.tagging import generate_topic_tags
from processing.chunking import chunk_content



def detect_language(text):
    text_lower = text.lower()
    hinglish_words = [" hai ", " ki ", " mein ", " aur ", " kya ", " aa jaao", " bhai ", " hindi", " yaar "]
    if any(w in text_lower for w in hinglish_words):
        return "hi"
    try:
        return detect(text)
    except:
        return "unknown"


# 🌍 REGION DETECTION
def detect_region(text, url, language):
    text = text.lower()

    india_kws = ["india", "mumbai", "delhi", "bengaluru", "chennai", "pune", "inr"]
    usa_kws = ["usa", "america", "california", "new york", "washington"]
    uk_kws = ["uk", "london", "britain", "england"]

    if any(w in text for w in india_kws) or ".in" in url or language == "hi":
        return "India"
    if any(w in text for w in usa_kws):
        return "USA"
    if any(w in text for w in uk_kws) or ".uk" in url:
        return "UK"

    return "Global"

# 📅 DATE FORMATTING
def format_date(date_str):
    if not date_str or date_str == "unknown":
        return "Unknown"
        
    if len(date_str) == 8 and date_str.isdigit():
        try:
            return datetime.strptime(date_str, "%Y%m%d").strftime("%B %d, %Y")
        except:
            pass
            
    try:
        if len(date_str) >= 10 and date_str[4] == '-' and date_str[7] == '-':
            return datetime.strptime(date_str[:10], "%Y-%m-%d").strftime("%B %d, %Y")
    except:
        pass
        
    return date_str


# 🧠 SUMMARY
def generate_summary(raw_data, topic_tags):
    try:
        text = raw_data.get("content", "")
        if len(text.split()) < 30:
            text = raw_data.get("description", "")
            if not text:
                return "This site doesn't have enough content to summarize."

        # Reverting to the highly reliable abstractive model (distilbart)
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        
        # Max length 120, min 40 ensures roughly 3-4 good sentences
        raw_summary = summarizer(text[:1024], max_length=120, min_length=40, do_sample=False)
        summary_text = raw_summary[0]['summary_text'].strip()

        # Construct the requested conversational introduction
        title = raw_data.get("title") or ""
        tags_str = ", ".join(topic_tags[:3]) if topic_tags else "several topics"
        
        if title:
            intro = f"This site tells you about '{title}' and explores concepts like {tags_str}. "
        else:
            intro = f"This site tells you about {tags_str}. "

        # Combine into a seamless human-like summary
        final_summary = intro + "Specifically, " + summary_text

        return final_summary

    except Exception as e:
        print("SUMMARY ERROR:", e)
        return "Summary not available"

    print("Loading summarizer model...")
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    print("Summarizer loaded successfully")


# 🚀 MAIN PROCESSOR (FIXED)
def process_content(raw_data):
    try:
        if raw_data is None:
            return None

        text = raw_data.get("content", "")

        # fallback if content empty
        if not text or len(text.strip()) == 0:
            text = raw_data.get("description", "") or "No content available"

        # processing
        language = detect_language(text)
        topic_tags = generate_topic_tags(text)
        content_chunks = chunk_content(text)

        full_text = text + " " + (raw_data.get("description") or "")
        region = detect_region(full_text, raw_data.get("source_url", ""), language)

        summary = generate_summary(raw_data, topic_tags)

        # ✅ FINAL RETURN (THIS WAS MISSING EARLIER)
        return {
            "source_url": raw_data.get("source_url"),
            "source_type": raw_data.get("source_type"),
            "author": raw_data.get("author") or "unknown",
            "published_date": format_date(raw_data.get("published_date") or "unknown"),
            "language": language,
            "region": region,
            "topic_tags": topic_tags,
            "content_chunks": content_chunks,
            "summary": summary,
            "title": raw_data.get("title"),
            "description": raw_data.get("description"),
            "extra": raw_data.get("extra", {})
        }

    except Exception as e:
        print("PROCESS ERROR:", e)
        return None