import pathlib
import pandas as pd
import numpy as np

def load_data(data_path, entity_types=["EVENT", "FACILITY", "GPE", "LANGUAGE", "LAW", "LOCATION", "MONEY", "NORP", "ORDINAL", "ORGANIZATION", "PRODUCT", "QUANTITY", "TIME", "WORK OF ART"]):
    # initialize df for all entities
    df_all = pd.DataFrame()

    # load data for all entities
    for type in entity_types:
        df = pd.read_excel(data_path / "LISTS.xlsx", sheet_name=type)
        df["TYPE"] = type
        df_all = pd.concat([df_all, df], ignore_index=True)

    return df_all

def create_examples(df_all, n_examples, n_entities=[1,3]):
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

    # create examples
    for i in range(n_examples):
        # sample number of entities
        n = np.random.randint(n_entities[0], n_entities[1]+1)

        # sample entities
        entities = df_all.sample(n=n)

        # create example
        example = []
        for index, row in entities.iterrows():
            example.append(f"{row['TYPE']}: {row['entity']}")

        # append example to list of examples
        examples.append(example)

    return examples


def main():
    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[1] / "data"

    # load data
    df = load_data(data_path, entity_types=["EVENT", "FACILITY", "GPE", "LANGUAGE", "LAW", "LOCATION", "NORP", "ORDINAL", "ORGANIZATION", "PRODUCT", "TIME", "WORK OF ART"])

    # create examples
    examples = create_examples(df, n_examples=50, n_entities=[1,3])

    for i, example in enumerate(examples):
        print(f"{i+1}. {example}")

    

if __name__ == "__main__":
    main()