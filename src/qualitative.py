'''
Qualitative analysis of the data
'''
import pathlib
from eval import convert_to_examples
import spacy
from spacy.tokens import DocBin
from spacy.scorer import Scorer
    
def main(): 
    path = pathlib.Path(__file__)
    model_root = path.parents[1] / "training" / "models"
    test_data_path = path.parents[1] / "data" / "test"

    # load one test file
    dansk_test_db = DocBin().from_disk(test_data_path / "DANSK_test.spacy")
    dane_test_db = DocBin().from_disk(test_data_path / "DANE_test.spacy")

    # load nlp
    nlp = spacy.load(model_root / "SYNEDA_LU" / "model-best")

    # convert to examples
    dansk_examples = convert_to_examples(dansk_test_db, nlp)
    dane_examples = convert_to_examples(dane_test_db, nlp)

    # get examples of mistakes
    example_taler = dansk_examples[146] # Taler 8: jeg er helt blank på den
    example_pirater = dansk_examples[605] # Pirater
    example_ordinal = dane_examples[363] # - Du ska' snakke med 2. kontor!
    example_cardinal = dane_examples[352] # - Du ska' snakke med 2. kontor! 206

    # concatenate the four examples
    examples = [example_taler, example_pirater, example_ordinal, example_cardinal]

    # iterate over examples
    for example in examples:
        score = nlp.evaluate([example])
        print('\n', "Text: ", example.text, '\n', "Evaluated as:", score)

if __name__ == "__main__":
    main()
