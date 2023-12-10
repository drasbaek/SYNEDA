'''
Make true labels for data
'''
import pathlib
import pandas as pd
import spacy
import re

def convert_to_doc(df):
    '''
    Converts the sentences column to a spacy doc object.

    Parameters
        df (pandas.DataFrame): dataframe with sentences column

    Returns
        df (pandas.DataFrame): dataframe with sentences column changed to spacy doc object
    '''
    print("Loading blank spaCy model...")
    nlp = spacy.blank("da")

    df['doc'] = df['sentences'].apply(lambda x: nlp(x))

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

    Parameters
       df (pandas.DataFrame): dataframe with entities column
    
    Returns
        df (pandas.DataFrame): dataframe with entities column changed to list of dictionaries
    '''
    
    # make into a list of dictionaries for each entity pair.
    df['entities_dict'] = df['entities'].apply(lambda x: [{'ent': item.split(': ')[1], 'label': item.split(': ')[0]} for item in eval(x)])

    return df



def create_ents(df):
    '''
    Create ents column for a dataframe with a spacy doc column
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
            pattern = re.compile(r'(?:["\']{}["\']|{})[.,;!?\s]|$'.format(re.escape(ent), re.escape(ent)))

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
                pattern = re.compile(r'(?:["\']{}["\']|{})[.,!?\s]|$'.format(re.escape(ent_format), re.escape(ent_format.replace(".", r"\."))))

                # Search for the pattern in the sentence
                matches = pattern.search(row['sentences'])

                match = matches.group(0)  # get matched text
                #print(match)

                if not match:
                    print("Could not find {} in sentence: {} at row {}".format(ent_format, row['sentences'], i))
                    start = -1
            else: 
                start = row['sentences'].find(match)  # get start index
            
            end = start + len(match)  # get end index

            # create ent
            ent = {"start": start, "end": end, "label": label}

            # append to list
            ents_in_row.append(ent)
        
        # append to list
        all_ents.append(ents_in_row)

    # add to dataframe
    df['ents'] = all_ents
    
    return df
            
def main(): 
    # define paths
    path = pathlib.Path(__file__)
    data_path = path.parents[1] / "data"

    # load data
    df = pd.read_excel(data_path / "DATASET.xlsx", sheet_name="ENTS")
    
    # remove context from ents
    df = remove_context(df)

    # create entity dict
    df = create_entity_dict(df)

    # convert sentences to doc objects
    df = convert_to_doc(df)

    # create sents
    df = create_sents(df)

    # create tokens
    df = create_tokens(df)

    # create ents
    df = create_ents(df)

    # print all ents where start key has a value of -1
    #print(df[df['ents'].apply(lambda x: any(ent['start'] == -1 for ent in x))])
    #print(df.iloc[0])


if __name__ == "__main__":
    main()