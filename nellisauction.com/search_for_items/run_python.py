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

## Extract the number of items found from the search results page HTML.
##
## Nellis renders the results count as text like:
##   5 items found when searching for
##   1 item found when searching for
##   181 items found for hangers
## The exact wording (e.g. "found when searching for" vs "found for") as well
## as the surrounding tags/CSS class names are subject to change, which is
## what broke the previous regex that depended on an exact
## `<p class="__search-results-description">` element and a fixed phrase. To
## be resilient to both markup and wording changes, strip all HTML tags first
## and then just look for "<number> item(s) found" in the resulting plain text.
def extract_number_of_items_found(html):
    ## Remove HTML tags so the count phrase is contiguous plain text
    ## regardless of what elements/classes wrap the number and the words.
    plain_text = re.sub(r'<[^>]+>', ' ', html)
    plain_text = re.sub(r'&nbsp;', ' ', plain_text, flags=re.IGNORECASE)
    plain_text = re.sub(r'\s+', ' ', plain_text)

    pattern = r'(\d+)\s+items?\s+found'
    result = re.search(pattern, plain_text, re.IGNORECASE)

    if result:
        return int(result.group(1))

    return None


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

        ## Extract the number of items found from the page.
        ## This is where in the html it will say how many items that your search result has found
        ## e.g. the rendered text: "5 items found when searching for" or "1 item found when searching for"
        num_items_found = extract_number_of_items_found(data)

        # Print extracted text
        if num_items_found is not None:
            debug_print(f"Regex matched, number of items found: {num_items_found}")

            print(f"Found {num_items_found} item(s) for: {search_item}")

            ## Do something if the number of items found is greater than 0
            if num_items_found > 0:
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
