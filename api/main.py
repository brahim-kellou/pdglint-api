import requests
import json

from fastapi import Request, FastAPI
from config import PDGLINT_MODEL_ENDPOINT_SCORE
from services import get_stats

url = PDGLINT_MODEL_ENDPOINT_SCORE
headers = {'Content-type': 'application/json'}

app = FastAPI()


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
