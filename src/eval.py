import spacy
from spacy.scorer import Scorer
from spacy.tokens import DocBin
import numpy as np
from sklearn.utils import resample
import pathlib
from spacy.training import Example
from tqdm import tqdm
import pandas as pd

def confidence_interval(scores):
    '''
    Compute 95% confidence interval for a list of scores
    '''
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

def bootstrap(model_name, model_rootdir, test_db, test_filename, n_iter:int=100, n_samples=250, save_path=None): 
    '''
    Bootstrapping function
    '''
    model_path = model_rootdir / model_name / "model-best"

    # load spaCy model
    nlp = spacy.load(model_path)

    # convert to examples
    examples = convert_to_examples(test_db, nlp)

    # get overall score 
    overall_scores = nlp.evaluate(examples)
    
    # prepare for bootstrap
    f1_scores = []
    p_scores = [] 
    r_scores = []

    print(f"Bootstrapping with {n_samples} samples for {model_name} model on {test_filename}!")
    for i in tqdm(range(n_iter)):
        # resample
        sampled_examples = resample(examples, n_samples=n_samples)

        # eval
        scores = nlp.evaluate(sampled_examples)

        # get scores
        f1_score = scores["ents_f"]
        p_score = scores["ents_p"]
        r_score = scores["ents_r"]

        # append to 
        f1_scores.append(f1_score)
        p_scores.append(p_score)
        r_scores.append(r_score)

    # make into dataframe
    df = pd.DataFrame({"iter":i+1, "f1": f1_scores, "p": p_scores, "r": r_scores})

    # get confidence intervals
    f1_ci = confidence_interval(f1_scores)
    p_ci = confidence_interval(p_scores)
    r_ci = confidence_interval(r_scores)

    # save dataframe to csv
    if save_path:
        full_path = save_path / "bootstrap" / f"{model_name}"
        full_path.mkdir(parents=True, exist_ok=True)
        df.to_csv(full_path / f"bootstrap_on_{test_filename}.csv")

        # save confidence intervals to txt 
        with open(full_path / f"confidence_intervals_on_{test_filename}.txt", "w") as f:
            f.write(f"Bootstrapping results for model {model_name} on dataset {test_filename}\n")
            f.write(f"Overall scores: {overall_scores}\n")
            f.write("-----------------------------------\n")
            f.write(f"95% confidence intervals for model: {model_name} on {test_filename}\n")
            f.write(f"F1 CI: {f1_ci}\n")
            f.write(f"Precision CI: {p_ci}\n")
            f.write(f"Recall CI: {r_ci}\n")

    return df, f1_ci, p_ci, r_ci

def main(): 
    path = pathlib.Path(__file__)
    model_root = path.parents[1] / "training" / "models"
    test_data_path = path.parents[1] / "data" / "test"

    test_files = ["SYNEDA_test.spacy", "DANSK_test.spacy", "DANE_test.spacy"]
    models = ["SYNEDA", "DANSK", "SYNEDA_DANSK"]

    # load all test data 
    test_dbs = {}

    for test_file in test_files:
        test_db = DocBin().from_disk(test_data_path / test_file)
        test_dbs[test_file.split("_")[0]] = test_db

    # use bootstrap function
    results_path = path.parents[1] / "results"

    for test_filename, test_data in test_dbs.items():
        for model in models:
            bootstrap(model, model_root, test_data, test_filename, save_path=results_path)


if __name__ == "__main__":
    main()
