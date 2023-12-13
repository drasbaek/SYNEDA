'''
Create a list of dates in different formats.
'''

import pathlib
from datetime import datetime, timedelta
import locale
import numpy as np
import pandas as pd

def generate_dates(n_dates, year1=1970, year2=2023):
    '''
    Generate a list of dates every day between two years (e.g., 1970-2023)
    '''
    # define start and end date
    start_date = datetime(year1, 1, 1)
    end_date = datetime(year2, 12, 31)

    # how many days between each date
    delta = timedelta(days=1)

    date_list = []

    while start_date <= end_date:
        date_list.append(start_date.strftime("%Y-%m-%d"))
        start_date += delta

    # sample a subset of dates
    sampled_date_list = np.random.choice(date_list, n_dates, replace=False)

    return sampled_date_list

def define_date_formats():
    '''
    Define a list of different date formats
    '''
    date_formats = {
        "%d. %b %y": 2,                    # 20. Jul 21
        "%d/%m/%y": 15,                    # 20/07/21
        "%d. %B %Y": 25,                   # 20. Juli 2021
        "%B %d %Y": 2,                     # Juli 20 2021
        "%Y-%m-%d": 2,                     # 2021-07-20
        "%d-%m-%Y": 10,                     # 20-07-2021
        "%d %b, %Y": 2,                    # 20 jul, 2021
        "%A, %d. %B %Y": 8,                # Tirsdag, 20. juli 2021
        "%d/%b/%Y": 2,                     # 20/jul/2021
        "%A, %d-%b-%y": 2,                 # Tirsdag, 20-jul-21
        "%A, %d. %B '%y": 5,               # Tirsdag, 20. juli '21
        "%d-%m-%y": 8,                     # 20-07-21
        "%Y": 20,                           # 2021 
        "%A": 20,                           # Mandag
        "%B": 20,                           # Juli
    }

    return date_formats

def define_specific_dates():
    '''
    Specifiy some specific date formats
    '''
    set_formats_dict = {
        "i morgen": 5,
        "imorgen": 2,
        "igår": 2,
        "i går": 5,
        "i dag": 5,
        "idag": 2,
        "næste uge": 2,
        "næste måned": 2,
        "næste år": 2,
        "overmorgen": 3,
        "sidste uge": 2,
        "sidste måned": 2,
        "sidste år": 2,
    }

    periods_dict = {
        "en måned": 5,
        "to måneder": 2,
        "9 måneder": 2,
        "elleve måneder": 2,
        "en uge": 2,
        "fire uger": 2,
        "fem-seks uger": 2,
        "18 uger": 2,
        "1910'erne": 2,
        "firserne": 2,
        "90'erne": 2,
        "1950'erne": 2,
        "et år": 5,
        "15 år": 2,
        "3 år": 2,
        "syv år": 2,
        "ni år": 2,
        "10-årig": 2,
        "tolvårig": 1,
        "toårig": 1,
        "femårig": 1,
        "halvtredsårig": 1,
        "8-11-årige": 1,
        "+18 år": 1,
        "+16 år": 1,
    }

    # combine dicts 
    specific_formats = {**set_formats_dict, **periods_dict}

    # make into a list (where key is repeated n times for n values)
    all_specific_formats = [key for key, value in specific_formats.items() for _ in range(value)]

    return all_specific_formats

def format_dates():
    '''
    Format dates randomly using a variety of date_formats.
    '''
    # generate a list of dates
    date_formats = define_date_formats()

    # compute length of ents 
    num_ents = sum(date_formats.values())

    # generate dates 
    dates = generate_dates(n_dates=num_ents)

    # make into a list (where key is repeated n times for n values)
    all_formats = [key for key, value in date_formats.items() for _ in range(value)]

    formatted_dates = []

    # set locale to danish to get danish month names
    locale.setlocale(locale.LC_TIME, "da_DK.utf-8")

    for i, date in enumerate(dates):
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        # format the date
        formatted_date = date_obj.strftime(all_formats[i])

        formatted_dates.append(formatted_date)

    return formatted_dates

def main(): 
    np.random.seed(1209)

    # define paths
    path = pathlib.Path(__file__)
    outpath =  path.parents[2] / "dbase" / "entities_lists"

    # add specific dates
    specific_dates = define_specific_dates()

    # format dates
    formatted_dates = format_dates()

    # combine lists
    all_dates = formatted_dates + specific_dates

    # save to file
    df = pd.DataFrame(all_dates, columns=["entity"])

    # add weights and context col (to match other lists)
    df["weight"] = 1
    df["context"] = None

    # save to file
    df.to_csv(outpath / "DATE.csv", index=False)
    
if __name__ == "__main__":
    main()