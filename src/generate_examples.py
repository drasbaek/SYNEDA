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


def shuffle_df(df):
    '''
    Shuffle a df, but ensure that two of the same "MULTIPLE" type are not next to each other.
    '''
    while True:
        # Shuffle df
        df = df.sample(frac=1).reset_index(drop=True)

        # Get indices of MULTIPLE
        multiple_indices = df[df["TYPE"] == "MULTIPLE"].index

        # Check if any of the MULTIPLE indices are next to each other
        if all(multiple_indices[i+1] - multiple_indices[i] != 1 for i in range(len(multiple_indices)-1)):
            return df
        else:
            print("Shuffling again ...")


def fix_multiples(df_subset, multiple):
    '''
    Fix multiples by replacing the multiple with the two entities. E.g., "Dan Jørgensen (S)" -> "Dan Jørgensen" and "(S)".
    '''
    # get multiple
    df_subset_multiple = df_subset[df_subset["TYPE"] == "MULTIPLE"].iloc[0]

    # get index of df_subset_multiple in multiple
    index = multiple[multiple["entity"] == df_subset_multiple["entity"]].index[0]

    # get the first and second entity in the multiple
    entity_1 = multiple.iloc[index]["entity_1"]
    entity_2 = multiple.iloc[index]["entity_2"]

    # get the types
    type_1 = multiple.iloc[index]["type_1"]
    type_2 = multiple.iloc[index]["type_2"]

    context = multiple.iloc[index]["context"]

    # replace the multiple with the two entities
    df_subset = df_subset[df_subset["TYPE"] != "MULTIPLE"]
    row_1 = {"entity": entity_1, "TYPE": type_1, "context": context}
    row_2 = {"entity": entity_2, "TYPE": type_2, "context": context}

    # concat new rows to df_subset
    df_subset = pd.concat([df_subset, pd.DataFrame([row_1, row_2])], ignore_index=True)   

    return df_subset

def create_examples(df_all, multiple): 
    # initialize list of examples
    examples = []

    # shuffle all rows in df_all
    df_all = shuffle_df(df_all)

    print("Creating examples ...")
    while len(df_all) != 0:
        # sample number of entities
        n_entities = sample_number()
        
        # check if we have enough entities left in df_all
        if n_entities > len(df_all):
            n_entities = len(df_all)
        
        # subset df_all to only include n_entities
        df_subset = df_all.sample(n_entities, replace=False)

        # drop subsetted entities from all df 
        df_all = df_all.drop(df_subset.index)

        # check if any of our entities are multiples
        if "MULTIPLE" in df_subset["TYPE"].values:
            df_subset = fix_multiples(df_subset, multiple)

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

def write_to_csv(examples, data_path):
    '''
    Write examples to csv file.
    '''
    # write to csv file - each example is a row
    df = pd.DataFrame({"entities": examples})
    print(df)

    df.to_csv(data_path / "NER_EXAMPLES.csv", index=True)

    print("Done writing to csv file.")
    
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

    # create examples
    examples = create_examples(df, multiple)

    write_to_csv(examples, data_path)

if __name__ == "__main__":
    main()