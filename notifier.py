import os
import time
import locale
import datetime
from tgtg import TgtgClient
from slack import WebClient
from slack.errors import SlackApiError

tgtg_email = os.environ.get('TGTG_EMAIL')
tgtg_password = os.environ.get('TGTG_PASSWORD')
slack_api_token = os.environ.get('SLACK_API_TOKEN')

# login with email and password
tgtg_client = TgtgClient(email=tgtg_email, password=tgtg_password)
slack_client = WebClient(token=slack_api_token)

cache = {}

def sendMessage(text):
    try:
        response = slack_client.chat_postMessage(channel='#tgtg', text=text)
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")

while True:
    try:
        items = tgtg_client.get_items()

        for item in items:
            id = item["item"]["item_id"]
            if id in cache and cache[id] <= item["items_available"]:
                cache[id] = item["items_available"]
                continue
            cache[id] = item["items_available"]
            bag = "bag"
            if item["items_available"] > 1:
                bag = "bags"
            msg = "{} {} available at {}\n".format(item["items_available"], bag, item["display_name"])
            msg += "Pickup time: {} to {}".format(item["pickup_interval"]["start"], item["pickup_interval"]["end"])
            sendMessage(msg)
    except Exception as e:
        print(f"Got an error: {e}")
    time.sleep(30)
