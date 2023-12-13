'''
Script for combining the training data from SYNEDA and DANSK in order to obtain a larger training set.

The script is based on the script combine_SYNEDA_DANSK.py from the SYNEDA repository.
'''
import pathlib
import spacy
from spacy.tokens import Doc, DocBin
import random


def load_db(path, file_name):
    # add path to file name
    file_path = path / file_name

    # instatiate a DocBin object
    db = DocBin()

    # load the DocBin object from file
    db.from_disk(file_path)

    # return the DocBin object
    return db


def shuffle_db(db, seed=1209):
    '''
    Shuffle a docbin dataset
    '''
    # set seed
    random.seed(seed)

    # load mdl
    nlp = spacy.blank("da")

    # extract docs from mdl
    docs = list(db.get_docs(nlp.vocab))

    # shuffle docs
    random.shuffle(docs)

    # create new docbin with shuffled
    shuffled_db = DocBin(docs=docs, store_user_data=True)

    return shuffled_db

def combine_dbs(db1, db2, save_path=None):
    '''
    Combines two DocBin objects into one DocBin object that have the same format and structure. Shuffles the dataset with seed.
    '''
    # combine the DocBin objects
    db1.merge(db2)

    # shuffle
    shuffled_db = shuffle_db(db1)

    # save
    if save_path:
        print("SAVING COMBINED & SHUFFLED DATASET ...")
        shuffled_db.to_disk(save_path)

    return shuffled_db

def main():
    # set paths
    path = pathlib.Path(__file__)

    # load the SYNEDA and DANSK DocBin objects
    partions = ["train", "dev"]

    for p in partions: 
        print(f"PROCESSING: {p.upper()} SET")
        data_path = path.parents[2] / "data" / p

        db_syneda = load_db(data_path, f"SYNEDA_{p}.spacy")
        db_dansk = load_db(data_path, f"DANSK_{p}.spacy")

        # print len of DocBin objects
        print(f"SYNEDA: {len(db_syneda)}")
        print(f"DANSK: {len(db_dansk)}")

        # combine the DocBin objects
        db_combined = combine_dbs(db_syneda, db_dansk, save_path = data_path / f"SYNEDA_DANSK_{p}.spacy")

        # print len of combined DocBin object
        print(f"Combined {p} set (Shuffled): {len(db_combined)}")

if __name__ == "__main__":
    main()



    