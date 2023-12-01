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

def main():
    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "data"

if __name__ == "__main__":
    main()