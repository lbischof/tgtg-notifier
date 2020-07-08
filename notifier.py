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
    items = tgtg_client.get_items()

    for item in items:
        if item["items_available"] == 0:
            continue
        id = item["item"]["item_id"] + item["purchase_end"]
        if id in cache and cache[id]:
            continue
        cache[id] = True
        bag = "bag"
        if item["items_available"] > 1:
            bag = "bags"
        msg = "{} {} available at {}\n".format(item["items_available"], bag, item["display_name"])
        msg += "Pickup time: {} to {}".format(item["pickup_interval"]["start"], item["pickup_interval"]["end"])
        sendMessage(msg)
    time.sleep(30)
