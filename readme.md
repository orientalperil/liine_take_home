restaurants can change their open hours so Hours has a datetime_range
hours listed can go into the next day
a restaurant for the same datetime_range can have multiple Hours records because they can open 9-12 and 5-10 on the same day
Hours.open_range, lower is inclusive, upper is exclusive
Hours.datetime_range, lower is inclusive, upper is exclusive

Script to load csv into database:
$ python manage.py runscript import_data

Access restaurant API at /restaurants/.  An ISO formatted date time "time" query string parameter is required.
