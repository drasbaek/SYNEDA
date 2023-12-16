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

def main():
    # set paths
    path = pathlib.Path(__file__)
    test_data_path = path.parents[1] / "data" / "test" / "SYNEDA_test.spacy"
    model_path = path.parents[1] / "training" / "models" / "syneda" / "model-best"

    # load spaCy model
    nlp = spacy.load(model_path)

    # load  test data
    test_data = DocBin().from_disk(test_data_path)

    # convert DocBin to a list of examples
    examples = list(test_data.get_docs(nlp.vocab))

    # Bootstrap resampling
    n_iterations = 100
    precision_scores, recall_scores, f_scores = [], [], []

    for _ in range(n_iterations):
        print("Iteration:", _)

        # Resample your test data
        sampled_examples = resample(examples)

        # Scoring
        scorer = Scorer(nlp)
        for example in sampled_examples:
            scorer.score([example])  # score expects a list of Example objects
            print(scorer.scores)

        # Collect scores
        scores = scorer.scores
        precision_scores.append(scores['ents_p'])
        recall_scores.append(scores['ents_r'])
        f_scores.append(scores['ents_f'])


    precision_ci = confidence_interval(precision_scores)
    recall_ci = confidence_interval(recall_scores)
    f_score_ci = confidence_interval(f_scores)

    print("Precision CI:", precision_ci)
    print("Recall CI:", recall_ci)
    print("F-score CI:", f_score_ci)

if __name__ == "__main__":
    main()


