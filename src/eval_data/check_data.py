import pathlib
from datasets import load_dataset

def check_dane(datasets): 
    '''
    Check and load DANE
    '''
    # check distribution of labels (ents) in test
    test = datasets['test']

    # get all labels
    labels = {}

    # loop through all rows
    for i, row in enumerate(test):
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

if __name__ == "__main__":
    datasets = load_dataset("KennethEnevoldsen/dane_plus")

    labels = check_dane(datasets)

    print(labels)