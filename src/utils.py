import pathlib
import pandas as pd

def load_data(data_path, entity_types=["EVENT", "FACILITY", "GPE", "LANGUAGE", "LAW", "LOCATION", "MONEY", "NORP", "ORDINAL", "ORGANIZATION", "PRODUCT", "QUANTITY", "TIME", "WORK OF ART"]):
    # initialize df for all entities
    df_all = pd.DataFrame()

    # load data for all entities
    for type in entity_types:
        df = pd.read_excel(data_path / "LISTS.xlsx", sheet_name=type)
        df["TYPE"] = type
        df_all = pd.concat([df_all, df], ignore_index=True)

    return df_all
