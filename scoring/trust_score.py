import datetime
from urllib.parse import urlparse


# -------------------------------
# Helper Functions
# -------------------------------

def score_author_credibility(author):
    if not author or author == "unknown":
        return 0.3

    # Simple heuristic
    if any(word in author.lower() for word in ["university", "institute", "hospital", "clinic"]):
        return 0.9

    if len(author.split(",")) > 1:
        return 0.8  # multiple authors

    return 0.6


def score_domain_authority(url):
    domain = urlparse(url).netloc

    if any(ext in domain for ext in [".gov", ".edu"]):
        return 1.0

    if "youtube.com" in domain:
        return 0.7

    if "pubmed.ncbi.nlm.nih.gov" in domain:
        return 0.95

    return 0.5


def score_recency(published_date):
    if published_date == "unknown":
        return 0.4

    try:
        year = int(published_date[:4])
        current_year = datetime.datetime.now().year
        diff = current_year - year

        if diff <= 1:
            return 1.0
        elif diff <= 3:
            return 0.8
        elif diff <= 5:
            return 0.6
        else:
            return 0.3

    except:
        return 0.4


def score_citation_count(extra_data):
    # Only meaningful for PubMed
    citation = extra_data.get("citation_count", 0)

    if citation >= 100:
        return 1.0
    elif citation >= 50:
        return 0.8
    elif citation >= 10:
        return 0.6
    elif citation > 0:
        return 0.5
    else:
        return 0.4


def score_medical_disclaimer(text):
    if not text:
        return 0.4

    disclaimer_keywords = [
        "consult a doctor",
        "medical advice",
        "for informational purposes",
        "not a substitute",
    ]

    text_lower = text.lower()

    if any(keyword in text_lower for keyword in disclaimer_keywords):
        return 1.0

    return 0.5


# -------------------------------
# MAIN TRUST SCORE FUNCTION
# -------------------------------

def calculate_trust_score(processed_data):

    author_score = score_author_credibility(processed_data.get("author"))

    domain_score = score_domain_authority(processed_data.get("source_url"))

    recency_score = score_recency(processed_data.get("published_date"))

    citation_score = score_citation_count(processed_data.get("extra", {}))

    # Combine title + description + content chunks
    text_for_disclaimer = (
        (processed_data.get("title") or "") + " " +
        (processed_data.get("description") or "") + " " +
        " ".join(processed_data.get("content_chunks", []))
    )

    disclaimer_score = score_medical_disclaimer(text_for_disclaimer)

    # -------------------------------
    # Final Weighted Score
    # -------------------------------
    final_score = (
        0.25 * author_score +
        0.20 * citation_score +
        0.20 * domain_score +
        0.20 * recency_score +
        0.15 * disclaimer_score
    )

    return round(min(max(final_score, 0), 1), 2)