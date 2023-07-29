# playground
A playground



curl 'https://www.recreation.gov/api/ticket/availability/facility/233362?date=2023-06-20'
* Messa verde national part tours: https://www.recreation.gov/ticket/facility/233362


curl 'https://www.recreation.gov/api/ticket/availability/facility/10089005?date=2023-06-20'
* African Burial Ground National Monument Tours - https://www.recreation.gov/ticket/facility/10089005
* Guided AFBG Tour - https://www.recreation.gov/ticket/10089005/ticket/10089006
*                                                      <facility>      <tour_id>




# Balcony House
https://www.recreation.gov/ticket/233362/ticket/500
                              <facility_id>   <tour_id>


curl 'https://www.recreation.gov/api/ticket/availability/facility/233362?date=2023-06-20'


"tour_id": "500"


# Cliff Palace
The main URL for this location:
```bash
https://www.recreation.gov/ticket/233362/ticket/502
```


When the page loads and it is loading the calendar, it is making this call to get the initial data
for the calendar:
```bash
curl https://www.recreation.gov/api/ticket/availability/facility/233362/monthlyAvailabilitySummaryView?year=2023&month=06&inventoryBucket=FIT&tourId=502
```

Will return a json for every sing day of the month for the specific tour_id

```json
    "2023-06-21": {
      "availability_level": "HIGH",
      "facility_id": "233362",
      "local_date": "2023-06-21",
      "reserved_count": 729,
      "scheduled_count": 828,
      "tour_availability_summary_view_by_tour_id": {
        "502": {
          "availability_level": "HIGH",
          "booking_windows": null,
          "facility_id": "233362",
          "has_not_yet_released": false,
          "has_reservable": true,
          "has_walk_up": true,
          "local_date": "2023-06-21",
          "next_release_timestamp": null,
          "not_yet_released": 0,
          "reservable": 11,
          "reserved_count": 421,
          "scheduled_count": 513,
          "tour_id": "502",
          "walk_up": 90
        }
      }
    },
```
* `reservable` - how many spaces are available for this day
* `has_not_yet_released` - if you can reserve it now or not






When clicking on a day to see the list of available time slots it is making this call:
```bash
curl 'https://www.recreation.gov/api/ticket/availability/facility/233362?date=2023-06-10' 
```
* This does have all available time slots for every tour in this facility





# The script

```bash
./run.sh 233362 502 2023 06
```



curl https://www.recreation.gov/api/ticket/availability/facility/233362/monthlyAvailabilitySummaryView?year=2023&month=06&inventoryBucket=FIT&tourId=502 | jq '.facility_availability_summary_view_by_local_date | to_entries[] | .key + " " + (.value | tostring)'






# Python

```
pip install slack-sdk
```


python run_python.py 251853 194 2023 08 "09,10,11"


