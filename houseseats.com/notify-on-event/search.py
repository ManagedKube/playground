# python script that takes in 4 user inputs via the command line input: FACILITY_ID, TOUR_ID, YEAR, MONTH. Then http get this url: https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}/monthlyAvailabilitySummaryView?year=${YEAR}&month=${MONTH}&inventoryBucket=FIT&tourId=${TOUR_ID}. It will return a json which we will parse in a loop

import requests
import sys
import os
import re 
import urllib.parse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import yaml

# How many tickets are you looking for per time slot
NUMBER_OF_RESERVABLE_PER_TIME_SLOT = 2
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

## Get envars
debug_on = os.environ.get('DEBUG_ON')

## Disable slack call for local runs
slack_enabled = 'true'
if os.environ.get('DISABLE_SLACK') == 'true':
    slack_enabled = 'false'

## Send message to Slack
## doc: https://github.com/slackapi/python-slack-sdk#sending-a-message-to-slack
def send_to_slack(message):
    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)


print('Starting program...')


# Open the state YAML file
with open('state.yaml', 'r') as file:
    # Load the YAML data from the file
    previous_state = yaml.safe_load(file)

# Now data is a list of dictionaries
print(previous_state)

new_state = []

# Create a session object
s = requests.Session()

# Define the login data
login_data = {
    'email': os.environ['HOUSESEAT_USERNAME'],
    'password': os.environ['HOUSESEAT_PASSWORD'],
    'submit': 'login',
    'lastplace': '',
}

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5' 
        }

# URL of the login page
login_url = 'https://lv.houseseats.com/member/index.bv'

# Send a POST request to the login page with your login data
s.post(login_url, data=login_data, headers=headers)

# Now s maintains the 'logged in' session. You can use it to send additional requests
response = s.get('https://lv.houseseats.com/member/ajax/upcoming-shows.bv?supersecret=&search=&sortField=&startMonthYear=&endMonthYear=&startDate=&endDate=&start=0', headers=headers)

# Print the content of the 'protected page'
# print(response.text)


# Find all instances of the <h1> title of a show
pattern = r'<h1><a href="./tickets/view/\?showid=(.*?)">(.*?)</a></h1>'

# Use re.findall() to find all instances of the pattern in the string
matches = re.findall(pattern, response.text.lower())

## Loop through the list of matches which should be all of the shows/events on the page
for event in matches:
    print(f'found: {event[0]} | {event[1]}')

    ## Compare to see if the event is in the exclude list.
    ## If it is in the exclude list, then do not send a message to Slack
    ## if it is not in the exclude list, then send a message to Slack
    found_exclude = False

    with open('items_to_exclude.txt', 'r') as file:
        for line in file:
            ## Do something with each line
            search_item = line.strip()
            # print(search_item)

            # Define regular expression pattern
            pattern = fr'{search_item}'

            # Use regular expression to extract text
            result = re.search(pattern, event[1].lower())

            # Print extracted text
            if result:
                print(f'found {search_item}')

                found_exclude = True

    ## If the event is not in the exclude list, then continue to process the event
    if found_exclude == False:
        print(f'[NOT IN EXCLUDE LIST] not found in exclude list: {event[0]} | {event[1]}')

        ## Add the event to the new state dictionary list
        new_state.append({
            'event_id': event[0],
            'event_name': event[1]
        })

        ## If the event is NOT in the previous state dictionary list then send a message to Slack
        ## and write it to the new state dictionary list
        found_in_previous_state = False

        for item in previous_state:
            if item['event_id'] == event[0]:
                found_in_previous_state = True

        if not found_in_previous_state:
            ## Send message to Slack
            print(f'[NOTIFY] Sending slack message for: {event[0]} | {event[1]}')
            if slack_enabled == 'true':
                send_to_slack(f"""
                    *[Houseseat v2]* Search found: <https://lv.houseseats.com/member/tickets/view/?showid={urllib.parse.unquote(event[0])}|{urllib.parse.unquote(event[1])}>  
                """)

# Output the new state dictionary list to the state.yaml file
with open('state.yaml', 'w') as file:
    # Write the YAML data to the file
    yaml.dump(new_state, file)
