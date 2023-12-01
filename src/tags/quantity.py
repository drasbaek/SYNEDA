'''
Create quantity ents from list of currencies and numbers.
'''

import pandas as pd
import numpy as np
import pathlib

def quantity(data_path):
    '''
    Generate quantities with different units 
    '''
    # load data
    df = pd.read_excel(data_path / "LISTS.xlsx", sheet_name="QUANTITY")

    print(df)

def main():
    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "data"

    quantity(data_path)

if __name__ == "__main__":
    main()