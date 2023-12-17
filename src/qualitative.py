'''
Qualitative analysis of the data
'''
import pathlib
from eval import convert_to_examples
import spacy
from spacy.tokens import DocBin
    
def main(): 
    path = pathlib.Path(__file__)
    model_root = path.parents[1] / "training" / "models"
    test_data_path = path.parents[1] / "data" / "test"

    # load one test file
    test_db = DocBin().from_disk(test_data_path / "DANSK_test.spacy")

    # load nlp
    nlp = spacy.load(model_root / "SYNEDA" / "model-best")

    # convert to examples
    examples = convert_to_examples(test_db, nlp)

    # get one example 
    #example = examples[146] #Taler 8: jeg er helt blank på den
    example = examples[83]

    print(example.text)

    # evaluate example
    score = nlp.evaluate([example])

    print(score)
    print(example)

if __name__ == "__main__":
    main()
