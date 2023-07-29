#!/bin/bash

# The first bash cli imput
# $1 is the first argument
FACILITY_ID=$1
TOUR_ID=$2
YEAR=$3
MONTH=$4

if $DEBUG == "true"; then
    curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}/monthlyAvailabilitySummaryView?year=${YEAR}&month=${MONTH}&inventoryBucket=FIT&tourId=${TOUR_ID}" | jq .
fi


# Curl the URL.  Then pipe the output to jq to parse the JSON starting with the .facility_availability_summary_view_by_local_date key.  For each of the dates, look at the `tour_availability_summary_view_by_tour_id` key and for each key under there look for the `reservable` key.  If it's greater than 0, then print the local_date value.
AVAILABLE_DATES=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}/monthlyAvailabilitySummaryView?year=${YEAR}&month=${MONTH}&inventoryBucket=FIT&tourId=${TOUR_ID}" | jq -r '.facility_availability_summary_view_by_local_date | to_entries[] | select(.value.tour_availability_summary_view_by_tour_id | to_entries[].value.reservable > 0) | .key')


#AVAILABLE_DATES=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}/monthlyAvailabilitySummaryView?year=${YEAR}&month=${MONTH}&inventoryBucket=FIT&tourId=${TOUR_ID}" | jq -r '.facility_availability_summary_view_by_local_date | to_entries[] | select(.value.tour_availability_summary_view_by_tour_id | to_entries[].value.reservable > 0) | .key + "," + (.value.tour_availability_summary_view_by_tour_id | to_entries[].value.reservable | tostring)')
#AVAILABLE_DATES=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}/monthlyAvailabilitySummaryView?year=${YEAR}&month=${MONTH}&inventoryBucket=FIT&tourId=${TOUR_ID}" | jq -r '.facility_availability_summary_view_by_local_date | to_entries[] | select(.value.tour_availability_summary_view_by_tour_id | to_entries[].value.reservable > 0) | .key + "," + (.value.tour_availability_summary_view_by_tour_id | to_entries[].value.reservable | tostring)')


echo "$AVAILABLE_DATES"



# Create a loop that will loop through the $AVAILABLE_DATES variable
for DATE in $AVAILABLE_DATES; do
    # Print the date
    echo "Date: $DATE"

    tour_time=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}?date=${DATE}" | jq -r '.[] | .tour_time | tostring')
    inventory_count=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}?date=${DATE}" | jq -r '.[] | .inventory_count.ANY | tostring')
    reservation_count=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}?date=${DATE}" | jq -r '.[] | .reservation_count.ANY | tostring')

    # Create a variable that will curl https://www.recreation.gov/api/ticket/availability/facility/251853?date=$DATE which will return a JSON object.  Pipe that to jq to parse the JSON starting with the first array position [0] and Look for the inventory_count.ANY value and reservation_count.ANY value and if inventory_count.ANY minus reservation_count.ANY is greater than 0, then print the time slot.  
    
    #AVAILABLE_TIMES=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}?date=${DATE}" | jq -r '.[] | to_entries[] | select(.value.inventory_count.ANY - .value.reservation_count.ANY > 0) | .key')
    
    # AVAILABLE_TIMES=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}?date=${DATE}" | jq -r '.timeslots | to_entries[] | select(.value.availability > 0) | .key + "," + (.value.availability | tostring)')

    # echo $AVAILABLE_TIMES

    echo "Tour Time: $tour_time"
    echo "Inventory Count: $inventory_count"
    echo "Reservation Count: $reservation_count"

    # exit 0

    count=0
    while IFS= read -r line; do
        echo "... $line ..."
        echo "inventory_count - reservation_count: $((inventory_count[$count] - reservation_count[$count]))"
        count=$((count+1))

        exit 0
    done <<< "$tour_time"


    # count=0
    # for i in "${tour_time}"; do
    #     echo "tour_time: $i"
    #     # echo the $count possition in $inventory_count variable
    #     # echo "inventory_count: ${inventory_count[$count]}"

    #     # inventory_count minus reservation_count
    #     # echo "inventory_count - reservation_count: $((inventory_count[$count] - reservation_count[$count]))"


    #     count=$((count+1))

    #     exit 0
    # done

    exit 0


    #AVAILABLE_TIMES=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}?date=${DATE}" | jq -r '.timeslots | to_entries[] | select(.value.availability > 0) | .key + "," + (.value.availability | tostring)')
    # AVAILABLE_TIMES=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/251853?date=$DATE" | jq -r '.timeslots | to_entries[] | select(.value.availability > 0) | .key + "," + (.value.availability | tostring)')

done

