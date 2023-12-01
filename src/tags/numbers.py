'''
Generate number lists

NB. Note that it can both be numbers (e.g., 1-100) and words (e.g., en-ti)
'''
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parents[2] / "src"))
from utils import load_data

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
    data_path = path.parents[1] / "data"

    # load data
    df = load_data(data_path, entity_types=["MONEY"])

    print(df)

if __name__ == "__main__":
    main()