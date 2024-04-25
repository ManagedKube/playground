# Alert on Low Price

This will use the Google Search Shopping API to search for an items and alert on the lowest prices.

The Google Search Shopping API needs some post filtering.  Here is the pricess.

Lets say you search for "Aqara water leak sensor 3 pack"

```yaml
search_items:
- item: Aqara water leak sensor 3 pack
  additional_title_filters:
  - 3 pack
  - something else
  not_from_these_sellers:
  - AliExpress.com
  - eBay
  price:
    low: 25
    high: 53
```

It will bring back some undesirable results.  We will do some post processing:

## Dont process from not_from_these_sellers
If the seller of the item is from this list, it wont process this item further


## additional_title_filters
It will bring back items that are not the 3 pack.

The list of additional_title_filters allows us to keep on filtering until we only
get what we want to see

## Filter by price
Then there is a price filter for low and high.  The price has to be inbetween these two
values

# Google SERG API results
```json
"shopping_results":[
    {
        "position": 1,
        "title": "Aqara Water Leak Sensor, Requires Aqara Hub, Wireless Water Leak Detector ...",
        "link": "https://www.amazon.com/Aqara-11LM-SJCGQ-Water-Sensor/dp/B07D39MSZS?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A35PXP61BJ01A2",
        "product_link": "https://www.google.com/shopping/product/16070575325377975061?gl=us",
        "product_id": "16070575325377975061",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=United+States&product_id=16070575325377975061",
        "number_of_comparisons": "10+",
        "comparison_link": "https://www.google.com/shopping/product/16070575325377975061/offers?hl=en&gl=us&uule=w+CAIQICINVW5pdGVkIFN0YXRlcw&q=aqara+water+leak+sensor&prds=eto:7824488265108361142_0,pid:256602637212884877,rsk:PC_15591572458261802167&sa=X&ved=0ahUKEwi6mOye99uFAxXwkK8BHUnACxQQ3q4ECP0J",
        "serpapi_product_api_comparisons": "https://serpapi.com/search.json?engine=google_product&filter=eto%3A7824488265108361142_0%2Cpid%3A256602637212884877%2Crsk%3APC_15591572458261802167&gl=us&offers=1&product_id=16070575325377975061&sa=X&uule=w+CAIQICINVW5pdGVkIFN0YXRlcw&ved=0ahUKEwi6mOye99uFAxXwkK8BHUnACxQQ3q4ECP0J",
        "source": "Amazon.com - Seller",
        "price": "$18.99",
        "extracted_price": 18.99,
        "best_match": true,
        "rating": 3.7,
        "reviews": 11,
        "extensions":
        [
            "Adjustable Alarm",
            "Siri"
        ]
        ,
        "thumbnail": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQUhBxkP3xIg3RNHb0DdL-UCmEtmcC5rtCXy2wa2HQ1H7qS9C43XyiKU15apUfBsYP5A0zHuEW8e3btTNEHmPNBU0SUYmXxwyuu91X81lbj&usqp=CAE",
        "delivery": "$5.99 delivery"
    }
    ,
```

# Setup
Can get the google serg API key at: https://serpapi.com/playground?engine=google_shopping&q=Aqara+water+leak+sensor+3+pack&location=United+States&gl=us&hl=en

env:
```
export SERP_API_KEY=
export SEARCH_ITEMS_YAML_FILE=search_items_gar.yaml
```

Run:
```
pip3 install google-search-results
pip3 install pyyaml
```