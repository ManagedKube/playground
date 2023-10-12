## This is a python script that reads from a local file that has a zip code on each line and then
## for each line, it will call the ford.com website and get the inventory for that zip code.

import requests
import json
import time
import datetime
import os
import sys
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

LOWEST_PRICE = 70000
SEARCH_RADIUS = 100
DEALER_SLUG = "O%2BvqNfNq6oPSDXJZ6w%2B70OkQTLnpMHLAKUQDRHGAaDzlUt6zJme%2BM17yTjbX4qi5" # Not really sure what this does

FORD_SEARCH_URL = f"https://shop.ford.com/aemservices/cache/inventory/dealer-lot?dealerSlug={DEALER_SLUG}&make=Ford&market=US&Order=Distance&PRange={LOWEST_PRICE}%3B73000&Radius={SEARCH_RADIUS}&inventoryType=Radius&model=transit+commercial&segment=Commercial-truck&zipcode="

## Open a file on the local system
with open('zipcodes.txt', 'r') as file:
    for line in file:
        # Do something with each line
        zip_code = line.strip()
        # print(zip_code)

        ## Construct URL with user inputs
        url = f"{FORD_SEARCH_URL}{zip_code}"

        ## The URL to get the JSON data
        # print("URL: " + url + "\n")

        ## Make HTTP GET request and get JSON data
        ## Set the header or it will think it is a bot and respond with some error
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5' 
        }
        response = requests.get(url, headers=headers, params={}, timeout=60)
        # response = requests.get(url, headers=headers, params={'input1': 'none', 'input2': 'none', 'input3': 'none'})
        data = response.json()

        response_status = data.get('status')

        if response_status == "success":
            # print(data.get('data').get('filterResults').get('ExactMatch').get('vehicles'))

            # There can be an empty map/dictionary returned if zero vehicles are found
            if len(data.get('data').get('filterResults')) > 0:

                # The number of vehicles in the returned JSON with the matching zip code and above $70k
                num_vehicles = len(data.get('data').get('filterResults').get('ExactMatch').get('vehicles'))

                # If there are vehicles, print out the zip code and the number of vehicles
                if num_vehicles > 0:
                    print(f"Zip code: {zip_code}")
                    print(f"Number of vehicles: {num_vehicles}")
                    print(f"URL: https://shop.ford.com/inventory/transitcommercial/results?Radius=100&PRange=70000%3B73000&Order=HighPrice&zipcode={zip_code}\n")

                    # Print our the vins in the returned JSON for this zip code
                    for vehicle in data.get('data').get('filterResults').get('ExactMatch').get('vehicles'):
                        print(vehicle.get('vin'))

                    print(f"========================================\n")

