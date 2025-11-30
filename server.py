from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
import os

app = FastAPI()

# Allow requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for incoming location data
class LocationData(BaseModel):
    latitude: float
    longitude: float
    timestamp: float

LOC_FILE = "locations.json"

# Ensure file exists
if not os.path.exists(LOC_FILE):
    open(LOC_FILE, "w").close()

# POST endpoint to receive live location
@app.post("/update_location")
def update_location(data: LocationData):
    entry = {
        "latitude": data.latitude,
        "longitude": data.longitude,
        "timestamp": data.timestamp,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(LOC_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return {"status": "ok"}

# GET endpoint to return all stored locations
@app.get("/locations")
def get_locations():
    items = []
    try:
        with open(LOC_FILE) as f:
            for line in f:
                items.append(json.loads(line))
    except:
        pass
    return items

# Optional root route
@app.get("/")
def root():
    return {"message": "Server is running!"}

