import csv
from list_data import get_list_data
from head_counts import get_headcount_data
from giving_data import get_donation_data
import time
import datetime
from util import get_mondays, test_config
from datetime import datetime, timedelta
import pyperclip
from dotenv import load_dotenv
import pathlib
import os
startTime = time.time()
load_dotenv('config.env')  # take environment variables from config.env

fields = []
row = []


# name of csv file
def get_filename():
    p = pathlib.Path('~/Documents/PCOMetrics/')
    p.expanduser().mkdir(parents=True, exist_ok=True)
    mondays = get_mondays()
    # We actually pull donations given before Monday at Midnight to ensure we get all the Sunday Donations.
    # So to make the filename reflect sunday we need to backup a day.
    next_monday = mondays[1] - timedelta(days=1)
    return f"{p.expanduser()}{datetime.strftime(mondays[0], '%m-%d-%Y')}-{datetime.strftime(next_monday, '%m-%d-%Y')}.csv"


def send_to_clipboard(fields, rows):
    clipboard_string = ""
    if len(fields) > 0 and len(row) > 0:
        if os.getenv('CLIPBOARD_HEADER') == "True":
            for field in fields:
                clipboard_string += f"{field}\t"
            clipboard_string += "\n"
        for r in row:
            clipboard_string += f"{r}\t"

    pyperclip.copy(clipboard_string)

    return


def build_donation_columns():
    print("Getting Giving Data", end=" ")
    for key, value in get_donation_data().items():
        fields.append(key)
        row.append(value)
    print("✔")
    return


def build_list_columns():
    print("Getting People List Data", end=" ")
    for key, value in get_list_data().items():
        fields.append(key)
        row.append(value)
    print("✔")

    return


def build_headcount_columns():
    print("Getting Headcount Data", end=" ")
    for key, value in get_headcount_data().items():  # Reversing order because we want 9am service first
        fields.append(key)
        row.append(value)
    print("✔")
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
print(f"Building CSV:\n"
      f"file://{get_filename()}")
build_donation_columns()
build_headcount_columns()
build_list_columns()

write_csv(fields, [row], get_filename())


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
send_to_clipboard(fields, row)
print("Data added to clipboard")
