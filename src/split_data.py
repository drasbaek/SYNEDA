import pathlib
import spacy 
import pandas as pd
from spacy.tokens import DocBin
import ast


def convert_to_spacy(df, save_path=None):
    '''
    Convert dataframe to spacy format. Inspired by https://spacy.io/usage/training#training-data

    Args
        df: dataframe with ents column
        save_path: path to save spacy docbin object (defaults to None i.e., no saving)
    
    Returns
        db: spacy docbin object
    '''
    db = DocBin()  # create a DocBin object
    nlp = spacy.blank("da")

    for i, row in df.iterrows(): 
        # get doc
        sentence = row['sentences']

        # create doc
        doc = nlp(sentence)

        # access dictionary within list in row['ents']
        spans = []

        for ent in row['ents']:
            # get start, end and label
            start, end, label = ent.values()

            # check if ent is at the end of a doc or if it is a money, quantity, ordinal or law entity (these often have annotation problems)
            if end+2 >= len(doc.text) or label in ["MONEY", "QUANTITY", "ORDINAL", "LAW"]:
                alignment_mode = "expand"
            else: 
                alignment_mode = "strict"

            span = doc.char_span(int(start), int(end), label=label, alignment_mode=alignment_mode)

            # append to list
            spans.append(span)

        # append ents to doc
        doc.ents = spans

        # add doc to docbin
        db.add(doc)

    # save docbin
    if save_path:
        db.to_disk(save_path)

    return db

def main(): 
    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[1] / "data"

    # load data
    df = pd.read_csv(data_path / "LABELLED_DATASET.csv")

    # convert entities dict into a dict again within col
    df['ents'] = df['ents'].apply(ast.literal_eval)

    # convert to spacy format
    db = convert_to_spacy(df)


if __name__ == "__main__":
    main()