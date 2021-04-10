import csv
from list_data import get_list_data
from head_counts import get_headcount_data
from giving_data import get_donation_data
import time
import datetime
from util import get_mondays, test_config
from datetime import datetime, timedelta
import pathlib
import pandas as pd
startTime = time.time()

fields = []
row = []


# name of csv file
def get_filename():
    pathlib.Path(f'{pathlib.Path.home()}/Documents/PCOMetrics').mkdir(parents=True, exist_ok=True)

    mondays = get_mondays()
    # We actually pull donations given before Monday at Midnight to ensure we get all the Sunday Donations.
    # So to make the filename reflect sunday we need to backup a day.
    next_monday = mondays[1] - timedelta(days=1)
    return f"{pathlib.Path.home()}/Documents/PCOMetrics/{datetime.strftime(mondays[0], '%m-%d-%Y')}-{datetime.strftime(next_monday, '%m-%d-%Y')}.csv"


def build_donation_columns():
    print("Getting Giving Data")
    for key, value in get_donation_data().items():
        fields.append(key)
        row.append(value)
    return


def build_list_columns():
    print("Getting People List Data")
    for key, value in get_list_data().items():
        fields.append(key)
        row.append(value)
    return


def build_headcount_columns():
    print("Getting Headcount Data")
    for key, value in get_headcount_data().items():
        fields.append(key)
        row.append(value)
    return


def write_csv(fields, rows, filename):
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)


test_config()
print(f"Building CSV for {get_filename()}")
build_donation_columns()
build_headcount_columns()
build_list_columns()

write_csv(fields, [row], get_filename())
df = pd.DataFrame([row], columns=fields)
df.to_clipboard(excel=True, index=False)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
print("Data added to clipboard")
