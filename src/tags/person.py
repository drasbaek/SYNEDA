'''
Script to create the PERSON entity tags for the training data.
'''
import pathlib
import pandas as pd
import numpy as np
import string
import random

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

    # remove row containing "000" as name
    df = df.loc[df["name"] != "000"]

    # copy df
    new_df = df.copy()

    # capitalize the names (but if it is a hyphenated name, capitalize both parts)
    new_df["name"] = new_df["name"].str.title()

    return new_df

def sample_person_tags(person_df:pd.DataFrame, n_names_total:int=200, high:int=2000, low:int=10, ratio:tuple=(0.75, 0.25), verbose=True):
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
    common_names = common_names.sample(int(round(n_names_total*ratio[0], 0)), replace=False)
    rare_names = rare_names.sample(int(round(n_names_total*ratio[1], 0)), replace=False)

    # info 
    info_after = f"Length of pools AFTER sampling:\nCommon names: {len(common_names)}, Rare names: {len(rare_names)}"

    # combine the two dfs
    sampled_names = pd.concat([common_names, rare_names])

    # sort by amount
    sampled_names = sampled_names.sort_values(by="amount", ascending=False).reset_index(drop=True)

    # print info
    if verbose:
        print("\n--------- INFORMATION ABOUT SAMPLING --------- \n")
        print(info_before)
        print("\n")
        print(info_after)
        print("\n")

    return sampled_names

def load_persons(data_path, df_names: list=["first_names_women_2023.txt", "first_names_men_2023.txt", "last_names_2023.txt"]): 
    '''
    Pipeline for loading and preprocessing the three lists of names.

    Args:
        data_path: path to the data folder with the three "normal" persons lists
    '''
    # load the three lists
    dfs = [txt_to_df(data_path / name) for name in df_names]

    # preprocess the dfs, but do it differently for the last names
    women_df, men_df = [preprocess_person_df(df, remove_first_two_rows=True) for df in dfs[:2]]
    last_names_df = preprocess_person_df(dfs[2], remove_first_two_rows=False)

    return men_df, women_df, last_names_df

def sample_persons(men_df, women_df, last_names_df):
    '''
    Sample persons from the three lists.
    '''
    # first names
    n_men_names = 250
    n_women_names = 250
    
    # last names
    n_last_names = 500
    
    # sample first names
    sampled_men_df = sample_person_tags(men_df, n_names_total=n_men_names, high=1000, low=200, ratio=(0.75, 0.25))
    sampled_women_df = sample_person_tags(women_df, n_names_total=n_women_names, high=1000, low=200, ratio=(0.75, 0.25))
    
    # sample last names
    sampled_last_names_df = sample_person_tags(last_names_df, n_names_total=n_last_names, high=1000, low=100, ratio=(0.75, 0.25))

    # lists of sampled names
    name_lists = []

    # make into lists instead of dfs
    for df in [sampled_men_df, sampled_women_df, sampled_last_names_df]:
        names = df["name"].tolist()
        name_lists.append(names)

    # unpack lists
    sampled_men, sampled_women, sampled_last_names = name_lists 

    return sampled_men, sampled_women, sampled_last_names

