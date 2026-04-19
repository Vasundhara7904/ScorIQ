from langdetect import detect
from keybert import KeyBERT
from transformers import pipeline

model="Falconsai/text_summarization"

kw_model = KeyBERT(model="all-MiniLM-L6-v2")


def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def generate_topic_tags(text):
    try:
        keywords = kw_model.extract_keywords(text, top_n=5)
        return [kw[0] for kw in keywords]
    except:
        return []


def chunk_content(text, max_words=200):
    try:
        words = text.split()
        return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    except:
        return []


# 🌍 REGION DETECTION
def detect_region(text, url):
    text = text.lower()

    if any(w in text for w in ["india", "mumbai", "delhi"]):
        return "India"
    if any(w in text for w in ["usa", "america", "california"]):
        return "USA"
    if any(w in text for w in ["uk", "london", "britain"]):
        return "UK"

    if ".in" in url:
        return "India"
    elif ".uk" in url:
        return "UK"

    return "Global"


# 🧠 SUMMARY
def generate_summary(text):
    try:
        if len(text.split()) < 30:
            return "Content too short to summarize"

        # Use a more capable instruction-tuned transformer for human-like summaries
        summarizer = pipeline(
            "text2text-generation",
            model="google/flan-t5-base"
        )

        truncated_text = " ".join(text.split()[:400])
        prompt = f"Read the following text. Write a 3 to 4 sentence summary of the text. Write it in the first person, as if you are a real person who just read the article and are summarizing it for a friend.\n\nText: {truncated_text}\n\nSummary:"

        summary = summarizer(prompt, max_length=150, min_length=40, do_sample=True, temperature=0.7)

        return summary[0]['generated_text']

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
        region = detect_region(full_text, raw_data.get("source_url", ""))

        summary = generate_summary(text)

        # ✅ FINAL RETURN (THIS WAS MISSING EARLIER)
        return {
            "source_url": raw_data.get("source_url"),
            "source_type": raw_data.get("source_type"),
            "author": raw_data.get("author") or "unknown",
            "published_date": raw_data.get("published_date") or "unknown",
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