import json
from scraper.blog_scraper import scrape_blog
from scraper.youtube_scraper import scrape_youtube
from scraper.pubmed_scraper import scrape_pubmed

from processing.processor import process_content
from scoring.trust_score import calculate_trust_score


def process_url(url, source_type):

    if source_type == "blog":
        raw_data = scrape_blog(url)

    elif source_type == "youtube":
        raw_data = scrape_youtube(url)

    elif source_type == "pubmed":
        raw_data = scrape_pubmed(url)

    else:
        return None

    if not raw_data:
        return None
    print("RAW DATA:", raw_data)
    processed_data = process_content(raw_data)
    if processed_data is None:
        return {
             "error": "Processing failed",
            "debug_raw": raw_data  # 👈 helps debugging
        }
    print("PROCESSED DATA:", processed_data)
    trust_score = calculate_trust_score(processed_data)

    return {
        "source_url": processed_data["source_url"],
        "source_type": processed_data["source_type"],
        "author": processed_data["author"],
        "published_date": processed_data["published_date"],
        "language": processed_data["language"],
        "region": processed_data["region"],
        "topic_tags": processed_data["topic_tags"],
        "trust_score": trust_score,
        "summary": processed_data["summary"],
        "content_chunks": processed_data["content_chunks"]
    }


# -----------------------------------
# ASSIGNMENT MODE
# -----------------------------------
if __name__ == "__main__":

    # 🔴 REQUIRED: 3 blogs, 2 YouTube, 1 PubMed
    blog_urls = [
    "https://thesnowmeltssomewhere.wordpress.com/2026/03/29/the-philosophy-of-a-hobby/?_gl=1*bdnkx9*_gcl_au*MTQ0MzE3MjAxMi4xNzc2NDYyMTc2LjE3MTgxNjQ5ODAuMTc3NjQ2MjI0Ni4xNzc2NDYzMzEy",
    "https://neptunesky.com/2026/03/21/beach-peace/",
    "https://wattsupwiththat.com/2026/04/13/bixonimania-how-ai-turned-a-joke-diagnosis-into-peer-reviewed-medicine/"
    ]
    

    youtube_urls = [
        "https://youtu.be/gRANhPtpuKc?si=j4o7_yjH6EjuRy_m",
        "https://youtu.be/7I3G21RyARs?si=9rvmSB73B6Rwam-Z"
    ]

    pubmed_urls = [
        "https://pubmed.ncbi.nlm.nih.gov/38041827/"
    ]

    blog_results = []
    youtube_results = []
    pubmed_results = []

    # ---------------- BLOGS ----------------
    for url in blog_urls:
        print(f"🔍 Processing blog: {url}")
        result = process_url(url, "blog")
        if result:
            blog_results.append(result)

    # ---------------- YOUTUBE ----------------
    for url in youtube_urls:
        print(f"🔍 Processing YouTube: {url}")
        result = process_url(url, "youtube")
        if result:
            youtube_results.append(result)

    # ---------------- PUBMED ----------------
    for url in pubmed_urls:
        print(f"🔍 Processing PubMed: {url}")
        result = process_url(url, "pubmed")
        if result:
            pubmed_results.append(result)

    # ---------------- SAVE FILES ----------------
    with open("output/blogs.json", "w") as f:
        json.dump(blog_results, f, indent=4)

    with open("output/youtube.json", "w") as f:
        json.dump(youtube_results, f, indent=4)

    with open("output/pubmed.json", "w") as f:
        json.dump(pubmed_results, f, indent=4)

    print("\n✅ Assignment JSON files generated successfully!")