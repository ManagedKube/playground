# trusted-traveler-scheduler 

Source: https://github.com/everettsouthwick/trusted-traveler-scheduler

## Run locally

```
python3 -m venv my_env
source my_env/bin/activate
pip3 install -r requirements.txt
```

## Test notifications
```
python3 ttp.py -t
```

## Running
```
python3 ttp.py -u slack://xxx/xxx/xxx
```


  "location_ids": [ 5020, 5026, 5021, 5022, 5024, 5025, 5026, 5027, 5028, 5029, 5030, 5031, 5032, 5060, 5080, 5100, 5101, 5120, 5160, 5161, 5223, 5500, 5520, 16502, 16511, 16546 ],



    def _get_schedule(self, location_id: int) -> None:
        """
        Retrieves the schedule for the given location ID and evaluates the available appointment times. If there are
        any new appointments that meet the criteria specified in the configuration, a notification is sent.

        :param location_id: The ID of the location to retrieve the schedule for.
        :type location_id: int
        :return: None
        """
        try:
            time.sleep(1)
            appointments = requests.get(
                GOES_URL_FORMAT.format(location_id), timeout=30
            ).json()

            if not appointments:
                print(f"{datetime.today():%Y/%m/%d %H:%M:%S}: No active appointments available for location {location_id}.")
                return

            hasWeekendSchedule = False
            
            schedule = []
            all_active_appointments = []
            for appointment in appointments:
                if appointment["active"]:
                    schedule = self._evaluate_timestamp(
                        schedule, location_id, appointment["startTimestamp"]
                    )

                    datetime_obj = datetime.strptime(appointment["startTimestamp"], "%Y-%m-%dT%H:%M")
                    formatted_string = datetime_obj.strftime("%A, %B %d, %H:%M")
                    print(f"GarDebug: the appointment datetime stamp formatted_string: {formatted_string} | {location_id}")

                    pattern = r"Sunday|Friday|Saturday"
                    match = re.search(pattern, formatted_string)

                    if match:
                        print("The string contains a weekend day.")
                        hasWeekendSchedule = True
                    else:
                        print("The string does not contain a weekend day.")
                    
                    all_active_appointments.append(datetime.strptime(appointment["startTimestamp"], "%Y-%m-%dT%H:%M").isoformat())

            self._clear_database_of_claimed_appointments(location_id, all_active_appointments)

            print("here")

            if not schedule:
                return

            print("here2")

            # if hasWeekendSchedule:
            print("GarDebug: notify")
            self.notification_handler.new_appointment(location_id, schedule)
            

        except OSError:
            return


Nexus onlY; 5020, 5120, 5160, 16511