def get_first_names(sampled_men, sampled_women, n_entities=100):
    '''
    Obtain entites that consist of just a first name
    '''

    # sample 50 entities from each list
    men_first_names = np.random.choice(sampled_men, size=n_entities//2, replace=False)
    women_first_names = np.random.choice(sampled_women, size=n_entities//2, replace=False)

    # obtain all names that have not been sampled
    sampled_men_remaining = [name for name in sampled_men if name not in men_first_names]
    sampled_women_remaining = [name for name in sampled_women if name not in women_first_names]

    # combine the two lists
    first_names = list(men_first_names) + list(women_first_names)

    return first_names, sampled_men_remaining, sampled_women_remaining

def get_last_names(sampled_last_names, n_entities=25):
    '''
    Obtain entities that consist of just a last name
    '''

    # sample 50 entities from each list
    last_names = np.random.choice(sampled_last_names, size=n_entities, replace=False)

    # obtain all names that have not been sampled
    sampled_last_names_remaining = [name for name in sampled_last_names if name not in last_names]

    return last_names, sampled_last_names_remaining

def get_first_and_last_names(sampled_men, sampled_women, sampled_last_names, n_entities=100): 
    '''
    Obtain entities that consist of a first and last name
    '''
    # sample 50 entities from each gender
    men_first_names = np.random.choice(sampled_men, size=n_entities//2, replace=False)
    women_first_names = np.random.choice(sampled_women, size=n_entities//2, replace=False)

    # sample 100 last names
    last_names = np.random.choice(sampled_last_names, size=n_entities, replace=False)

    # obtain all names that have not been sampled
    sampled_men_remaining = [name for name in sampled_men if name not in men_first_names]
    sampled_women_remaining = [name for name in sampled_women if name not in women_first_names]
    sampled_last_names_remaining = [name for name in sampled_last_names if name not in last_names]

    # combine the two lists
    first_names = list(men_first_names) + list(women_first_names)

    first_last_names = []

    # combine the two ents into one 
    for first_name, last_name in zip(first_names, last_names):
        first_last_names.append(first_name + " " + last_name)

    return first_last_names, sampled_men_remaining, sampled_women_remaining, sampled_last_names_remaining


def get_double_first_name(sampled_men, sampled_women, n_entities=26):
    '''
    Obtain entities that consist of a double first name
    '''
    # sample 26 ents from each gender
    men_first_names = np.random.choice(sampled_men, size=n_entities, replace=False)
    women_first_names = np.random.choice(sampled_women, size=n_entities, replace=False)

    # obtain all names that have not been sampled
    sampled_men_remaining = [name for name in sampled_men if name not in men_first_names]
    sampled_women_remaining = [name for name in sampled_women if name not in women_first_names]

    # add two first names together (seperately for each gender)
    men_double = [men_first_names[i] + " " + men_first_names[i + 1] for i in range(0, len(men_first_names), 2) if i + 1 < len(men_first_names)]
    women_double = [women_first_names[i] + " " + women_first_names[i + 1] for i in range(0, len(women_first_names), 2) if i + 1 < len(women_first_names)]

    # combine 
    double_first_names = list(men_double) + list(women_double)
    
    return double_first_names, sampled_men_remaining, sampled_women_remaining

def get_first_name_initial(sampled_men, sampled_women, n_entities=26):
    '''
    Obtain entities that consist of a first name and an initial
    '''
    # sample 13 ents from each gender
    men_first_names = np.random.choice(sampled_men, size=n_entities//2, replace=False)
    women_first_names = np.random.choice(sampled_women, size=n_entities//2, replace=False)

    # combine the two lists
    first_names = list(men_first_names) + list(women_first_names)

    # obtain all names that have not been sampled
    sampled_men_remaining = [name for name in sampled_men if name not in men_first_names]
    sampled_women_remaining = [name for name in sampled_women if name not in women_first_names]
    
    # create a list of uppercase letters
    uppercase_letters = list(string.ascii_uppercase)

    # sample 26 initials
    initials = np.random.choice(uppercase_letters, size=n_entities, replace=False)

    # add a dot at the end of each initial
    initials = [initial + "." for initial in initials]

    # combine the two lists
    first_name_initial = []
    
    for first_name, initial in zip(first_names, initials):
        first_name_initial.append(first_name + " " + initial)
    
    return first_name_initial, sampled_men_remaining, sampled_women_remaining
    
    
def get_double_last_name(sampled_men, sampled_women, sampled_last_names, n_entities=76): 
    '''
    Obtain entities that consist of a first and double last_name
    '''
    # sample 38 ents from each gender
    men_first_names = np.random.choice(sampled_men, size=n_entities//2, replace=False)
    women_first_names = np.random.choice(sampled_women, size=n_entities//2, replace=False)

    # sample 76 last names
    last_names = np.random.choice(sampled_last_names, size=n_entities*2, replace=False)

    # obtain all names that have not been sampled
    sampled_men_remaining = [name for name in sampled_men if name not in men_first_names]
    sampled_women_remaining = [name for name in sampled_women if name not in women_first_names]
    sampled_last_names_remaining = [name for name in sampled_last_names if name not in last_names]
    
    # put two last names together
    last_double = [last_names[i] + " " + last_names[i + 1] for i in range(0, len(last_names), 2) if i + 1 < len(last_names)]

    # combine the two lists
    first_names = list(men_first_names) + list(women_first_names)

    first_double_last_names = []

    # combine the two ents into one 
    for first_name, last_name in zip(first_names, last_double):
        first_double_last_names.append(first_name + " " + last_name)

    return first_double_last_names, sampled_men_remaining, sampled_women_remaining, sampled_last_names_remaining


def get_first_name_initial_last(sampled_men, sampled_women, sampled_last_names, n_entities=50):
    '''
    Obtain entities consisting of a first name + initial + last name
    '''

    # sample 50 entities from both first names and last names
    men_first_names = np.random.choice(sampled_men, size=n_entities//2, replace=False)
    women_first_names = np.random.choice(sampled_women, size=n_entities//2, replace=False)
    last_names = np.random.choice(sampled_last_names, size=n_entities, replace=False)

    # obtain all names that have not been sampled
    sampled_men_remaining = [name for name in sampled_men if name not in men_first_names]
    sampled_women_remaining = [name for name in sampled_women if name not in women_first_names]
    sampled_last_names_remaining = [name for name in sampled_last_names if name not in last_names]

    # combine the two lists
    first_names = list(men_first_names) + list(women_first_names)

    # create a list of uppercase letters
    uppercase_letters = list(string.ascii_uppercase)

    # sample 26 initials
    initials = np.random.choice(uppercase_letters, size=n_entities, replace=True)

    # add a dot at the end of each initial
    initials = [initial + "." for initial in initials]

    # combine the three lists
    first_name_initial_last = []

    for first_name, initial, last_name in zip(first_names, initials, last_names):
        first_name_initial_last.append(first_name + " " + initial + " " + last_name)

    return first_name_initial_last, sampled_men_remaining, sampled_women_remaining, sampled_last_names_remaining


def main():
    # set seed
    np.random.seed(1209)

    path = pathlib.Path(__file__)
    names_path = path.parents[2] / "lists" / "names" 

    # load the three lists
    men_df, women_df, last_names_df = load_persons(names_path)

    # sample persons
    sampled_men, sampled_women, sampled_last_names = sample_persons(men_df, women_df, last_names_df)

    # sample first names
    first_names, sampled_men_remaining, sampled_women_remaining = get_first_names(sampled_men, sampled_women)

    # sample last names
    last_names, sampled_last_names_remaining = get_last_names(sampled_last_names)

    # sample first + last names
    first_last_names, sampled_men_remaining, sampled_women_remaining, sampled_last_names_remaining = get_first_and_last_names(sampled_men_remaining, sampled_women_remaining, sampled_last_names_remaining)

    # sample first + first names
    double_first_names, sampled_men_remaining, sampled_women_remaining = get_double_first_name(sampled_men_remaining, sampled_women_remaining)

    # sample first + initial
    first_name_initial, sampled_men_remaining, sampled_women_remaining = get_first_name_initial(sampled_men_remaining, sampled_women_remaining)

    # sample first + last + last
    double_last_names, sampled_men_remaining, sampled_women_remaining, sampled_last_names_remaining = get_double_last_name(sampled_men_remaining, sampled_women_remaining, sampled_last_names)
    
    # sample first + initial + last
    first_name_initial_last, sampled_men_remaining, sampled_women_remaining, sampled_last_names_remaining = get_first_name_initial_last(sampled_men_remaining, sampled_women_remaining, sampled_last_names_remaining)
    
    # combine all lists
    all_names = []

    for lst in [first_names, last_names, first_last_names, double_first_names, double_last_names, first_name_initial, first_name_initial_last]:
        all_names.extend(lst)

    # load famous names
    data_path = path.parents[2] / "data"
    famous_names = pd.read_excel(data_path / "CLEAN_LISTS.xlsx", sheet_name="PERSON")

    # combine the two lists
    all_names.extend(famous_names["entity"].tolist())

    # make all names into a dataframe
    df = pd.DataFrame(all_names, columns=["entity"])

    # add weights and context col (to match other lists)
    df["weight"] = 1
    df["context"] = None

    # save to file
    df.to_csv(data_path / "PERSON.csv", index=False)


if __name__ == '__main__':
    main()