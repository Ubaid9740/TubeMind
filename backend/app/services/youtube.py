import os
import glob
import re
from dotenv import load_dotenv
from googleapiclient.discovery import build
import yt_dlp

# Load Environment Variables
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Connect to YouTube
youtube_client = build("youtube", "v3", developerKey=API_KEY)

def get_video_id(url: str):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url:
        return url.split("/")[-1]
    return None

def get_video_details(video_id: str):
    try:
        request = youtube_client.videos().list(part="snippet", id=video_id)
        response = request.execute()
        if not response["items"]: return None
        item = response["items"][0]["snippet"]
        return {
            "video_id": video_id,
            "title": item["title"],
            "thumbnail_url": item["thumbnails"]["high"]["url"],
            "channel_name": item["channelTitle"]
        }
    except Exception as e:
        print(f"Error fetching details: {e}")
        return None

def get_transcript(video_id: str):
    """
    Fetches transcript using yt-dlp (Reliable) and cleans it (Readable).
    """
    print(f"📡 Fetching transcript with yt-dlp for {video_id}...")
    
    # 1. Setup Options
    temp_filename = f"temp_{video_id}"
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'skip_download': True,      # No video, just text
        'outtmpl': temp_filename,
        'quiet': True,
        'subtitleslangs': ['en'],
    }

    try:
        # 2. Download
        url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # 3. Find the file
        files = glob.glob(f"{temp_filename}*.vtt")
        if not files:
            print("⚠️ yt-dlp finished but no file found.")
            return None
        
        subtitle_file = files[0]

        # 4. Read and Clean
        transcript_parts = []
        with open(subtitle_file, "r", encoding="utf-8") as f:
            for line in f:
                # Skip header junk
                if "WEBVTT" in line or "Kind:" in line or "Language:" in line:
                    continue
                
                # CLEANING MAGIC: Remove <tags> and timestamps
                clean_line = re.sub(r'<[^>]+>', '', line)       # Remove <c> tags
                clean_line = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', '', clean_line) # Remove timestamps
                clean_line = clean_line.strip()
                
                # Save unique lines only
                if clean_line and "-->" not in clean_line:
                    if not transcript_parts or transcript_parts[-1] != clean_line:
                        transcript_parts.append(clean_line)

        full_text = " ".join(transcript_parts)

        # 5. Cleanup (Delete temp file)
        os.remove(subtitle_file)
        
        return full_text

    except Exception as e:
        print(f"⚠️ yt-dlp failed: {e}")
        # Cleanup
        for f in glob.glob(f"{temp_filename}*"):
            try: os.remove(f) 
            except: pass
        return None

if __name__ == "__main__":
    print("--- FINAL SYSTEM CHECK ---")
    test_id = "tekn7vd5fng&t=30s"
    
    # 1. Test Details
    details = get_video_details(test_id)
    if details:
        print(f"✅ Found Video: {details['title']}")

    # 2. Test Transcript
    print("------------------------------------------------")
    transcript = get_transcript(test_id)
    
    if transcript:
        print(f"✅ SUCCESS! Length: {len(transcript)} chars")
        print(f"📝 Preview: {transcript[:200]}...")
    else:
        print("❌ FAILED.")