import pathlib
import pandas as pd


def main():
    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[1] / "data"

    # load entities
    ent_df = pd.read_csv(data_path / "final_ents" / "NER_ENTS_OVERVIEW.csv")

    # summarize count of each label and save to a variable
    ent_counts = ent_df["TYPE"].value_counts()

    # get the relative percentage of each label
    ent_perc = round(100*(ent_counts / ent_counts.sum()),1)

    # get only unique entities
    unique_ent_df = ent_df.drop_duplicates(subset=["entity"])

    # repeat the same process for unique entities
    unique_ent_counts = unique_ent_df["TYPE"].value_counts()
    unique_ent_perc = round(100*(unique_ent_counts / unique_ent_counts.sum()),1)

    # bind all the data together
    ent_summary = pd.concat([ent_counts, ent_perc, unique_ent_counts, unique_ent_perc], axis=1)
    
    # rename columns
    ent_summary.columns = ["Count", "Percentage", "Unique Count", "Unique Percentage"]

    print(ent_summary)


if __name__ == "__main__":
    main()