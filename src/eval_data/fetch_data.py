'''
Script to fetch external data 

Heavily inspired by 
https://github.com/centre-for-humanities-computing/DaCy/blob/main/training/ner_fine_grained/fetch_assets.py 
'''

import spacy
from datasets import load_dataset
from spacy.tokens import Doc, DocBin
import pathlib

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

def fetch_dane(): 
    try:
        datasets = load_dataset("KennethEnevoldsen/dane_plus")
    except FileNotFoundError:
        raise FileNotFoundError(
            "Dane_Plus is not available. Check that HuggingFace is up and running, and that the dataset has been publically released.",
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
        db.to_disk(corpus_path / f"DANE_{p}.spacy")

if __name__ == "__main__":
    fetch_dansk()
    fetch_dane()