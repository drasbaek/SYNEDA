import pathlib
import pandas as pd

def annotation_errors(annotations_path, outpath):
    # load data
    ents = pd.read_excel(annotations_path / "annotations_w_generations.xlsx", sheet_name="ENTS")
    no_ents = pd.read_excel(annotations_path / "annotations_w_generations.xlsx", sheet_name="NO ENTS")

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


def entity_distributions(annotations_path, outpath):
    # read spanned data
    spanned_data = pd.read_csv(annotations_path / "annotations_w_generations_spanned.csv")

    # all
    all_ents = []

    # iterate over ents column
    for index, row in spanned_data.iterrows():
        # split ents column by comma
        ents = row["ents"]

        # ensure that it is read as a list of dicts
        ents_dict_list = eval(ents)

        # iterate over ents
        for ent in ents_dict_list:
            # get label
            label = ent["label"]
            
            # append to all_ents
            all_ents.append(label)
    
    # count how many of each type
    all_ents = pd.Series(all_ents).value_counts()

    # add column with how many percent that is
    all_ents = pd.DataFrame(all_ents)

    # rename column
    all_ents = all_ents.rename(columns={0: "count"})

    # add column with percentage
    all_ents["percentage"] = round(((all_ents["count"] / sum(all_ents["count"])) * 100), 1)

    # set the index column as "type"
    all_ents = all_ents.reset_index()
    all_ents = all_ents.rename(columns={"index": "type"})

    # save to file
    all_ents.to_csv(outpath / "entity_distribution.csv")

    print(all_ents)


def main():
    # set paths
    path = pathlib.Path(__file__)
    annoations_path = path.parents[1] / "dbase" / "annotations"
    outpath = path.parents[1] / "dbase" / "annotations"

    annotation_errors(annoations_path, outpath)

if __name__ == "__main__":
    main()