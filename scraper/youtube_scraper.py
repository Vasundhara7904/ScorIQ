import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse


def get_video_id(url):
    parsed = urlparse.urlparse(url)

    if "youtube" in url:
        return urlparse.parse_qs(parsed.query).get("v", [None])[0]
    elif "youtu.be" in url:
        return parsed.path[1:]

    return None


def scrape_youtube(url):
    try:
        # 🔥 Step 1: Get metadata using yt-dlp
        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get("title")
        author = info.get("uploader")
        published_date = info.get("upload_date")
        description = info.get("description")

        # 🔥 Step 2: Get transcript (MAIN CONTENT)
        video_id = get_video_id(url)

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            content = " ".join([x["text"] for x in transcript])
        except:
            content = description  # fallback if transcript not available

        return {
            "source_url": url,
            "source_type": "youtube",
            "title": title,
            "author": author,
            "published_date": published_date,
            "content": content,
            "description": description,
            "extra": {
                "views": info.get("view_count"),
                "length": info.get("duration")
            }
        }

    except Exception as e:
        print("YOUTUBE SCRAPER ERROR:", e)
        return None