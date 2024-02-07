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
