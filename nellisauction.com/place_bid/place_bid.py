import requests
import sys
import os
import re 
import urllib.parse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

## Text file with items to search for
# TEXT_FILE_WITH_ITEMS_TO_SEARCH_FOR = sys.argv[1]

## Slack channel to send messages to
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

## Get envars
debug_on = os.environ.get('DEBUG_ON')
run_only_once = os.environ.get('RUN_ONLY_ONCE') # only do one loop of this and stop after the first free reservaction is found

## Disable slack call for local runs
slack_enabled = 'true'
if os.environ.get('DISABLE_SLACK') == 'true':
    slack_enabled = 'false'

## Send message to Slack
## doc: https://github.com/slackapi/python-slack-sdk#sending-a-message-to-slack
def send_to_slack(message):
    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)

## Login to Nellis Auction
login_url = f'https://www.nellisauction.com/login'

# Create a Session which will keep the cookies
s = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

login_params = {
    '__rvfInternalFormId': 'login',
    'email': os.environ['NELLI_EMAIL'],
    'password': os.environ['NELLI_PASSWORD'],
}

response = s.post(login_url, headers=headers, data=login_params)

# print(response.text)

# The cookies are stored in the Session's cookie jar
print(s.cookies)

# ## Testing to get a post authentication page
# response = s.get('https://www.nellisauction.com/dashboard/auctions/watchlist')

# ## Should see what you have in your watchlist in the output
# print(response.text)

## Place a bid
bid_url = f'https://www.nellisauction.com/api/bids'

## Same as the curl --data-raw flag
bid_data = '{"productId":28158068,"bid":28}'

headers_bid = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Cookie': '__session=eyJ1c2VySWQiOjMzNTI0NywidXNlckF1dGhUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpwWkNJNk16TTFNalEzTENKcFlYUWlPakUzTVRRNE5qSTVNRE1zSW1WNGNDSTZNVGN4TnpRMU5Ea3dNMzAuQzBSTXp4LXd0WTI3eXgxdE43OVN3R1Y0cGxRSGZEVHcwT3hiYUtjU2g4VSJ9.ioZKnQGlto2s6iPwH%2BrbjHXkU1b%2F6IjdDXcBJx51kyc;',
}

response = requests.post(bid_url, headers=headers_bid, data=bid_data)

print(response.text)
