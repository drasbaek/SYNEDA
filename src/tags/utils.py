import numpy as np

def number_words():
    '''
    Create list of numbers in words (danish) from pre-defined list of small numbers and big numbers.
    '''

    small_numbers = [
        "to", "tre", "fire", "fem", "seks", "syv", "otte", "ni", "ti", "tolv", "tretten", "fjorten", "femten", "seksten", "sytten", "atten", "nitten",
        "tyve", "tredive", "fyrre", "halvtreds", "tres", "firs", "halvfems", "halvfems", "halvfjerds", "firs", "halvfems"
    ]

    big_numbers = ["hundrede", "tusinde", "millioner"]

    big_combined_nums = []

    for num in small_numbers: 
        for big_num in big_numbers: 
            big_combined_nums.append(f"{num} {big_num}")

    # sample 30 big nums 
    big_combined_numbers = np.random.choice(big_combined_nums, size=28)

    # combine with small nums 
    all_numbers = np.concatenate([small_numbers, big_combined_numbers])

    return all_numbers