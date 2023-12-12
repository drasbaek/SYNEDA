'''
Script to fetch external data 

Heavily inspired by 
https://github.com/centre-for-humanities-computing/DaCy/blob/main/training/ner_fine_grained/fetch_assets.py 
'''

import spacy
from datasets import load_dataset
from spacy.tokens import Doc, DocBin
import pathlib
from check_data import check_dane

def fetch_dansk():
    try:
        datasets = load_dataset("chcaa/DANSK")
    except FileNotFoundError:
        raise FileNotFoundError(
            "DANSK is not available. Check that HuggingFace is up and running, and that the dataset has been publically released.",
        )
    
    nlp = spacy.blank("da")
    partitions = ["train", "dev", "test"]

    path = pathlib.Path(__file__)

    corpus_path = path.parents[2] / "external_data"
    corpus_path.mkdir(parents=True, exist_ok=True)

    for p in partitions:
        db = DocBin()
        for doc in [
            Doc(nlp.vocab).from_json(dataset_row) for dataset_row in datasets[f"{p}"]
        ]:
            db.add(doc)
        
        # save DANSK
        db.to_disk(corpus_path / f"DANSK_{p}.spacy")

def fix_dane(dataset):
    '''
    Remove all sentences that have old, ambigious labels PER, ORG, LOC, MISC as entities
    '''
    # define labels to remove
    labels_to_remove = ["PER", "ORG", "LOC", "MISC"]

    # convert to pandas dataframe
    df = dataset.to_pandas()

    # loop through all rows
    for i, row in df.iterrows():
        # get ents
        ents = row['ents']

        for ent in ents: 
            # get label
             label = ent['label']

             # rename 
             if label == "WORK_OF_ART": 
                ent["label"] = "WORK OF ART"

        # loop through all ents
        for ent in ents:
            # get label
            label = ent['label']

            # remove entire row if label is in labels_to_remove
            if label in labels_to_remove:
                df.drop(i, inplace=True)
                break

    # convert back to dataset
    dataset = dataset.from_pandas(df)

    return dataset

def fetch_dane(): 
    try:
        datasets = load_dataset("KennethEnevoldsen/dane_plus")
    except FileNotFoundError:
        raise FileNotFoundError(
            "Dane_Plus is not available. Check that HuggingFace is up and running, and that the dataset has been publically released.",
        )

    path = pathlib.Path(__file__)

    corpus_path = path.parents[2] / "external_data"
    corpus_path.mkdir(parents=True, exist_ok=True)

    nlp = spacy.blank("da")
    partitions = ["train", "dev", "test"]

    # use fix_dane 
    for p in partitions:
        datasets[f"{p}"] = fix_dane(datasets[f"{p}"])

    # check fix_dane on test dataset
    labels = check_dane(datasets)
    print(labels)

    # create DocBin 
    for p in partitions:
        db = DocBin()
        for doc in [
            Doc(nlp.vocab).from_json(dataset_row) for dataset_row in datasets[f"{p}"]
        ]:
            db.add(doc)
        
        # save DANE
        db.to_disk(corpus_path / f"DANE_{p}.spacy")

if __name__ == "__main__":
    fetch_dansk()
    fetch_dane()