import pathlib
import pandas as pd
import sys
from spacy.tokens import DocBin
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sys.path.append(str(pathlib.Path(__file__).parents[1]))
from external_data.fetch_data import fetch_dansk, fix_dane, fetch_dane

def get_performance(model_name, test_set_name, results_path):
    
    # get data path
    performance = pd.read_json(results_path / model_name / f"results_on_{test_set_name}.json", orient="index")

    # reset index
    performance = performance.reset_index() 

    # filer index column to only include ents_per_type
    performance = performance[performance["index"] == "ents_per_type"]

    # drop index column
    performance = performance.drop(columns=["index"])

    # get the dict
    performance = performance.iloc[0].to_dict()

    # keep only f-score
    performance = {label: values['f'] for label, values in performance[0].items()}

    # sort by label alphabetically
    performance = {k: performance[k] for k in sorted(performance)}

    return performance

def plot_performance(performance_dicts, test_set, save_path=None):
    '''
    Create a plot with each of the labels on the y-axis and then the f-score for each model on the x-axis as dots (colored by model)
    '''

    # create dataframe
    df = pd.DataFrame(performance_dicts)

    # transpose dataframe
    df = df.transpose()

    # reset index
    df = df.reset_index()

    # rename index column
    df = df.rename(columns={"index": "label"})

    # melt dataframe
    df = df.melt(id_vars=["label"])

    # rename columns
    df = df.rename(columns={"variable": "model", "value": "f-score"})

    # fix model names from 0, 1, 2 to SYNEDA, DANSK, SYNEDA_DANSK
    df["model"] = df["model"].replace({0: "SYNEDA", 1: "DANSK", 2: "SYNEDA + DANSK"})

    # remove LANGUAGE label from DANE (since there is no LANGUAGE in DANE)
    if test_set == "DANE":
        df = df[df["label"] != "LANGUAGE"]

    # create plot
    sns.set_theme(style="whitegrid")

    # set font to times
    plt.rcParams["font.family"] = "Times New Roman"

    # create figure
    fig, ax = plt.subplots(figsize=(14, 10))

    # set colors for each model
    colors = {"SYNEDA": "#65BBF3", "DANSK": "#F36965", "SYNEDA + DANSK": "#9966FF"}

    # create plot as dots with swarmplot, adding some white space between each row
    sns.swarmplot(data=df, x="f-score", y="label", hue="model", palette=colors, size=12, alpha=1, ax=ax)

    # add horizontal lines
    ax.hlines(y=np.arange(0, len(df["label"].unique())), xmin=0, xmax=1, color="black", alpha=0.5, linestyles="dashed")

    # set x-axis label
    ax.set_xlabel("F-score", fontsize=16, labelpad=10)

    # remove y-axis label
    ax.set_ylabel("")

    # create new legend at top, just outside plot
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=3, fontsize=16)

    # set x-axis limit
    ax.set_xlim(0, 1)

    # save plot to high DPI
    if save_path:
        plt.savefig(save_path, dpi=500, bbox_inches="tight")




def main():
    path = pathlib.Path(__file__)

    # get data path
    results_path = path.parent.parent.parent / "results"
    plot_path = path.parent.parent.parent / "plots"

    test_sets = ["DANE", "DANSK", "SYNEDA"]

    for set in test_sets:
        syneda_performance = get_performance("SYNEDA", set, results_path)
        dansk_performance = get_performance("DANSK", set, results_path)
        syneda_dansk_performance = get_performance("SYNEDA_DANSK", set, results_path)

        # plot performance on DANE
        plot_performance([syneda_performance, dansk_performance, syneda_dansk_performance], test_set = set, save_path=plot_path / f"performance_{set.lower()}.png")

if __name__ == "__main__":
    main()