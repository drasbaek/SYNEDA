'''
Script to create the PERSON entity tags for the training data.
'''
import pathlib
import pandas as pd
import numpy as np

# create the tags for the PERSON entity
def txt_to_df(path: pathlib.Path):
    '''
    Load a txt file into a dataframe
    '''

    df = pd.read_fwf(path, encoding="latin-1", header=None, sep = "\t")

    # split the data into columns
    df = df[0].str.split('\t', expand=True)

    return df

def preprocess_person_df(df:pd.DataFrame, remove_first_two_rows:bool=True):
    '''
    Preprocess the person df from txt file. 
    Optionally remove the first two rows (first name dataframes have two rows of metadata which the last name dataframe does not have).

    Args
        df: dataframe with names and amount of times they appear
        remove_first_two_rows: whether to remove the first two rows or not

    Returns
        new_df: preprocessed dataframe with capitalized names and colnames in English
    '''

    # remove first two row 
    df = df.iloc[2:]

    # rename the columns
    df.columns = ["name", "amount"]

    # make amount column numeric
    df["amount"] = pd.to_numeric(df["amount"])

    # copy df
    new_df = df.copy()

    # capitalize the names
    new_df["name"] = new_df["name"].str.capitalize()

    return new_df

def sample_person_tags(person_df:pd.DataFrame, n_names_total:int=200, high:int=2000, low:int=10, ratio:tuple=(0.75, 0.25)):
    '''
    Sample PERSON tags from the list of names. Account for the amount of times the name appears in df (sampling more frequent names more often).

    Args
        person_df: dataframe with names and amount of times they appear
        n_names_total: total number of names to sample (common + rare)
        high: upper bound for amount of times a name has to appear to be considered common
        low: lower bound for amount of times a name has to appear to be considered rare
        ratio: ratio of common names to rare names (common, rare). Values must sum to 1.
    
    Returns
        sampled_names: dataframe with sampled names
        info_before, info_after: info about the length of the pools before and after sampling
    '''

    # raise value error if ratio does not sum to 1
    if sum(ratio) != 1:
        raise ValueError("Ratio must sum to 1")

    # sample names
    common_names = person_df.loc[person_df["amount"] >= high]
    rare_names = person_df.loc[(person_df["amount"] < high) & (person_df["amount"] > low)] 

    # info 
    info_before = f"Length of pools BEFORE sampling:\nCommon names: {len(common_names)}, Rare names: {len(rare_names)}"

    # sample names from both pools 
    common_names = common_names.sample(int(n_names_total*ratio[0]), replace=False)
    rare_names = rare_names.sample(int(n_names_total*ratio[1]), replace=False)

    # info 
    info_after = f"Length of pools AFTER sampling:\nCommon names: {len(common_names)}, Rare names: {len(rare_names)}"

    # combine the two dfs
    sampled_names = pd.concat([common_names, rare_names])

    # sort by amount
    sampled_names = sampled_names.sort_values(by="amount", ascending=False).reset_index(drop=True)

    return sampled_names, info_before, info_after

def all_normal_persons(data_path, df_names: list=["first_names_women_2023.txt", "first_names_men_2023.txt", "last_names_2023.txt"]): 
    '''
    Pipeline for loading and preprocessing all the normal persons lists

    Args:
        data_path: path to the data folder with the three "normal" persons lists
    '''
    # load the three lists
    dfs = [txt_to_df(data_path / name) for name in df_names]

    # preprocess the dfs, but do it differently for the last names
    women_df, men_df = [preprocess_person_df(df, remove_first_two_rows=True) for df in dfs[:2]]
    last_names = preprocess_person_df(dfs[2], remove_first_two_rows=False)

    return men_df, women_df, last_names

def check_for_duplicates(dfs):
    '''
    Check for duplicates between the three name lists
    '''
    pass

def main():
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "lists" / "names" 

    # load the three lists
    men_df, women_df, last_names = all_normal_persons(data_path)

    # sample names
    men_df, info_before, info_after = sample_person_tags(men_df, n_names_total=200, high=2000, low=100, ratio=(0.75, 0.25))

    # print all names where amount is 1
    print(men_df)
    
    # print info
    print("\n--------- INFORMATION ABOUT SAMPLING --------- \n")
    print(info_before)
    print("\n")
    print(info_after)

if __name__ == '__main__':
    main()