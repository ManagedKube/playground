# python script that takes in 4 user inputs via the command line input: FACILITY_ID, TOUR_ID, YEAR, MONTH. Then http get this url: https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}/monthlyAvailabilitySummaryView?year=${YEAR}&month=${MONTH}&inventoryBucket=FIT&tourId=${TOUR_ID}. It will return a json which we will parse in a loop

import requests
import sys
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

## Get user inputs
FACILITY_ID = sys.argv[1]
TOUR_ID = sys.argv[2]
YEAR = sys.argv[3]
MONTH = sys.argv[4]

# How many tickets are you looking for per time slot
NUMBER_OF_RESERVABLE_PER_TIME_SLOT = 2

## Get envars
debug_on = os.environ.get('DEBUG_ON')

## Send message to Slack
## doc: https://github.com/slackapi/python-slack-sdk#sending-a-message-to-slack
def send_to_slack(message):
    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    try:
        response = client.chat_postMessage(channel='#random', text=message)
        assert response["message"]["text"] == message
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

## Construct URL with user inputs
url = f"https://www.recreation.gov/api/ticket/availability/facility/{FACILITY_ID}/monthlyAvailabilitySummaryView" #?year={YEAR}&month={MONTH}&inventoryBucket=FIT&tourId={TOUR_ID}"

print("URL: " + url + "\n")

## Make HTTP GET request and get JSON data
## Set the header or it will think it is a bot and respond with some error
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers, params={'year': YEAR, 'month': MONTH, 'inventoryBucket': 'FIT', 'tourId': TOUR_ID})
data = response.json()

if debug_on == 'true':
    print("XXXXXXXXXXXXXXXXXXXX")
    print(response.content)
    print(f"URL: {url}?year={YEAR}&month={MONTH}&inventoryBucket=FIT&tourId={TOUR_ID}\n")
    print("XXXXXXXXXXXXXXXXXXXX")

## Loop through JSON data on the `facility_availability_summary_view_by_local_date` key
for facility_availability_summary_view_by_local_date in data:
    print(facility_availability_summary_view_by_local_date)

    try:
        # For each item in facility_availability_summary_view_by_local_date that starts and the key starts with a number loop through it
        for a_date in data.get(facility_availability_summary_view_by_local_date):
            print(a_date)

            # print(data.get(facility_availability_summary_view_by_local_date).get(a_date).get('tour_availability_summary_view_by_tour_id').get(TOUR_ID).get('reservable'))

            # THis is the total reservable slots for the day.  It could be 1 slot free for the 9:00am time slot and 1 slot free for the 10:00am time slot.  So it is 2 reservable slots for the day
            reservable = data.get(facility_availability_summary_view_by_local_date).get(a_date).get('tour_availability_summary_view_by_tour_id').get(TOUR_ID).get('reservable')

            # We need query each day which will give us the time slots for that day and then we can
            # calculate how many slots are available for each time slot
            if reservable > NUMBER_OF_RESERVABLE_PER_TIME_SLOT:
                print(f"reservable: {reservable}\n")

                #############################################
                # Lets look at the time slots in each day
                #############################################
                daily_timeslot_url = f"https://www.recreation.gov/api/ticket/availability/facility/{FACILITY_ID}"
                daily_timeslot_response = requests.get(daily_timeslot_url, headers=headers, params={'date': a_date})
                daily_timeslot_data = daily_timeslot_response.json()

                if debug_on == 'true':
                    print("XXXXXXXXXXXXXXXXXXXX")
                    print(daily_timeslot_response.content)
                    print(f"URL: {daily_timeslot_url}?date={a_date}\n")
                    print("XXXXXXXXXXXXXXXXXXXX")

                for a_daily_timeslot in daily_timeslot_data:
                    print("yyyyyyyy")

                    tour_time = a_daily_timeslot.get('tour_time')
                    reservation_count = a_daily_timeslot.get('reservation_count').get('ANY')
                    inventory_count = a_daily_timeslot.get('inventory_count').get('ANY')

                    print(f"tour_time: {tour_time}")
                    print(f"reservation_count: {reservation_count}")
                    print(f"inventory_count: {inventory_count}")

                    if (inventory_count - reservation_count) > NUMBER_OF_RESERVABLE_PER_TIME_SLOT:
                        print(f"inventory_count - reservation_count: {inventory_count - reservation_count}\n")

                        # There are free slots available that is over the NUMBER_OF_RESERVABLE_PER_TIME_SLOT
                        # Send this information to Slack
                        send_to_slack("hello world")


    except AttributeError:
        print("AttributeError: 'NoneType' object has no attribute 'get'")
        break


