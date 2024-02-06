# notify-on-event
The purpose of this set of scripts are to continuously search the houseseats.com site after a user has logged in
and search for specific keywords in the events list.  Once an event is found, it should send a Slack
notification to a Slack destination.

# Envars

```
export HOUSESEAT_USERNAME=
export HOUSESEAT_PASSWORD=
```

# Run
```
python3 search.py
```
