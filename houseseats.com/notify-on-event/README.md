# notify-on-event
This bot will use an authenticated houseseat account to get a list of events.  It will send a Slack notification
for any events that are not in the items_to_exclude.txt file.

# Envars

```
export HOUSESEAT_USERNAME=
export HOUSESEAT_PASSWORD=
```

# Run
```
python3 search.py
```

# The process

Logs in

Gets the events page's source

Search for and get a list of all instances of the pattern:
```
<h1><a href="./tickets/view/?showid=1743">Murray The Magician at Tropicana Las Vegas</a></h1>
```
This would be all of the events.

With this list, loop through it.

For each items found, compare it to the items in the `items_to_exclude.txt` file list.

If the item is in the exclude list, then skip it.

If the item is not in the exclude list, send and alert on it


Then for each item, if the string in the excluded text file is not in there, it will send a
notification.  This represents a show that we don't know about and is interested in.  There are
new shows or one time shows that comes up sometimes and these are the shows we are trying to find.




## scratch

New process:
* Open the state.yaml file and read it the yaml to a list of dictionaries
* Go and get a list of all the events
* Loop through the new events list
* If the event is in the exclude file list, then dont process this event anymore, else continue
* If the event is NOT in the previous state dictionary list 
  * then send a notification to slack
  * add it into the new state list dictionary
* If the event is in the previous state dictionary list
  * add it into the new state list dictionary
* Output the new state list dictionary to the state.yaml file


What this should do based on how events shows up and leaves:
* 7:00pm battle bot comes up
* alert goes to slack
* 7:05pm battle bots does not alert again
* 7:10pm battle bots is removed 
* 7:15pm battle bots shows up again
* alert goes to slack

This means that it will only alert on new events that freshly comes up.
