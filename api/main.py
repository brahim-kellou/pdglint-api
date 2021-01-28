import requests
import json

from fastapi import Request, FastAPI
from config import PDGLINT_MODEL_ENDPOINT
from services import get_stats

url = PDGLINT_MODEL_ENDPOINT
headers = {'Content-type': 'application/json'}

app = FastAPI()

@app.get("/")
def hello_pdglint():
    return {
        'Hello': 'From PDglint!'
    }

@app.post("/score/")
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
