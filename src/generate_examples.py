import pathlib
import pandas as pd
import numpy as np
import random

def load_data(data_path):
    # complete entities
    coded_entity_types = ["DATE", "MONEY", "PERCENT", "QUANTITY", "PERSON"]

    # manual entities
    manual_entity_types = ["EVENT", "FACILITY", "GPE", "LANGUAGE", "LAW", "LOCATION", "NORP", "ORDINAL", "ORGANIZATION", "PRODUCT", "TIME", "WORK OF ART", "CARDINAL"]

    # initialize df for all entities
    df_all = pd.DataFrame()
    
    # load data for entities that are manual (not coded)
    for ent_type in manual_entity_types:
        df = pd.read_excel(data_path / "CLEAN_LISTS.xlsx", sheet_name=ent_type)
        df["TYPE"] = ent_type
        df_all = pd.concat([df_all, df], ignore_index=True)
    
    # load data for entities that are coded
    for ent_type in coded_entity_types:
        df = pd.read_csv(data_path / f"{ent_type}.csv")
        df["TYPE"] = ent_type
        df_all = pd.concat([df_all, df], ignore_index=True)

    # load multiples
    multiple = pd.read_excel(data_path / "CLEAN_LISTS.xlsx", sheet_name="MULTIPLE")
    multiple["TYPE"] = "MULTIPLE"
    
    # add multiples to df_all but only the entity col 
    df_all = pd.concat([df_all, multiple[["entity", "weight", "context", "TYPE"]]], ignore_index=True)

    return df_all, multiple

def expand_data(df_all):
    """
    Expands data by multiplying rows by the weight of each entity.
    """
    
    # multiply rows by weight
    df_all = df_all.loc[df_all.index.repeat(df_all["weight"])].reset_index(drop=True)

    # drop weights
    df_all = df_all.drop(columns=["weight"])

    return df_all

def sample_number():
    # Define the probabilities for each number
    probabilities = np.array([0.5, 0.3, 0.15, 0.05])
    numbers = np.array([1, 2, 3, 4])

    # Use np.random.choice to sample based on the specified probabilities
    return np.random.choice(numbers, p=probabilities)

def create_examples(df_all, n_examples):
    """
    Creates lists of entity examples (such as: [WORK OF ART: "One Dance", EVENT: "Folketingsvalget 2019"]) to generate synthetic text from.

    Args:
        df_all (pd.DataFrame): Dataframe containing all entities.
        n_examples (int): Number of examples to create.
        n_entities (list): Range describing number of entities to include in each example
    
    Returns:
        examples (list): List of examples.
    """
    
    # initialize list of examples
    examples = []

    # shuffle all rows in df_all
    df_all = df_all.sample(frac=1, random_state=1209).reset_index(drop=True)

    # create examples
    for i in range(n_examples):
        # sample number of entities
        n_entities = sample_number()
        
        # subset df_all to only include n_entities
        df_subset = df_all.sample(n_entities, replace=False).reset_index(drop=True)

        # create example
        example = []
        for index, row in df_subset.iterrows():
            if row["context"] is np.nan:
                example.append(f"{row['TYPE']}: {row['entity']}")
            else:
                example.append(f"{row['TYPE']}: {row['entity']} {{{row['context']}}}")
    
        # append example to list of examples
        examples.append(example)

    return examples


def main():
    # set seed
    np.random.seed(1209)

    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[1] / "data"

    # load data
    df, multiple = load_data(data_path)

    # multiply rows by weight
    df = expand_data(df)

    # save df to check 
    df.to_csv(data_path / "test.csv", index=False)

    # create examples
    examples = create_examples(df, n_examples=50)

    for i, example in enumerate(examples):
        print(f"{i+1}. {example}")

if __name__ == "__main__":
    main()