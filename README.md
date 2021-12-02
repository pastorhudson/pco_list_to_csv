# pco_list_to_csv
This is a script to dump selected lists, and other check in's data to a csv

# Configure
All configuration is handled in the config.env file.
Here is an example:
```
APPLICATION_ID=<Generate this on api.planningcenteronline.com>
SECRET=<Generate this on api.planningcenteronline.com>
# The List Catigory in Planning Center People you want to pull
LIST_CATEGORY=Church Metrics
# Comma separated list of Event:Headcount. Don't worry about multiple times. We'll get those automatically.
# eg Church:Worship Cent,Kids Min:Regular
HEAD_COUNT_EVENTS=Church:Worship Cent,Church:RK Volunteer
# Comma separated list of funds you want to pull
FUNDS=General,Building Fund
```
On Mac this confit.env needs to be put in your user home directory.

To run with python `python3 build_csv.py`