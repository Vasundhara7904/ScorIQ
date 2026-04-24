from keybert import KeyBERT

print("Loading KeyBERT tagging model globally...")
kw_model = KeyBERT(model="all-MiniLM-L6-v2")
print("Tagging model loaded.")

def generate_topic_tags(text):
    try:
        keywords = kw_model.extract_keywords(text, top_n=5)
        return [kw[0] for kw in keywords]
    except:
        return []
