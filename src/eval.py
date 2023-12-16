import spacy
from spacy.scorer import Scorer
from spacy.tokens import DocBin
import numpy as np
from sklearn.utils import resample
import pathlib
from spacy.training import Example

# Calculate 95% Confidence Intervals
def confidence_interval(scores):
    lower = np.percentile(scores, 2.5)
    upper = np.percentile(scores, 97.5)
    return lower, upper

def convert_to_examples(db, nlp):
    '''
    Convert a DocBin to a list of spaCy Example objects with nlp object's vocab
    '''
    examples = []
    for doc in db.get_docs(nlp.vocab):
        entities = []

        for ent in doc.ents:
            entities.append((ent.start_char, ent.end_char, ent.label_))

        example = Example.from_dict(nlp.make_doc(doc.text), {"entities": entities})
        examples.append(example)

    return examples

def main():
    # set paths
    path = pathlib.Path(__file__)
    test_data_path = path.parents[1] / "data" / "test" / "SYNEDA_test.spacy"
    model_path = path.parents[1] / "training" / "models" / "SYNEDA" / "model-best"

    # load spaCy model
    nlp = spacy.load(model_path)

    # load  test data
    test_data = DocBin().from_disk(test_data_path)

    # convert DocBin to a list of examples
    examples = convert_to_examples(test_data, nlp)

    overall_scores = nlp.evaluate(examples)
    print("Overall scores:", overall_scores)

    # bootstrap resampling
    n_iterations = 100
    f_scores = []

    for _ in range(n_iterations):
        print("Iteration:", _)

        # resample your test data
        n_samples = 250

        print(f"Bootstrapping with {n_samples} samples!")
        sampled_examples = resample(examples, n_samples=n_samples)
        scores = nlp.evaluate(sampled_examples)

        f1_individual = scores["ents_f"]

        print("F-score:", f1_individual, "At iteration:", _)

        # collect scores
        f_scores.append(f1_individual)


    f_score_ci = confidence_interval(f_scores)
    print("F-score CI:", f_score_ci)

if __name__ == "__main__":
    main()
