from flask import Flask, render_template, request
import traceback
import logging
from main import process_url

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def detect_source_type(url):
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "pubmed.ncbi.nlm.nih.gov" in url_lower:
        return "pubmed"
    else:
        return "blog"

# ----------------------------
# GLOBAL ERROR HANDLER
# ----------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    print("\n🔥 GLOBAL ERROR CAUGHT:")
    print(traceback.format_exc())

    return render_template(
        "index.html",
        result={
            "error": True,
            "title": "Error",
            "author": "-",
            "published_date": "-",
            "region": "-",
            "language": "-",
            "trust_score": 0,
            "summary": str(e),
            "topic_tags": [],
            "content_chunks": []
        }
    )


# ----------------------------
# MAIN ROUTE
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            source_type = detect_source_type(url)
            print(f"🔗 Processing URL: {url} as {source_type}")
            try:
                result = process_url(url, source_type)
            except Exception as e:
                print(f"🔥 Error processing {url}: {e}")
                result = {
                    "error": True,
                    "title": "Error",
                    "author": "-",
                    "published_date": "-",
                    "region": "-",
                    "language": "-",
                    "trust_score": 0,
                    "summary": f"Failed to process: {str(e)}",
                    "topic_tags": [],
                    "content_chunks": []
                }
    
    return render_template("index.html", result=result)


# ----------------------------
# RUN SERVER
# ----------------------------
if __name__ == "__main__":
    print("🔥 Flask server starting...")
    app.run(debug=True, port=5000)