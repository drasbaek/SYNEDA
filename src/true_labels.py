'''
Make true labels for data
'''
import pathlib
import pandas as pd

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
    main()