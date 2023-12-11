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
    Create ents column for a dataframe with a spacy doc column. It goes through a lot of checks with various regex patterns in order to ensure that ents are correct.
    '''
    all_ents = []  

    for i, row in df.iterrows():
        ents_dict_list = row['entities_dict']  # get dict

        # skip row if entities_dict is empty
        if not ents_dict_list:
            all_ents.append([])
            continue

        ents_in_row = [] 

        for ents_dict in ents_dict_list:
            ent = ents_dict['ent']  # get text
            label = ents_dict['label']  # get label

            if label == "PERCENT" and "%" in ent:
                pattern = re.escape(ent) + r'(?!\w)'
            elif label == "ORDINAL":
                pattern = re.escape(ent) + r'.'
            # if the label is money and ent ends on a period, remove the period from the pattern
            elif label == "MONEY" and ent.endswith("."):
                pattern = re.escape(ent[:-1]) + r'(?!\w)'
            # if the label is money and has a special character (e.g. $), add a backslash before the special character
            elif label == "MONEY" and re.search(r'[^a-zA-Z0-9\s]', ent):
                pattern = re.escape(ent) + r'(?!\w)'
            elif label == "PERSON" and ent.endswith("."):
                pattern = re.escape(ent) + r'(?!\w)'
            # if ent starts with @, add a backslash before the @
            elif ent.startswith("@"):
                pattern = re.escape(ent) + r'(?!\w)'
            # if ent has a parenthesis, add a backslash before the parenthesis
            elif "(" in ent or ")" in ent:
                pattern = re.escape(ent) + r'(?!\w)'
            elif label == "LAW":
                pattern = re.escape(ent) + r'(?!\w)'
            # if ent contains a +, add a backslash before the +  OR contains a ' e.g., '23, add a backslash before the '
            elif "+" in ent or "'" in ent:
                pattern = re.escape(ent) + r'(?!\w)'
            elif label == "CARDINAL":
                pattern = r'\b' + re.escape(ent) + r'(?!\w)'
            else:  # general case
                pattern = r'\b' + re.escape(ent) + r'(?!\w)'

            # search for the pattern in the sentence, ignoring case
            for match in re.finditer(pattern, row['sentences'], re.UNICODE):
                # get start and end of match
                start, end = match.span()        

                if (row['sentences'][start-1:start] in ['"', "'"]) and (row['sentences'][end:end+1] in ['"', "'"]):
                # exclude the quotes from the span
                    start = start - 1
                    end = end + 1
                
                # add span
                ent_dict = {"start": start, "end": end, "label": label}
                ents_in_row.append(ent_dict)

        if not ents_in_row:
            # search now but ignore case
            for match in re.finditer(pattern, row['sentences'], re.IGNORECASE):
                # get start and end of match
                start, end = match.span()        

                if (row['sentences'][start-1:start] in ['"', "'"]) and (row['sentences'][end:end+1] in ['"', "'"]):
                # exclude the quotes from the span
                    start = start - 1
                    end = end + 1
                
                # add span
                ent_dict = {"start": start, "end": end, "label": label}
                ents_in_row.append(ent_dict)

        all_ents.append(ents_in_row)  # Add entities of the current row to the main list

    df['ents'] = all_ents  # Add entities column to the dataframe

    return df

def remove_cardinal_en(df):
    '''
    Remove all cardinal numbers that are "en" from the dataframe but without removing the entire row
    '''
    for i, row in df.iterrows():
        # get ents
        ents = row['entities_dict']

        # loop through all ents
        for ent in ents:
            # get label
            label = ent['label']
            text = ent['ent']

            # check if label is cardinal and text is "en"
            if label == "CARDINAL" and text == "en":
                # remove from ents
                ents.remove(ent)
    
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

    # remove doc column from dataframe
    df = df.drop(columns=["doc", "checked", "changed?", "entities", "index", "type", "entities_dict"])

    # rename "sentences" column to "text"
    df = df.rename(columns={"sentences": "text"})

    # save dataframe to json
    df.to_csv(data_path / "LABELLED_DATASET.csv", index=False)

if __name__ == "__main__":
    main()