'''
Generate number lists

NB. Note that it can both be numbers (e.g., 1-100) and words (e.g., en-ti)
'''
import pathlib
import pandas as pd
import numpy as np

def cardinal():
    '''
    Generate cardinal numbers with random numbers
    ''' 
    pass 

def date():
    '''
    Generate dates with different formats
    '''
    pass

def percent(): 
    '''
    Generate numbers with percentage 
    '''
    pass


def quantity():
    '''
    Generate quantities with different units 
    '''
    pass


def money(data_path): 
    '''
    Generate money with different currencies from list. 
    
    (Note that we need to account for all kinds of weird formatting e.g., 1,000.00 kr and 200DKK, 200 DKK, 200 kr. 200kr.)
    '''
    # read in data
    df = pd.read_excel(data_path / "LISTS.xlsx", sheet_name="MONEY")

    # generate random numbers (100)
    small_numbers = np.random.randint(1, 100, size=100)
    big_numbers = np.random.randint(1000, 10000, size=50)
    numbers_words = ["to", "tre", "fire", "fem", "seks", "syv", "otte", "ni", "ti", "tusinde", "hundrede", "halvtreds", "halvfjerds", "tres", "firs", "halvfems", "halvfems"]

    # combine numbers and words
    numbers = np.concatenate([small_numbers, big_numbers, numbers_words])

    # weights (TEMP)
    df["weight"] = 1
    total_weight = df["weight"].sum()
    df["normalized_weight"] = df["weight"] / total_weight

    # define string invalid currencies, all currencies that have single quantiy as NO in df + ",-"
    string_invalid_currencies = df[df["only_single_quantity"] == "YES"]["entity"].tolist()
    string_invalid_currencies.append(",-")

    # filter out invalid currencies
    df_string_valid =  df[~df["entity"].isin(string_invalid_currencies)]

    formatted_numbers = []

    for num in numbers: 
        # sample currency based on weight col 
        currency = np.random.choice(df["entity"], p=df["normalized_weight"])

        # extract index of currency
        currency_idx = df[df["entity"] == currency].index[0]

        # extract placement of currency
        placement = df.loc[currency_idx, "placement"]

        # identify single quantity 
        single_quantity = df.loc[currency_idx, "only_single_quantity"]

        # define accepted formats
        after_format = f"{num} {currency}"
        before_format = f"{currency} {num}"
        after_no_space_format = f"{num}{currency}"
        before_no_space_format = f"{currency}{num}"

        if single_quantity == "YES":
            # update num
            num = np.random.choice(["en", 1])

        if placement == 'both':
            placement = np.random.choice(["before", "after"])        

        # if placement is before/after and number is int 
        if placement == "before" and isinstance(num, int):
            formatted_num = np.random.choice([before_format, before_no_space_format])
        
        elif placement == "after" and isinstance(num, int):
            formatted_num = np.random.choice([after_format, after_no_space_format])

        if isinstance(num, str):
            # replace string invalid currency with random currency
            if currency in string_invalid_currencies:
                # filter out invalid currencies
                df_filtered = df[~df["entity"].isin(string_invalid_currencies)]
                currency = np.random.choice(df_filtered["entity"])
            formatted_num = after_format

        # append to list of formatted numbers
        formatted_numbers.append(formatted_num)

    return formatted_numbers

def main():
    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "data"

    # load data
    formatted_numbers = money(data_path)

    print(formatted_numbers)

if __name__ == "__main__":
    main()