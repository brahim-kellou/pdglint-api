import requests
import json

from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import PDGLINT_MODEL_ENDPOINT
from services import get_stats

url = PDGLINT_MODEL_ENDPOINT
headers = {'Content-type': 'application/json'}

app = FastAPI()

origins = [
    "http://pdglint-app.azurewebsites.net",
    "https://pdglint-app.azurewebsites.net",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=["*"],
)


@app.get("/")
def hello_pdglint():
    return {
        'Method': 'GET',
        'Hello': 'From PDglint!'
    }


@app.post("/")
async def get_score(request: Request):
    body = await request.body()
    data = json.loads(body)

    stats = get_stats(data)

    resp = requests.post(
        url,
        headers=headers,
        data=json.dumps({"data": [stats]})
    )
    resp_json = json.loads(resp.json())

    return resp_json
