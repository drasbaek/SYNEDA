'''
Split annotations_w_generations_spanned into train, dev, test. Convert to .spacy formats for model development.
'''

import pathlib
import spacy 
import pandas as pd
from spacy.tokens import DocBin
import ast
from sklearn.model_selection import train_test_split

def create_splits(df, train_size=0.8, dev_size=0.1, test_size=0.1, random_state=1209):
    '''
    Create train, dev and test splits from dataframe
    '''
    # split into train and test
    train_df, test_df = train_test_split(df, train_size=train_size, 
                                         random_state=random_state, shuffle=True,
                                         )

    # split test into test and val
    dev_df, test_df = train_test_split(test_df, train_size=dev_size/(dev_size+test_size), 
                                       random_state=random_state, shuffle=True
                                       )

    return train_df, dev_df, test_df

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
        text = row['text']

        # create doc
        doc = nlp(text)

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

def distributions_labels(df):
    '''
    Return distribution of labels in ents dict from dataframe 
    '''
    # create empty dict
    labels = {}

    # loop through all rows
    for i, row in df.iterrows():
        # get ents
        ents = row['ents']

        # loop through all ents
        for ent in ents:
            # get label
            label = ent['label']

            # add to dict
            if label in labels.keys():
                labels[label] += 1
            else:
                labels[label] = 1
        
    return labels

def main(): 
    # define paths 
    path = pathlib.Path(__file__)
    data_path = path.parents[1] / "dbase" / "annotations"

    # load data
    df = pd.read_csv(data_path / "annotations_w_generations_spanned.csv")

    # convert entities dict into a dict again within col
    df['ents'] = df['ents'].apply(ast.literal_eval)

    # print distribution of labels
    print(distributions_labels(df))

    # create splits
    train_df, dev_df, test_df = create_splits(df)

    # print lengths
    print(f"Train length: {len(train_df)}")
    print(f"Dev length: {len(dev_df)}")
    print(f"Test length: {len(test_df)}")

    # check distributions post split
    for df in [train_df, dev_df, test_df]:
        labels = distributions_labels(df)
        print(labels)
        print(len(labels.keys()))

    # convert all to spacy format
    spacy_path = path.parents[1] / "data" 
    spacy_path.mkdir(parents=True, exist_ok=True)

    train_db = convert_to_spacy(train_df, save_path = spacy_path/ "train" / "SYNEDA_train.spacy")
    dev_db = convert_to_spacy(dev_df, save_path = spacy_path/ "dev" / "SYNEDA_dev.spacy")
    test_db = convert_to_spacy(test_df, save_path = spacy_path/ "test" / "SYNEDA_test.spacy")


if __name__ == "__main__":
    main()