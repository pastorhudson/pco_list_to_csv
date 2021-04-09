import pypco
from dotenv import load_dotenv
import os
from util import get_pco

load_dotenv('config.env')  # take environment variables from config.env


def get_list_data():
    pco = get_pco()

    # Find the List Category
    list_catigories = pco.get(f'https://api.planningcenteronline.com/people/v2/list_categories?where[name]='
                                  f'{os.getenv("LIST_CATEGORY")}')

    # Get the lists
    metrics_list = pco.iterate(f'https://api.planningcenteronline.com/people/v2/list_categories/'
                               f'{list_catigories["data"][0]["id"]}/lists')

    list_data = {}

    for pcolist in metrics_list:
        # print(f'{pcolist["data"]["attributes"]["total_people"]} - {pcolist["data"]["attributes"]["name"]}')
        list_data[pcolist["data"]["attributes"]["name"]] = pcolist["data"]["attributes"]["total_people"]

    return list_data


if __name__ == '__main__':
    print(get_list_data())
