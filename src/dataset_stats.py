import pathlib
import pandas as pd
from external_data.fetch_data import fetch_dansk, fix_dane, fetch_dane
from spacy.tokens import DocBin
import spacy

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


def map_sentence_lengths(data_path):
    # create nlp object
    nlp = spacy.blank("da")
    nlp.add_pipe('sentencizer')

    # ensure that DANSK and DANE are fetched
    fetch_dansk(save_path=data_path, partitions=["train", "dev", "test"])
    fetch_dane(save_path=data_path, partitions=["train", "dev", "test"])

    # load data from spacy format
    dansk_train = DocBin().from_disk(data_path / "train" / "dansk_train.spacy")
    dansk_dev = DocBin().from_disk(data_path / "dev" / "dansk_dev.spacy")
    dansk_test = DocBin().from_disk(data_path / "test" / "dansk_test.spacy")

    dane_train = DocBin().from_disk(data_path / "train" / "dane_train.spacy")
    dane_dev = DocBin().from_disk(data_path / "dev" / "dane_dev.spacy")
    dane_test = DocBin().from_disk(data_path / "test" / "dane_test.spacy")

    # get all docs from DocBin for each dataset
    dansk_docs = list(dansk_train.get_docs(nlp.vocab)) + list(dansk_dev.get_docs(nlp.vocab)) + list(dansk_test.get_docs(nlp.vocab))
    dane_docs = list(dane_train.get_docs(nlp.vocab)) + list(dane_dev.get_docs(nlp.vocab)) + list(dane_test.get_docs(nlp.vocab))

    # get all sentences
    dansk_sentences = [sent for doc in dansk_docs for sent in doc.sents]
    dane_sentences = [sent for doc in dane_docs for sent in doc.sents]

    # get lengths
    dansk_lengths = [len(sent) for sent in dansk_sentences]
    dane_lengths = [len(sent) for sent in dane_sentences]

    # create an overlapping plot of the two datasets
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

    # set style
    sns.set_style("darkgrid")

    # create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # create histogram
    sns.histplot(data=dansk_lengths, bins=100, color="blue", label="DANSK", ax=ax)

    # create histogram
    sns.histplot(data=dane_lengths, bins=100, color="red", label="DANE", ax=ax)

    # set labels
    ax.set_xlabel("Sentence length")
    ax.set_ylabel("Count")

    # set title
    ax.set_title("Distribution of sentence lengths in DANSK and DANE")

    # set legend
    ax.legend()

    # show plot
    plt.show()





def main():
    # set paths
    path = pathlib.Path(__file__)
    data_path = path.parents[1] / "data"
    annoations_path = path.parents[1] / "dbase" / "annotations"
    outpath = path.parents[1] / "dbase" / "annotations"

    #annotation_errors(annoations_path, outpath)

    map_sentence_lengths(data_path)

if __name__ == "__main__":
    main()