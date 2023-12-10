'''
Make true labels for data
'''
import pathlib
import pandas as pd
import spacy

def test():
    nlp = spacy.load("da_core_news_sm")
    doc = nlp("Nina Bang: var en fremtrædende figur i politik.")

    span = doc[0:2]

    print(span.text)
    print(span.start_char)
    print(span.end_char)
    print(span.id)

def main(): 
    # define paths
    path = pathlib.Path(__file__)
    data_path = path.parents[1] / "data"

    # load data
    df = pd.read_excel(data_path / "final_ents" / "NER_EXAMPLES.xlsx", index_col=0)

    # make into entities 
    df['entities'] = df['entities'].apply(lambda x: {item.split(': ')[0]: item.split(': ')[1] for item in eval(x)})

    # print first row 
    print(df['entities'][0].keys())



if __name__ == "__main__":
    test()