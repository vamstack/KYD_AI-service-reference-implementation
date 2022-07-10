from helper import send_analysis_result
import cv2, numpy as np
import logging


def do_analysis(input_bytes, req_uid):
    ##  --->>> put analysis code here <<< --- ##
    # For example: make input_bytes into a greyscale image and send analysis back to KYD serice
    logging.info("Begining analysis")
    input_mat = cv2.imdecode(np.frombuffer(input_bytes, np.uint8), cv2.IMREAD_UNCHANGED)

    # Convert to greyscale
    logging.info("Converting to greyscale")
    input_mat = cv2.cvtColor(input_mat, cv2.COLOR_BGR2GRAY)

    logging.info("Analysis complete")

    ## Comment out the following line to disable sending analysis result to KYD service
    # logging.info("Sending analysis result to KYD service")
    # send_analysis_result(cv2.imencode(".png", input_mat)[1].tobytes(), req_uid)
