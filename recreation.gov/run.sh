#!/bin/bash

# The first bash cli imput
# $1 is the first argument
FACILITY_ID=$1
TOUR_ID=$2
YEAR=$3
MONTH=$4


# Curl the URL.  Then pipe the output to jq to parse the JSON starting with the .facility_availability_summary_view_by_local_date key.  For each of the dates, look at the `tour_availability_summary_view_by_tour_id` key and for each key under there look for the `reservable` key.  If it's greater than 0, then print the local_date and reservable value.
AVAILABLE_DATES=$(curl -s "https://www.recreation.gov/api/ticket/availability/facility/${FACILITY_ID}/monthlyAvailabilitySummaryView?year=${YEAR}&month=${MONTH}&inventoryBucket=FIT&tourId=${TOUR_ID}" | jq -r '.facility_availability_summary_view_by_local_date | to_entries[] | select(.value.tour_availability_summary_view_by_tour_id | to_entries[].value.reservable > 0) | .key + "," + (.value.tour_availability_summary_view_by_tour_id | to_entries[].value.reservable | tostring)')

echo "$AVAILABLE_DATES"
