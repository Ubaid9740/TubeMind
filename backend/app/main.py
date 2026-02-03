from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
from app.services.youtube import get_video_id, get_transcript, get_video_details
from app.services.ai import Summarize_text
from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class VideoRequest(BaseModel):
    url:str

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()        

@app.get("/")
def home():
    return {"message":"TubeMind backend is running"}

@app.post("/summarize")
def summarize_video(request: VideoRequest,db:Session = Depends(get_db)):
    print(f"recieved request {request.url}")

    video_id = get_video_id(request.url)
    if not video_id:
        raise HTTPException(status_code=400,detail="YT url invalid") 


# if the summary already exists in the database
    existing_video = db.query(models.Video).filter(models.Video.video_id == video_id).first()

    if existing_video:  
        print("Found in DB! returning savend summary")
        return {
            "video_id":video_id,
            "title": existing_video.title,
            "thumbnail_url": existing_video.thumbnail_url,
            "summary": existing_video.transcript_summary,
            "source": "database"
        }
    
    # else:
    print("not found in DB. Fetching from YT and AI...")
    video_details = get_video_details(video_id)

    title = video_details("title","Unknown Title") if video_details else "Unknown Title"
    thumbnail = video_details("thumbnail_url","") if video_details else ""
    channel = video_details("channel_name","Unknown Channel") if video_details else "Unknown Channel" 

    print("fetching transcript...")

    transcript = get_transcript(video_id) 
    if not transcript:
        raise HTTPException(status_code=404, detail="No Transcript found")
    
    print("Summarizing...")

    summary_text = Summarize_text(transcript)

    if not summary_text:
        raise HTTPException(status_code=500, detail="AI failed to generate a summary")
    
    new_video = models.Video(
        video_id = video_id,
        title = title,
        thumbnail_url = thumbnail,
        channel_name = channel,
        transcript_summary = summary_text
    )
    
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    print("saved to database")
    return {
        "video_id": video_id,
        "title": title,
        "thumbnail_url": thumbnail,
        "summary": summary_text,
        "source": "ai"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)