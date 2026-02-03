import sys
from youtube_transcript_api import YouTubeTranscriptApi

print("--- DOCTOR TEST V2 ---")

# 1. Test with the classic "Rick Roll" video (Very reliable captions)
test_video_id = "dQw4w9WgXcQ"

try:
    print(f"Attempting to fetch transcript for: {test_video_id}")
    
    # Fetch the transcript
    transcript = YouTubeTranscriptApi.get_transcript(test_video_id)
    
    print("\n✅ SUCCESS!")
    print(f"Transcript Length: {len(transcript)} lines")
    print(f"First line: {transcript[0]}")

except Exception as e:
    print("\n❌ FAILURE")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
    print("\nPOSSIBLE CAUSES:")
    print("1. IP Ban: You ran the script too many times too fast (Wait 1 hour).")
    print("2. Cookie Consent: YouTube is asking for a cookie click (happens in EU).")