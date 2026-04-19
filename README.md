# ScorIQ: Web Scorer & Trust Analyzer

ScorIQ is a powerful, multi-source data scraping and content trust scoring pipeline. It evaluates the credibility of web content across multiple platforms (Blogs, YouTube, and PubMed) and provides a beautifully designed dynamic web dashboard to view structured analytics and abstractive machine-generated summaries.

## 🚀 Features

- **Multi-Source Scraping**: Extract metadata and content seamlessly from YouTube videos, PubMed research articles, and general blog posts.
- **Trust Scoring Algorithm**: Calculates a sophisticated Trust Score (0-100%) based on author credibility, citation count, domain authority, recency, and the presence of medical disclaimers.
- **Abstractive AI Summarization**: Uses the highly reliable `sshleifer/distilbart-cnn-12-6` NLP model to act as a human analyst and generate concise, accurate 3-sentence summaries of the content in its own words.
- **Automated Topic Tagging**: Extracts relevant keywords from the text using `KeyBERT`.
- **Dynamic Web Dashboard**: A stunning, modern Glassmorphism UI built with Flask that allows you to paste a link and instantly view its Trust Score meter, metadata, and AI summary.

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS (Vanilla Glassmorphism UI)
- **AI / NLP**: HuggingFace Transformers (`distilbart-cnn-12-6`), `KeyBERT`, `langdetect`
- **Scraping Libraries**: `BeautifulSoup4`, `yt-dlp`, `youtube-transcript-api`, `Biopython` (Entrez)

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Vasundhara7904/ScorIQ.git
   cd ScorIQ
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The AI summarization model relies on PyTorch and Transformers. The first run will automatically download the required model weights).*

## 💻 Usage

### Web Interface (Dynamic Upload)
To start the dynamic web interface where you can analyze links in real-time:

```bash
python app.py
```
Then, open your browser and navigate to `http://localhost:5000`.

### Batch Processing
To run the scraper in batch mode and generate the static `blogs.json`, `pubmed.json`, and `youtube.json` output files:

```bash
python main.py
```

## 🧠 Trust Score Algorithm
The Trust Score evaluates the reliability of a source using a weighted heuristic function of:
- **Author Credibility**
- **Citation Count**
- **Domain Authority**
- **Recency** (How recently the content was published)
- **Medical Disclaimer Presence**
