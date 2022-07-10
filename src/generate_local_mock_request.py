import requests
import logging
import json
from rich import print

sample = json.load(open("request-analysis.sample.json"))

logging.info("Sending analysis result to KYD service")
res = requests.post(
    f"http://0.0.0.0:8080/request/analysis",
    headers={"Content-Type": "application/json; charset=utf-8"},
    data=json.dumps(sample),
)
print(res.json())
