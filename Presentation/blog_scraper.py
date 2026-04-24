import requests
from bs4 import BeautifulSoup


def scrape_blog(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # -------------------------------
        # TITLE
        # -------------------------------
        title_tag = soup.find("meta", property="og:title")
        title = title_tag["content"] if title_tag else "unknown"

        # -------------------------------
        # DESCRIPTION
        # -------------------------------
        desc_tag = soup.find("meta", property="og:description")
        description = desc_tag["content"] if desc_tag else "unknown"

        # -------------------------------
        # AUTHOR (multiple fallbacks)
        # -------------------------------
        author = None

        # Method 1: rel="author"
        author_tag = soup.find("a", rel="author")
        if author_tag:
            author = author_tag.text.strip()

        # Method 2: meta tag
        if not author:
            meta_author = soup.find("meta", {"name": "author"})
            if meta_author:
                author = meta_author.get("content")

        author = author if author else "unknown"

        # -------------------------------
        # PUBLISHED DATE
        # -------------------------------
        published_date = None

        time_tag = soup.find("time")
        if time_tag and time_tag.get("datetime"):
            published_date = time_tag.get("datetime")

        # fallback meta
        if not published_date:
            meta_date = soup.find("meta", property="article:published_time")
            if meta_date:
                published_date = meta_date.get("content")

        published_date = published_date if published_date else "unknown"

        # -------------------------------
        # CONTENT EXTRACTION
        # -------------------------------
        paragraphs = soup.find_all("p")

        content_list = []
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 50:  # filter noise
                content_list.append(text)

        content = "\n\n".join(content_list)

        # -------------------------------
        # RETURN STRUCTURED DATA
        # -------------------------------
        return {
            "source_url": url,
            "source_type": "blog",
            "author": author,
            "published_date": published_date,
            "title": title,
            "description": description,
            "content": content,
            "extra": {}
        }

    except Exception as e:
        print(f"❌ WordPress scraping failed for {url}: {e}")
        return None