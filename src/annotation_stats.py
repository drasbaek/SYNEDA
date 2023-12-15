import pathlib
import pandas as pd


def main():
    # set paths
    path = pathlib.Path(__file__)
    data_path = path.parents[1] / "dbase" / "annotations" / "annotations_w_generations.xlsx"
    outpath = path.parents[1] / "dbase" / "annotations"

    # load data
    ents = pd.read_excel(data_path, sheet_name="ENTS")
    no_ents = pd.read_excel(data_path, sheet_name="NO ENTS")

    # merge data
    data = pd.concat([ents, no_ents], ignore_index=True)

    # calculate how many were changed (based on NaN vs not NaN)
    changed = (sum(data["changed?"].notna()) / len(data)) * 100

    print("Percentage of annotations changed:", round(changed, 1), "%")

    # group all "type" annotations that have a plus in them together as "multiple"
    data["type"] = data["type"].replace(to_replace=r".*\+.*", value="multiple", regex=True)

    # count how many of each "type" there is
    error_types = data["type"].value_counts()

    # save to file
    error_types.to_csv(outpath / "generation_entity_errors.csv")




if __name__ == "__main__":
    main()