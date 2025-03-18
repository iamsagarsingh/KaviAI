from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import requests
from google import genai
from config import GenAIKey, FASTAPI_POST_URL
import json


def fetch_and_store():
    try:
        client = genai.Client(api_key=GenAIKey)

        GenAIPrompt="""Give me one 4 to 6 line in hinglish Kavita or poem or shayri that should be unique and in json format. for example the json format: {id:"",text:""}"""

        response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=GenAIPrompt,)
        
        jsonData = json.loads(response.text[8:-4])

        data = {"kavitaText":jsonData['text']}
        post_response = requests.post(FASTAPI_POST_URL,json=data)

        if post_response.status_code == 201:
            print("data stored successfully")
        else:
            print("failed to store data")
        
    except Exception as e:
        print(e)


def start_scheduler():
    """Start the scheduler."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store, IntervalTrigger(minutes=2))
    scheduler.start()
    print("schedular activated....")
