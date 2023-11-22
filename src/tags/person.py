'''
Script to create the PERSON entity tags for the training data.
'''
import pathlib
import pandas as pd

# create the tags for the PERSON entity
def txt_to_df(path):
    df = pd.read_fwf(path, encoding="latin-1", header=None, sep = "\t")

    # split the data into columns
    df = df[0].str.split('\t', expand=True)

    return df

def preprocess_person_df(df):
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

def sample_person_tags(person_df, n_names):
    '''
    Sample PERSON tags from the list of names. Account for the amount of times the name appears in df (sampling more frequent names more often).
    '''

    # sample name
    sampled_names = person_df.sample(n_names, weights="amount", replace=True, random_state=2502) #NB. find a better way to sample more frequent names more often!! 

    # save sampled names to a df, add a PERSON tag
    sampled_names["tag"] = "PERSON"

    return sampled_names

def main():
    path = pathlib.Path(__file__)
    filepath = path.parents[2] / "lists" / "names" / "first_names_women_2023.txt"
    print(filepath)

    # load, preprocess
    df = txt_to_df(filepath)
    df = preprocess_person_df(df)

    # sample names
    sampled_names = sample_person_tags(df, 500)


if __name__ == '__main__':
    main()