import os
import requests
import json
import base64
import logging


def send_analysis_result(output_mat, req_uid):
    VXNAT_APP_ID = os.environ.get("VXNAT_APP_ID")
    VXNAT_APP_TOKEN = os.environ.get("VXNAT_APP_TOKEN")
    VXNAT_APP_HOSTNAME = os.environ.get("VXNAT_APP_HOSTNAME")
    VXNAT_APP_OUTPUT_EVENT_TYPE = os.environ.get("VXNAT_APP_OUTPUT_EVENT_TYPE")

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer " + VXNAT_APP_TOKEN,
    }

    logging.info("Sending analysis result to KYD service")
    requests.post(
        f"https://{VXNAT_APP_HOSTNAME}/api/v1/app/{VXNAT_APP_ID}/msg/",
        headers=headers,
        data=json.dumps(
            {
                "eventType": VXNAT_APP_OUTPUT_EVENT_TYPE,
                "payload": {
                    "uid": req_uid,
                    "output_base64": base64.b64encode(output_mat).decode("utf-8"),
                },
            }
        ),
    )
