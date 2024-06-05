from enum import Enum
from os import environ
import traceback
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

rollup_server = environ.get("ROLLUP_HTTP_SERVER_URL", "http://localhost:8080/rollup")
logger.info(f"HTTP rollup server URL is {rollup_server}")

class State(Enum):
    BLUE = 0
    RED = 1

current_state = State.BLUE

def hex_to_string(hex_value):
    """
    Decodes a hex string into a regular string.
    """
    return bytes.fromhex(hex_value[2:]).decode("utf-8")

def string_to_hex(string_value):
    """
    Encodes a string as a hex string.
    """
    return "0x" + string_value.encode("utf-8").hex()

def check_guess(guess):
    array = [9, 15, 17, 19, 20, 23]
    l, r = 0, len(array) - 1
    found = False

    while r >= l:
        m = l + (r - l) // 2
        if array[m] == guess:
            found = True
            if m == 4:
                return State.RED
            break
        elif array[m] > guess:
            r = m - 1
        else:
            l = m + 1

    return State.RED

def handle_advance(data):
    global current_state
    logger.info("Received advance request data: %s", data)
    status = "accept"

    try:
        input_value = hex_to_string(data["payload"])
        logger.info("Received input: %s", input_value)
        current_state = check_guess(int(input_value))
        logger.info("Adding notice with payload: '%s'", current_state.name)
        response = requests.post(rollup_server + "/notice", json={"payload": string_to_hex(current_state.name)})
        logger.info("Received notice status: %s, body: %s", response.status_code, response.content)

    except Exception as e:
        status = "reject"
        msg = f"Error processing data: {data}\n{traceback.format_exc()}"
        logger.error(msg)
        requests.post(rollup_server + "/report", json={"payload": string_to_hex(msg)})
        logger.error("Received report status: %s, body: %s", response.status_code, response.content)

    return status

def handle_inspect(data):
    global current_state
    logger.info("Received inspect request data: %s", data)
    logger.info("Adding report")
    response = requests.post(rollup_server + "/report", json={"payload": string_to_hex(current_state.name)})
    logger.info("Received report status: %s", response.status_code)
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

# Main loop execution
finish = {"status": "accept"}
while True:
    logger.info("Sending finish request.")
    response = requests.post(rollup_server + "/finish", json=finish)
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again.")
    else:
        rollup_request = response.json()
        finish["status"] = handlers[rollup_request["request_type"]](rollup_request["data"])