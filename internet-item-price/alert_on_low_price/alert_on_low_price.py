from serpapi import GoogleSearch
import yaml
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

## This dashboard helps you build your search query
## https://serpapi.com/playground?engine=google_shopping&q=aqara+water+leak+sensor+3+pack&location=United+States&gl=us&hl=en

api_key = os.environ['SERP_API_KEY']
search_items_gar_yaml = os.environ['SEARCH_ITEMS_YAML_FILE']
## Slack channel to send messages to
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

## Disable slack call for local runs
slack_enabled = 'true'
if os.environ.get('DISABLE_SLACK') == 'true':
    slack_enabled = 'false'

## Send message to Slack
## doc: https://github.com/slackapi/python-slack-sdk#sending-a-message-to-slack
def send_to_slack(message):
    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)

## Open the yaml file and read the contents
with open(search_items_gar_yaml, 'r') as file:
    data = yaml.safe_load(file)

# Access the list by its key and loop through it
for item in data['search_items']:
    print(f"Searching for: {item['item']}")

    ## Set the search parameters
    params = {
      "api_key": api_key,
      "engine": "google_shopping",
      "google_domain": "google.com",
      "q": item['item'],
      "gl": "us",
      "hl": "en",
      "location": "United States"
    }

    ## Google Shopping API search
    search = GoogleSearch(params)
    results = search.get_dict()

    ## Loop through the results and run our various post result processing
    for product in results['shopping_results']:

      ## If the key product['source'] is not found, then stop processing this product
      if 'source' not in product:
        continue

      ## If the words in not_from_these_sellers is found in the product['source'], then stop processing this product
      if 'not_from_these_sellers' in item and any(x.lower() in product['source'].lower() for x in item['not_from_these_sellers']):
        # print(f"Skipping (not_from_these_sellers): {product['source']}\n")
        continue

      ## For each additional_title_filters in the yaml file list, check if the words are in the product['title'].  
      ## All strings has to appear in the product['title'].  If it is not, then stop processing this product
      should_skip_item = False
      for a_title_filter in item['additional_title_filters']:
        if a_title_filter.lower() not in product['title'].lower():
            # print(f"Skipping {a_title_filter.lower()}: {product['title']}\n")
            should_skip_item = True

      ## If we did not find all of the additional_title_filters strings in the title, then skip this product
      if should_skip_item:
        continue

      ## If the price in item['price']['high'] is greater than the product['extracted_price'], then skip this product
      if float(product['extracted_price']) > float(item['price']['high']):
        # print(f"Skipping (price): {product['price']}\n")
        continue

      ## If the price in item['price']['low'] is lower than the product['extracted_price'], then skip this product
      if float(product['extracted_price']) < float(item['price']['low']):
        # print(f"Skipping (price): {product['price']}\n")
        continue

      ## Print the items that are left after all of the various filters
      print(f"Title: {product['title']}\nPrice: {product['price']}\nSource: {product['source']}\n{product['product_link']}\n")

      ## This product passed all of the filters
      ## Send message to Slack
      if slack_enabled == 'true':
          send_to_slack(f"""
              Source: managedkube/playground/internet-item-price/alert_on_low_price
              Title: {product['title']}
              Price: {product['price']}
              Source: {product['source']}
              {product['product_link']}                                                                                                                                 
          """)
