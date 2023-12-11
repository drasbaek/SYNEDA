'''
Prepare dataset with true labels 
'''
import pathlib
import pandas as pd
import spacy
import re
from spacy.tokens import DocBin

def convert_to_doc(df, textcol="sentences"):
    '''
    Convert text from text column into spacy doc objects. Save to 'doc' column.
    '''
    print("Loading blank spaCy model...")
    nlp = spacy.blank("da")

    df['doc'] = df[textcol].apply(lambda x: nlp(x))

    return df

def create_sents(df):
    '''
    Create sents column for dataframe with a spacy doc column
    '''
    sents = []

    for i in range(len(df)):
        # get doc object
        doc = df['doc'][i]
        
        # create sentences
        sent = [{"start": 0, "end": len(doc.text)}]

        # append to list
        sents.append(sent)
    
    # add to dataframe
    df['sents'] = sents

    return df

def create_tokens(df):
    '''
    Create tokens column for dataframe with a spacy doc column
    '''
    all_tokens = []

    for i in range(len(df)):
        # get doc object
        doc = df['doc'][i]

        # create tokens
        tokens = [{"id": idx, "start": token.idx, "end": token.idx + len(token.text)} for idx, token in enumerate(doc)]

        # append to list
        all_tokens.append(tokens)

    # add to dataframe
    df['tokens'] = all_tokens

    return df

def remove_context(df):
    '''
    Removes context from the entities column that is within {}
    '''

    # remove curly brackets and their contents in entities column and white space infront of it
    df['entities'] = df['entities'].str.replace(r'\s*{.*}\s*', '', regex=True)

    return df  

def create_entity_dict(df):
    '''
    Changes the formatting of entity lists from strings to a list of dictionaries.
    '''
    
    # make into a list of dictionaries for each entity pair.
    df['entities_dict'] = df['entities'].apply(lambda x: [{'ent': item.split(': ')[1], 'label': item.split(': ')[0]} for item in eval(x)])

    return df

def create_ents(df):
    '''
    Create ents column for a dataframe with a spacy doc column. It goes through a lot of checks with various regex patterns in order to ensure that ents are correct
    '''
    # create list of all ents 
    all_ents = []

    for i, row in df.iterrows():
        # get ents
        ents_dict_list = row['entities_dict']

        ents_in_row = []

        for ents_dict in ents_dict_list:
            # get ent
            ent = ents_dict['ent']

            # get label
            label = ents_dict['label']

            # Define the pattern to search for ent with or without quotations, accounting for various placements
            pattern = re.compile(r'(?:["\']{}["\']|{})[".,:;!?\s]|$'.format(re.escape(ent), re.escape(ent)))

            # Search for the pattern in the sentence
            matches = pattern.search(row['sentences'])

            match = matches.group(0)  # get matched text

            if not match: 
                # check whether the ent is more than one word
                if len(ent.split()) > 1:
                    # capitalize only the first word 
                    ent_format = ent.split()[0].capitalize() + " " + " ".join(ent.split()[1:])

                else: 
                    ent_format = ent.capitalize()

                # check pattern where ent is capitalized
                pattern = re.compile(r'(?:["\']{}["\']|{})["\'.;,:!?\s]|$'.format(re.escape(ent_format), re.escape(ent_format)))

                # Search for the pattern in the sentence
                matches = pattern.search(row['sentences'])
                match = matches.group(0)  # get matched text

                # get start index
                start = row['sentences'].find(match)

                if not match:
                    print("No {} and {} in sentence: {} at row {}".format(ent_format, ent, row['sentences'], i))
                    start = -1
            else: 
                start = row['sentences'].find(match)  # get start index
            
            end = start + len(match)-1  # get end index

            # create ent
            ent = {"start": start, "end": end, "label": label}

            # append to list
            ents_in_row.append(ent)
        
        # append to list
        all_ents.append(ents_in_row)

    # add to dataframe
    df['ents'] = all_ents
    
    return df

def remove_cardinal_en(df):
    '''
    Remove all cardinal numbers that are "en" from the dataframe
    '''
    # remove all cardinal numbers that are "en"
    df["entities_dict"] = df["entities_dict"].apply(lambda x: [item for item in x if item["label"] != "CARDINAL" and item["ent"] != "en"])

    return df

def label_pipeline(df):
    '''
    Pipeline for labeling NER data as SpaCy Span
    ''' 
    # remove context from ents
    df = remove_context(df)

    # create entity dict
    df = create_entity_dict(df)

    # remove cardinal numbers that are "en"
    df = remove_cardinal_en(df)

    # convert sentences to doc objects
    df = convert_to_doc(df)

    # create sents
    df = create_sents(df)

    # create tokens
    df = create_tokens(df)

    # create ents
    df = create_ents(df)

    return df

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

    for i, row in df.iterrows(): 
        # get doc
        doc = row['doc']

        # access dictionary within list in row['ents']
        spans = []

        for ent, ent_dict in zip(row['ents'], row['entities_dict']):
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
    df_ents = pd.read_excel(data_path / "DATASET.xlsx", sheet_name="ENTS")
    df_noents = pd.read_excel(data_path / "DATASET.xlsx", sheet_name="NO ENTS")

    # merge dataframes
    df = pd.concat([df_ents, df_noents])

    # reset index
    df.reset_index(inplace=True)

    # label data
    df = label_pipeline(df)
    
    # convert to spacy format (NB does not work!)
    db = convert_to_spacy(df)

    # remove doc column from dataframe
    df = df.drop(columns=["doc", "entities_dict", "checked", "changed?", "entities", "index", "type"])

    # save dataframe to json
    df.to_csv(data_path / "LABELLED_DATASET.csv", index=False)

if __name__ == "__main__":
    main()