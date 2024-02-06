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
