'''
Script to fetch external data (DANSK and DANE) and fix DANE. 

Heavily inspired by 
https://github.com/centre-for-humanities-computing/DaCy/blob/main/training/ner_fine_grained/fetch_assets.py 
'''

import spacy
from datasets import load_dataset
from spacy.tokens import Doc, DocBin
import pathlib

def fetch_dansk(save_path, partitions=["train", "dev", "test"]):
    try:
        datasets = load_dataset("chcaa/DANSK")
    except FileNotFoundError:
        raise FileNotFoundError(
            "DANSK is not available. Check that HuggingFace is up and running, and that the dataset has been publically released.",
        )
    
    nlp = spacy.blank("da")

    for p in partitions:
        db = DocBin()
        for doc in [
            Doc(nlp.vocab).from_json(dataset_row) for dataset_row in datasets[f"{p}"]
        ]:
            db.add(doc)
        
        # save DANSK
        db.to_disk(save_path / f"{p}" /  f"DANSK_{p}.spacy")

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

def fetch_dane(save_path, partitions=["train", "dev", "test"]): 
    try:
        datasets = load_dataset("KennethEnevoldsen/dane_plus")
    except FileNotFoundError:
        raise FileNotFoundError(
            "Dane+ is not available. Check that HuggingFace is up and running, and that the dataset has been publically released.",
        )

    path = pathlib.Path(__file__)

    corpus_path = path.parents[2] / "external_data"
    corpus_path.mkdir(parents=True, exist_ok=True)

    nlp = spacy.blank("da")

    # use fix_dane (rm old MISC, LOC labls)
    for p in partitions:
        datasets[f"{p}"] = fix_dane(datasets[f"{p}"])

    # create DocBin 
    for p in partitions:
        db = DocBin()
        for doc in [
            Doc(nlp.vocab).from_json(dataset_row) for dataset_row in datasets[f"{p}"]
        ]:
            db.add(doc)
        
        # save DANE
        db.to_disk(save_path / f"{p}" /  f"DANE_{p}.spacy")

def main(): 
    # define paths
    path = pathlib.Path(__file__)
    spacy_path = path.parents[2] / "data"

    # get DANE test set 
    fetch_dane(save_path=spacy_path, partitions=["test"])
    
    # get all sets from DANSK
    fetch_dansk(save_path=spacy_path, partitions=["train", "dev", "test"])

if __name__ == "__main__":
    main()