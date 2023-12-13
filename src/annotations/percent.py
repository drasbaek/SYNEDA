import pandas as pd
import numpy as np
import pathlib
import random

from utils import number_words

def number_words(): 
    small_numbers = [
        "to", "tre", "fire", "fem", "seks", "syv", "otte", "ni", "ti", "tolv", "tretten", "fjorten", "femten", "seksten", "sytten", "atten", "nitten",
        "tyve", "tredive", "fyrre", "halvtreds", "tres", "firs", "halvfems", "halvfems", "halvfjerds", "firs", "halvfems"
    ]

    big_numbers = ["tusind", "et hundrede"]

    # make one final list
    all_numbers = small_numbers + big_numbers

    return all_numbers


def percent():
    """
    Creates a dataframe with randomly sampled cardinal numbers.
    
    """
    # define how many floats and ints to generate
    n_size = 200

    # generate floats up to 100 (half of total n_size)
    random_floats = np.random.uniform(low=0, high=100, size=int(n_size * 0.2)).round(2)
    random_ints = np.random.randint(low=0, high=100, size=int(n_size * 0.8))

    # number words (edge cases)
    numbers_words = number_words()*2

    # combine numbers and words
    all_numbers = np.concatenate([random_floats, random_ints, numbers_words])

    # formatted percents
    formatted_percents = []

    # len of all numbers
    len_all_numbers = len(all_numbers)

    for num in range(len_all_numbers):
        # get num
        num = np.random.choice(all_numbers)

        # ensure space if num is a word
        if num in numbers_words:
            formatted_percent = f"{num} procent"

        # give a 80% probability adding a space at the end of a number
        else:
            if np.random.rand() > 0.2:
                num = f"{num} "

            # concatenate quantity and num
            formatted_percent = f"{num}%"

        # append to list
        formatted_percents.append(formatted_percent)

    return formatted_percents

def main(): 
    # set seed
    np.random.seed(1209)

    # define paths 
    path = pathlib.Path(__file__)
    ents_path = path.parents[2] / "dbase" / "entities_lists"

    formatted_percents = percent()

    # add weights and context col (to match other lists)
    df = pd.DataFrame(formatted_percents, columns=["entity"])

    # add weights and context col (to match other lists)
    df["weight"] = 1
    df["context"] = None

    # save to file
    df.to_csv(ents_path / "PERCENT.csv", index=False)

    
if __name__ == "__main__":
    main()

