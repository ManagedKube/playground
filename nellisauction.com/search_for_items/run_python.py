# python script that takes in 4 user inputs via the command line input: FACILITY_ID, TOUR_ID, YEAR, MONTH. Then http get this url: https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}/monthlyAvailabilitySummaryView?year=${YEAR}&month=${MONTH}&inventoryBucket=FIT&tourId=${TOUR_ID}. It will return a json which we will parse in a loop

import requests
import sys
import os
import re 
import urllib.parse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

## Text file with items to search for
TEXT_FILE_WITH_ITEMS_TO_SEARCH_FOR = sys.argv[1]

## Slack channel to send messages to
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

## Get envars
debug_on = os.environ.get('DEBUG_ON') == 'true'
run_only_once = os.environ.get('RUN_ONLY_ONCE') # only do one loop of this and stop after the first free reservaction is found

## Disable slack call for local runs
slack_enabled = 'true'
if os.environ.get('DISABLE_SLACK') == 'true':
    slack_enabled = 'false'

## Print debug message if DEBUG_ON is set to 'true'
def debug_print(message):
    if debug_on:
        print(f"[DEBUG] {message}")

debug_print(f"SLACK_CHANNEL={SLACK_CHANNEL}")
debug_print(f"slack_enabled={slack_enabled}")
debug_print(f"run_only_once={run_only_once}")

## Send message to Slack
## doc: https://github.com/slackapi/python-slack-sdk#sending-a-message-to-slack
def send_to_slack(message):
    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    print(f"Sending Slack message to channel '{SLACK_CHANNEL}': {message}")

    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        debug_print(f"Slack response: {response}")
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print(f"Got an error sending message to Slack: {e.response['error']}")
        debug_print(f"Full Slack error response: {e.response}")


search_url = f"https://www.nellisauction.com/search?query="

with open(TEXT_FILE_WITH_ITEMS_TO_SEARCH_FOR, 'r') as file:
    for line in file:
        ## Do something with each line
        search_item = line.strip()
        print(f"Searching for: {search_item}")

        ## Construct URL with user inputs
        url = f"{search_url}{urllib.parse.quote(search_item)}"
        debug_print(f"Requesting URL: {url}")

        ## Make HTTP GET request and get JSON data
        ## Set the header or it will think it is a bot and respond with some error
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5' 
        }
        response = requests.get(url, headers=headers, params={}, timeout=60)

        debug_print(f"Response status code: {response.status_code}")

        data = response.text

        debug_print(f"Response body length: {len(data)} characters")
        debug_print(f"Response body: {data}")

        ## Extract everything between the <p class="__search-results-description"> and </span>
        ## This is where in the html it will say how many items that your search result has found
        ## The html: <p class="__search-results-description"><span>5 items found when searching for </span>
    
        # Define regular expression pattern
        pattern = r'<p class="__search-results-description">(.*?)</span>'

        # Use regular expression to extract text
        result = re.search(pattern, data)

        # Print extracted text
        if result:
            debug_print(f"Regex matched, raw text: {result.group(1)}")

            ## Remove unwanted characters around the returned string
            new_string = result.group(1).replace('<span>', '')
            new_string = new_string.strip()
            new_string = new_string.replace('items found when searching for', '')
            new_string = new_string.replace('item found when searching for', '')

            print(f"Found {new_string.strip()} item(s) for: {search_item}")

            ## Do something if the number of items found is greater than 0
            if int(new_string) > 0:
                print(f"Search with more than one item available: {search_item} | {url}")

                ## Send message to Slack
                debug_print(f"slack_enabled={slack_enabled}, about to send Slack message" if slack_enabled == 'true' else f"slack_enabled={slack_enabled}, skipping Slack message")
                if slack_enabled == 'true':
                    send_to_slack(f"""
                        Search with more than one item available: {search_item}
                        Link: {url}                                                                                                                                                
                    """)
            else:
                debug_print(f"No items found for: {search_item}, not sending Slack message")
        else:
            debug_print(f"Regex did not match search-results-description for: {search_item}. HTML may have changed or page did not load as expected.")
