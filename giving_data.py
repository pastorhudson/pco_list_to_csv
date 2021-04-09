from dotenv import load_dotenv
import os
import locale
from util import get_mondays, get_pco
from datetime import datetime

locale.setlocale(locale.LC_ALL, '')

load_dotenv('config.env')  # take environment variables from config.env

pco = get_pco()


def parse_funds():
    """Parses the comma separated list of Fund names in the config.env
    returns list of tuples of (fund name, fund_id)"""
    funds = []
    for fund in os.getenv('FUNDS').split(","):
        funds.append((fund,get_fund_id(fund)))

    return funds


def get_fund_id(fund_name):
    """Takes a fund name string and returns the pco id for that fund"""
    return pco.get(f'https://api.planningcenteronline.com/giving/v2/funds?where[name]={fund_name}')['data'][0]['id']


def get_donations(date_range, fund_ids):
    """Takes a tuple of UTC date ranges , and a list of tuples containing (fund_name, fund_id and returns a dict:
    {Fund Name: TOTAL} for the period"""

    donations = pco.iterate(f'https://api.planningcenteronline.com/giving/v2/donations?'
                            f'order=-recieved_at'
                            f'&where[received_at][gte]={date_range[0]}'
                            f'&where[received_at][lt]={date_range[1]}'
                            '&include=designations,labels'
                            '&per_page=100')

    # print(f'https://api.planningcenteronline.com/giving/v2/donations?'
    #                         f'order=-recieved_at'
    #                         f'&where[received_at][gte]={date_range[0]}'
    #                         f'&where[received_at][lt]={date_range[1]}'
    #                         '&include=designations,labels'
    #                         '&per_page=100')

    donation_data = {}

    for donation in donations:
        donation_fund_id = donation['included'][0]['relationships']['fund']['data']['id']  # Donation Fund ID
        donation_amount = donation['data']['attributes']['amount_cents']  # Donation Amount
        for fund in fund_ids:
            if fund[1] == donation_fund_id:
                try:
                    donation_data[fund[0]] += donation_amount
                except KeyError:
                    if donation_amount > 0:
                        donation_data[fund[0]] = donation_amount
                    else:
                        donation_data[fund[0]] = 0

    for k, v in donation_data.items():
        donation_data[k] = locale.currency(v / 100)

    return donation_data


def get_donation_data():
    """Gets the data cells for the csv"""
    mondays = get_mondays()
    return get_donations((datetime.strftime(mondays[0], '%Y-%m-%dT%H:%M:%SZ'),
                          datetime.strftime(mondays[1], '%Y-%m-%dT%H:%M:%SZ')), parse_funds())


if __name__ == "__main__":
    print(get_donation_data())
