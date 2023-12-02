'''
Script to create the PERSON entity tags for the training data.
'''
import pathlib
import pandas as pd
import numpy as np

# create the tags for the PERSON entity
def txt_to_df(path):
    df = pd.read_fwf(path, encoding="latin-1", header=None, sep = "\t")

    # split the data into columns
    df = df[0].str.split('\t', expand=True)

    return df

def preprocess_person_df(df, remove_first_two_rows=True):
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

def all_normal_persons(data_path, df_names: list=["first_names_women_2023.txt", "first_names_men_2023.txt", "last_names_2023.txt"]): 
    '''
    Pipeline for loading and preprocessing all the normal persons lists

    Args:
        data_path (str): path to the data folder with the three normal persons lists
    '''
    # load the three lists
    dfs = [txt_to_df(data_path / name) for name in df_names]

    # preprocess the dfs, but do it differently for the last names
    men_df, women_df = [preprocess_person_df(df, remove_first_two_rows=True) for df in dfs[:2]]
    last_names = preprocess_person_df(dfs[2], remove_first_two_rows=False)

    return men_df, women_df, last_names

def sample_person_tags(person_df, n_names, frequency_cutoff=2500, ratio:tuple=(1, 0.25)):
    '''
    Sample PERSON tags from the list of names. Account for the amount of times the name appears in df (sampling more frequent names more often).
    '''
    # define the weights for sampling, based on the amount of times the name appears in the df
    weights = np.where(np.array(person_df["amount"]) >= frequency_cutoff, ratio[0], ratio[1])

    # sample name
    sampled_indicies = np.random.choice(len(person_df["name"]), n_names, p=weights / np.sum(weights))

    # extract sampled names from sampled indices
    sampled_names = [person_df["name"][i] for i in sampled_indicies]

    return sampled_names

def main():
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "lists" / "names" 

    # load the three lists
    men_df, women_df, last_names = all_normal_persons(data_path)

    # sample names
    sampled_names = sample_person_tags(men_df, 200)

    print(sampled_names)


if __name__ == '__main__':
    main()