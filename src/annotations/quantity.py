'''
Create quantity ents from list of currencies and numbers.
'''

import pandas as pd
import numpy as np
import pathlib

from utils import number_words

def quantity(data_path):
    '''
    Generate quantities with different units 
    '''
    # load data
    df = pd.read_excel(data_path / "MANUAL_LISTS.xlsx", sheet_name="QUANTITY")

    # generate random numbers (100)
    small_numbers = np.random.randint(1, 350, size=150)
    big_numbers = np.random.randint(1000, 10000, size=25)
    numbers_words = number_words()

    all_numbers = np.concatenate([small_numbers, big_numbers, numbers_words])

    # duplicate entities based on weight
    df = df.loc[df.index.repeat(df["weight"])].reset_index(drop=True)

    formatted_quantities = []

    for _, row in df.iterrows():
        # extract values
        quantity = row["entity"]

        # get num
        num = np.random.choice(all_numbers)

        # ensure space if num is a word
        if num in numbers_words:
            num = f"{num} "
        
        # give a 80% probability adding a space at the end of a number
        else:
            if np.random.rand() > 0.2:
                num = f"{num} "
        
        # concatenate quantity and num
        formatted_quantity = f"{num}{quantity}"
        
        # append to list
        formatted_quantities.append(formatted_quantity)

    return formatted_quantities

def main():
    # set seed
    np.random.seed(1209)

    # define paths 
    path = pathlib.Path(__file__)
    ents_path = path.parents[2] / "dbase" / "entities_lists"

    formatted_quantities = quantity(ents_path)

    # save to file
    df = pd.DataFrame(formatted_quantities, columns=["entity"])

    # add weights and context col (to match other lists)
    df["weight"] = 1
    df["context"] = None

    # save to file
    df.to_csv(ents_path / "QUANTITY.csv", index=False)

if __name__ == "__main__":
    main()