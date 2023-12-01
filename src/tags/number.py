'''
Generate number lists

NB. Note that it can both be numbers (e.g., 1-100) and words (e.g., en-ti)
'''
import pathlib
import pandas as pd

def load_number_type(data_path, entity_type="MONEY"):
    df = pd.read_excel(data_path / "LISTS.xlsx", sheet_name=entity_type)

    return df

def load_data(data_path, entity_types=["EVENT", "FACILITY", "GPE", "LANGUAGE", "LAW", "LOCATION", "MONEY", "NORP", "ORDINAL", "ORGANIZATION", "PRODUCT", "QUANTITY", "TIME", "WORK OF ART"]):
    # initialize df for all entities
    df_all = pd.DataFrame()

    # load data for all entities
    for type in entity_types:
        df = pd.read_excel(data_path / "LISTS.xlsx", sheet_name=type)
        df["TYPE"] = type
        df_all = pd.concat([df_all, df], ignore_index=True)

    return df_all

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


def money(currencies:list): 
    '''
    Generate money with different currencies from list. 
    
    (Note that we need to account for all kinds of weird formatting e.g., 1,000.00 kr and 200DKK, 200 DKK, 200 kr. 200kr.)
    '''
    pass


def main():
    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "data"

    # load data
    df = load_data(data_path, entity_types=["MONEY"])

    print(df)

if __name__ == "__main__":
    main()