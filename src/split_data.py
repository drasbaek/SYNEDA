import spacy 
from spacy.tokens import DocBin


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