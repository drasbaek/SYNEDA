import pathlib
import pandas as pd
import sys
from spacy.tokens import DocBin
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sys.path.append(str(pathlib.Path(__file__).parents[1]))
from external_data.fetch_data import fetch_dansk, fix_dane, fetch_dane


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


def get_SYNEDA_sentence_lens(annotations_path):
    # create nlp object
    nlp = spacy.blank("da")

    # load syneda
    syneda = pd.read_csv(annotations_path / "annotations_w_generations_spanned.csv")

    # get text column into a list
    text = syneda["text"].tolist()

    # for each element, calculate word count with spacy
    sentence_lengths = [len(nlp(text[i])) for i in range(len(text))]

    return sentence_lengths


def get_DANSK_DANE_sentence_lens(data_path):
    # create nlp object
    nlp = spacy.blank("da")

    # ensure that DANSK and DANE are fetched
    fetch_dansk(save_path=data_path, partitions=["train", "dev", "test"])
    fetch_dane(save_path=data_path, partitions=["train", "dev", "test"], fix_dane=False)

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

    return dansk_lengths, dane_lengths


def plot_sentence_lengths(syneda_lengths, dansk_lengths, dane_lengths, plot_path):
    # define custom params
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    
    # set theme
    sns.set_theme(style="white", rc=custom_params)

    # set font to times
    plt.rcParams["font.family"] = "Times New Roman"

    # create figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # create density plot for SYNEDA
    sns.kdeplot(data=syneda_lengths, ax=ax, fill=True, label="SYNEDA", color="#65BBF3")

    # create density plot for DANSK
    sns.kdeplot(data=dansk_lengths, ax=ax, fill=True, label="DANSK", color="#F36965")

    # create density plot for DANE
    sns.kdeplot(data=dane_lengths, ax=ax, fill=True, label="DaNE+", color="#9966FF")

    # set x-axis label
    ax.set_xlabel("Text length (tokens)", fontsize=16, labelpad=10)

    # set y-axis label
    ax.set_ylabel("Density", fontsize=16, labelpad=10)

    # set legend
    ax.legend(fontsize=16, loc="upper right")

    # truncate x-axis
    ax.set_xlim(0, 60)

    # save plot to directory (create if it doesn't exist)
    plot_path.mkdir(parents=True, exist_ok=True)

    # save plot to a high DPI
    plt.savefig(plot_path / "sentence_lengths.png", dpi=500)


def main():
    # set paths
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "data"
    annoations_path = path.parents[2] / "dbase" / "annotations"
    outpath = path.parents[2] / "dbase" / "annotations"
    plot_path = path.parents[2] / "plots"

    annotation_errors(annoations_path, outpath)

    # get sentence lengths
    dansk_lengths, dane_lengths = get_DANSK_DANE_sentence_lens(data_path)
    syneda_lengths = get_SYNEDA_sentence_lens(annoations_path)

    # plot sentence lengths
    plot_sentence_lengths(syneda_lengths, dansk_lengths, dane_lengths, plot_path)

if __name__ == "__main__":
    main()