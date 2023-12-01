import pathlib
import pandas as pd
import numpy as np

def number_words(): 
    '''
    Create list of numbers in words (danish) from pre-defined list of small numbers and big numbers.
    '''

    small_numbers = [
        "to", "tre", "fire", "fem", "seks", "syv", "otte", "ni", "ti", "tolv", "tretten", "fjorten", "femten", "seksten", "sytten", "atten", "nitten",
        "tyve", "tredive", "fyrre", "halvtreds", "tres", "firs", "halvfems", "halvfems", "halvfjerds", "firs", "halvfems"
    ]

    big_numbers = ["hundrede", "tusinde", "millioner"]

    big_combined_nums = []

    for num in small_numbers: 
        for big_num in big_numbers: 
            big_combined_nums.append(f"{num} {big_num}")

    # sample 30 big nums 
    big_combined_numbers = np.random.choice(big_combined_nums, size=28)

    # combine with small nums 
    all_numbers = np.concatenate([small_numbers, big_combined_numbers])

    return all_numbers

def money(data_path): 
    '''
    Generate money with different currencies from list. 
    
    (Note that we need to account for all kinds of weird formatting e.g., 1,000.00 kr and 200DKK, 200 DKK, 200 kr. 200kr.)
    '''
    # read in data
    df = pd.read_excel(data_path / "CLEAN_LISTS.xlsx", sheet_name="MONEY")

    # generate random numbers (100)
    small_numbers = np.random.randint(1, 150, size=100)
    big_numbers = np.random.randint(1000, 10000, size=50)
    numbers_words = number_words()

    # combine numbers and words
    numbers = np.concatenate([small_numbers, big_numbers, numbers_words])

    # duplicate entities based on weight
    df = df.loc[df.index.repeat(df["weight"])].reset_index(drop=True)

    # define string invalid currencies, all currencies that have single quantiy as NO in df + ",-"
    string_invalid_currencies = df[df["only_single_quantity"] == "YES"]["entity"].tolist()
    string_invalid_currencies.extend([",-", "$", "€", "£"])

    # filter out invalid currencies
    df_string_valid =  df[~df["entity"].isin(string_invalid_currencies)]

    formatted_numbers = []

    for num in numbers: 
        # sample randomly from df with replacement
        currency = np.random.choice(df["entity"])

        # define accepted formats
        after_format = f"{num} {currency}"
        before_format = f"{currency} {num}"
        after_no_space_format = f"{num}{currency}"
        before_no_space_format = f"{currency}{num}"
        
        currency_idx = df[df["entity"] == currency].index[0]

        # extract placement and single quantity
        placement = df.loc[currency_idx, "placement"]
        single_quantity = df.loc[currency_idx, "only_single_quantity"]

        # check if single quantity is YES, update number
        if single_quantity == "YES":
            # update num
            num = np.random.choice(["en", 1])

        # if placement is both, update placement to before or after based on random choice 
        if placement == 'both':
            placement = np.random.choice(["before", "after"])   

        if num in numbers_words:
            if currency in string_invalid_currencies: # replace invalid currency with random valid currency
                currency = np.random.choice(df_string_valid["entity"])
                print(num, currency)
                
            formatted_num = after_format     

        # if num is int
        elif num not in numbers_words: 
            if placement == "before":
                formatted_num = np.random.choice([before_format, before_no_space_format])
            elif placement == "after":
                formatted_num = np.random.choice([after_format, after_no_space_format])

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