'''
Create money tags from list of currencies and numbers.
'''

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
    small_numbers = np.random.randint(1, 350, size=100)
    big_numbers = np.random.randint(1000, 10000, size=50)
    numbers_words = number_words()

    # combine numbers and words
    all_numbers = np.concatenate([small_numbers, big_numbers, numbers_words])
    numeric_numbers = np.concatenate([small_numbers, big_numbers])

    # duplicate entities based on weight
    df = df.loc[df.index.repeat(df["weight"])].reset_index(drop=True)

    formatted_numbers = []

    for i, row in df.iterrows():
        # extract values 
        currency = row["entity"]
        currency_placement = row["placement"]
        single_quantity = row["only_single_quantity"]
        number_word = row["number_word"]

        # check if single quantity is YES, update number
        if single_quantity == "YES":
            num = np.random.choice(["en", 1])
            formatted_num = f"{num} {currency}"

        elif number_word == "NO" and single_quantity == "NO":
            num = np.random.choice(numeric_numbers)
            if currency_placement == "both":
                currency_placement = np.random.choice(["before", "after"])
                if currency_placement == "after":
                    formatted_num = np.random.choice([f"{num} {currency}", f"{num}{currency}"])
    
                elif currency_placement == "before":
                    formatted_num = np.random.choice([f"{currency} {num}", f"{currency}{num}"]) 

        else:
            if currency_placement == "after":
                num = np.random.choice(all_numbers)
                if num in numbers_words:
                    formatted_num = f"{num} {currency}"
                else: 
                    formatted_num = np.random.choice([f"{num} {currency}", f"{num}{currency}"])

            if currency_placement == "both": # if placement is both, update placement to before or after based on random choice
                currency_placement = np.random.choice(["before", "after"])

                if currency_placement == "after":
                    num = np.random.choice(all_numbers)
                    if num in numbers_words:
                        formatted_num = f"{num} {currency}"
                    else: 
                        formatted_num = np.random.choice([f"{num} {currency}", f"{num}{currency}"])

                elif currency_placement == "before":
                    num = np.random.choice(numeric_numbers)
                    formatted_num = np.random.choice([f"{currency} {num}", f"{currency}{num}"])

        # append to list of formatted numbers
        formatted_numbers.append(formatted_num)    
        
    return formatted_numbers

def main():
    # set seed
    np.random.seed(1209)

    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "data"

    # load data
    formatted_numbers = money(data_path)
    print(formatted_numbers)

    # save data
    df = pd.DataFrame(formatted_numbers, columns=["entity"])

    # add weights col and context col (to match other lists)
    df["weights"] = 1
    df["context"] = None

    # save to excel
    df.to_csv(data_path / "MONEY.csv", index=False) 

if __name__ == "__main__":
    main()