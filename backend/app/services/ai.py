import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
# load_dotenv()
# API_KEY = "AIzaSyAsejezcur8Q6eCpHO_BZTSFQ9ufCQ2U44"
# API_KEY=os.getenv("GEMINI_API_KEY")
base_dir = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(base_dir / ".env")

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# genai.configure(api_key=API_KEY)

modelname="gemini-flash-latest"


def Summarize_text(text):

    if not text:
        return print("Error: No text provided")
    
    prompt=(f"summarize the following youtbe transcript into 3-5 concise bullet points: {text}")
    
    try:
        model=genai.GenerativeModel(modelname)
        response= model.generate_content(prompt)
        return response.text

    except Exception as e:
        return print(f"AI Error:{e}")   
    


if __name__ == "__main__":
    print("🧠 Testing AI Brain...")
    test_text = "Python is a programming language. It is great for web development and AI. It is easy to learn."
    
    # Call the function
    summary = Summarize_text(test_text)
    
    print("\n--- Result ---")
    print(summary)



