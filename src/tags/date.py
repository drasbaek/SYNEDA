'''
Create a list of dates in different formats.
'''

import pathlib
from datetime import datetime, timedelta
import locale
import numpy as np
import pandas as pd

def generate_dates(year1=1970, year2=2023):
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

    return date_list

def define_date_formats():
    '''
    Define a list of different date formats
    '''
    date_formats = [
        "%d. %b %y",                   # 20. jul 21
        "%d/%m/%y",                    # 20/07/21
        "%d. %B %Y",                   # 20. juli 2021
        "%B %d %Y",                    # Juli 20 2021
        "%Y-%m-%d",                     # 2021-07-20
        "%d-%m-%Y",                    # 20-07-2021
        "%d %b, %Y",                   # 20 jul, 2021
        "%A, %d. %B %Y",               # Tirsdag, 20. juli 2021
        "%d/%b/%Y",                    # 20/jul/2021
        "%b %dth, %Y",                 # jul 20th, 2021
        "%A, %d-%b-%y",                # Tirsdag, 20-jul-21
        "%A, %d. %B '%y",               # Tirsdag, 20. juli '21
    ]

    return date_formats

def format_dates(date_list, date_formats):
    '''
    Format dates randomly using a variety of date_formats. 
    Ensures that all formats are used equally often.

    Args:
        date_list (list): list of dates
        date_formats (list): list of date formats

    Returns:
        all_formatted_dates (list): list of formatted dates
    '''

    all_formatted_dates = []
    
    # set locale to danish to get danish month names
    locale.setlocale(locale.LC_TIME, "da_DK.utf-8")

    # dict for keeping track of how many times each format has been used
    format_count = {format_str: 0 for format_str in date_formats}

    for date_str in date_list:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            # Create a copy of date_formats, shuffle it using NumPy to randomize format selection
            shuffled_formats = date_formats.copy()
            np.random.shuffle(shuffled_formats)

            selected_formats = []

            # Select the first two formats that have the lowest usage count
            for format_str in shuffled_formats:
                if len(selected_formats) == 2:
                    break
                if format_count[format_str] == min(format_count.values()):
                    selected_formats.append(format_str)
                    format_count[format_str] += 1

            # Format the date using the selected formats and append to the list
            formatted_dates = [date_obj.strftime(format_str) for format_str in selected_formats]

            all_formatted_dates.extend(formatted_dates)

    return all_formatted_dates, format_count

def sample_dates_favor_recent(date_list, num_samples, cutoff=2000, ratio=(1, 0.25)):
    '''
    Sample dates from a list of dates, favouring recent dates above cutoff value. 

    Args:
        date_list (list): list of dates
        num_samples (int): number of samples to draw
        cutoff (int): year cutoff for favouring recent dates
        ratio (tuple): ratio of recent dates to older dates

    Returns:
        sampled_dates (list): list of sampled dates
    '''

    # make str dates into date time objects only to define weights
    date_objects = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in date_list]

    # define weights (favour recent dates above 2000)
    weights = np.where(np.array([date.year for date in date_objects]) >= cutoff, ratio[0], ratio[1])

    # sample with weights
    sampled_indices = np.random.choice(len(date_list), num_samples, p=weights / np.sum(weights))

    # extract sampled dates from sampled indices
    sampled_dates = [date_list[i] for i in sampled_indices]

    return sampled_dates

def main():
    # set seed
    np.random.seed(1209)

    # define paths
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "data"

    # generate a list of dates
    dates = generate_dates()

    # select a random subset of dates, favouring dates closer to the present
    dates_subset = sample_dates_favor_recent(dates, 300)

    # define a list of different date formats
    date_formats = define_date_formats()

    # generate balanced formats
    formatted_dates, format_count = format_dates(dates_subset, date_formats)

    # save to file
    df = pd.DataFrame(formatted_dates, columns=["entity"])

    # add weights and context col (to match other lists)
    df["weight"] = 1
    df["context"] = None

    # save to file
    df.to_csv(data_path / "DATE.csv", index=False)

if __name__ == "__main__":
    main()