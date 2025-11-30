from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LocationData(BaseModel):
    latitude: float
    longitude: float
    timestamp: float

@app.post("/update_location")
def update_location(data: LocationData):
    entry = {
        "latitude": data.latitude,  
        "longitude": data.longitude,
        "timestamp": data.timestamp,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("locations.json", "a") as f:
        f.write(json.dumps(entry) + "\n")

    return {"status": "ok"}

@app.get("/locations")
def get_locations():
    items = []
    try:
        with open("locations.json") as f:
            for line in f:
                items.append(json.loads(line))
    except:
        pass
    return items
