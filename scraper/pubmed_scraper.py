from Bio import Entrez
from xml.etree import ElementTree as ET

Entrez.email = "vasu.yande@gmail.com"  # REQUIRED


def extract_pubmed_id(url):
    return url.rstrip("/").split("/")[-1]


def scrape_pubmed(url):
    try:
        pubmed_id = extract_pubmed_id(url)

        handle = Entrez.efetch(db="pubmed", id=pubmed_id, rettype="xml")
        records = handle.read()

        root = ET.fromstring(records)

        article = root.find(".//PubmedArticle")

        # Title
        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "unknown"

        # Abstract
        abstract_elem = article.find(".//AbstractText")
        description = abstract_elem.text if abstract_elem is not None else "unknown"

        content = description  # PubMed content = abstract

        # Authors
        authors_list = article.findall(".//Author")
        authors = []
        for a in authors_list:
            lastname = a.find("LastName")
            firstname = a.find("ForeName")
            if lastname is not None and firstname is not None:
                authors.append(f"{firstname.text} {lastname.text}")

        author = ", ".join(authors) if authors else "unknown"

        # Journal
        journal_elem = article.find(".//Title")
        journal = journal_elem.text if journal_elem is not None else "unknown"

        # Year
        year_elem = article.find(".//PubDate/Year")
        published_date = year_elem.text if year_elem is not None else "unknown"

        return {
            "source_url": url,
            "source_type": "pubmed",
            "author": author,
            "published_date": published_date,
            "title": title,
            "description": description,
            "content": content,
            "extra": {
                "journal": journal,
                "citation_count": 1  # placeholder (can improve later)
            }
        }

    except Exception as e:
        print(f"❌ PubMed scraping failed for {url}: {e}")
        return None