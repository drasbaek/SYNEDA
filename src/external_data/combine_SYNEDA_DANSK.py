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

def combine_dbs(db1, db2, save_path=None):
    '''
    Combines two DocBin objects into one DocBin object that have the same format and structure
    '''
    # combine the DocBin objects
    db1.merge(db2)

    # save
    if save_path:
        db1.to_disk(save_path)

    return db1


def shuffle_db(db):
    # Load your spaCy model
    nlp = spacy.blank("da")

    # Assuming you already have a DocBin object named doc_bin
    # Extract Docs from DocBin
    docs = list(db.get_docs(nlp.vocab))

    # Shuffle the Docs
    random.shuffle(docs)

    # Create a new DocBin and add shuffled Docs
    shuffled_db = DocBin(docs=docs, store_user_data=True)

    return shuffled_db



def main():
    # set paths
    path = pathlib.Path(__file__)
    data_path = path.parents[2] / "data" / "train"

    # load the SYNEDA and DANSK DocBin objects
    db_syneda = load_db(data_path, "SYNEDA_train.spacy")
    db_dansk = load_db(data_path, "DANSK_train.spacy")

    # print len of DocBin objects
    print(f"SYNEDA: {len(db_syneda)}")
    print(f"DANSK: {len(db_dansk)}")

    # combine the DocBin objects
    db_combined = combine_dbs(db_syneda, db_dansk, save_path = data_path / "SYNEDA_DANSK_train.spacy")

    # shuffle the DocBin object
    shuffled_db = shuffle_db(db_combined)

    # print len of combined DocBin object
    print(f"Combined (Shuffled): {len(shuffled_db)}")

if __name__ == "__main__":
    main()



    