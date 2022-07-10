from custom_log import configure_logger
from rich import print
from rich.panel import Panel
from rich.text import Text
from flask import Flask, request, jsonify
import base64
import magic
from analysis import do_analysis

service = Flask(__name__)
log = configure_logger()


@service.route("/request/analysis", methods=["POST"])
def request_handler():
    # Get the request body as JSON object
    req_json = request.json

    # Try get the request Unique ID
    try:
        req_uid = req_json["uid"]
    except KeyError:
        # reject the request if the Unique ID is not provided
        return jsonify({"error": "Unique ID is not provided"}), 400

    # Get the request input
    input_base64 = req_json["input_base64"]

    # Decode base64 input
    input_bytes = base64.b64decode(input_base64)

    # Check if the input have MIME type and reject if it None
    input_mimetype = magic.from_buffer(input_bytes, mime=True)
    if input_mimetype is None:
        log.error("Input has no MIME type")
        return jsonify({"error": "Input has no MIME type"})

    log.info("Request received", req_uid=req_uid, input_mimetype=input_mimetype)
    do_analysis(input_bytes, req_uid)

    return jsonify({"status": "ok"})


@service.route("/request/head", methods=["HEAD"])
def head():
    return jsonify({"status": "ok"})
