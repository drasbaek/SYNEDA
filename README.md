![SYNEDA LOGO CROPPED](https://github.com/drasbaek/SYNEDA/assets/71491570/5104e03e-3bc0-4c7d-adb4-d6ee7569972d)

<p align="center">
  Anton Drasbæk Schiønning (<strong><a href="https://github.com/drasbaek">@drasbaek</a></strong>) and
  Mina Almasi (<strong><a href="https://github.com/MinaAlmasi">@MinaAlmasi</a></strong>)<br>
  Aarhus University, Natural Language Processing Exam (E23)
</p>
<hr>

## About
This repository contains the scripts used to develop `SYNEDA` (**Sy**nthetic **N**amed **E**ntity **Da**nish dataset) for Danish named entity recognition. Concretely, the dataset is created by developing a `reverse-annotation` pipeline, consisting of the following steps: 

1. Devising entity databases for 18 entity categories, following the OntoNotes 5.0 framework (see [dbase/entities_lists](https://github.com/drasbaek/SYNEDA/tree/main/dbase/entities_lists))
2. Combining entities across databases (randomly) to create `annotation lists` (see [dbase/annotations](https://github.com/drasbaek/SYNEDA/tree/main/dbase/annotations)). 
3. Prompting a ChatGPT 4 instance with the `annotations lists` to generate text around them (see [data](https://github.com/drasbaek/SYNEDA/tree/main/data)).

### Release
The `SYNEDA` dataset can be downloaded from the `data` folder (already split into `train`, `dev` and `test`). 

## Project Overview
The repository is structured as such: 
| Folder/File               | Description |
|---------------------------|-------------|
| `data/`                   | Contains the `.spacy` versions of all three splits of SYNEDA. Placeholder files are inserted for DANSK and DaNE+ (obtained with `src/external_data/fetch_data.py`). |
| `dbase/`                  | Contains the databases for the entity lists. Also functions as a store for all annotation lists and their corresponding generations. |
| `plots/`                  | Contains all plots used in the SYNEDA paper and appendix. |
| `results/`                | Contains all evaluation results for all three models specified in the paper. |
| `src/`                    | Contains all Python code related to the project. |
| `training/`               | Contains SpaCy config files for training the models as well as their logs and a placeholder folder for the models. |
| `annotations.sh`          | Executes all scripts related to non-manual annotations. |
| `debug.sh`, `train.sh`, `evaluate.sh` | For debugging datasets, training and evaluating models with SpaCy pipelines. |

Please note that the `src` folder has a seperate [README](https://github.com/drasbaek/SYNEDA/tree/main/src) with a greater overview of the scripts within. 


## Technical Requirements
The training pipeline was run via on Ubuntu v22.04.3, Python v3.10.12 (UCloud, Coder Python 1.84.2). Creating the annotations and plotting was done locally on a Macbook Pro ‘13 (2020, 2 GHz Intel i5, 16GB of ram). 

Python's venv needs to be installed for the code to run as intended.

## Setup
Prior to running any code, please run the command below to create a virtual environment (`env`) and install necessary packages within it:
```
bash setup
```

## Usage
The spaCy training pipeline can be rerun by running the three bash scripts `debug.sh`, `train.sh`, and `evaluate.sh`. For instance:
```
bash train.sh
```

Other files can be run as shown below while `env` is activated. For instance, the file to perform evaluation with bootstrapping:
```
python src/analysis/bootstrap_eval.py
```

## Contact
For any questions regarding the project or its reproducibility, please feel free to contact us: 
<ul style="list-style-type: none;">
  <li><a href="mailto:drasbaek@post.au.dk">drasbaek@post.au.dk</a>
(Anton)</li>
    <li><a href="mailto: mina.almasi@post.au.dk"> mina.almasi@post.au.dk</a>
(Mina)</li>
</ul>

## Acknowledgements 
This work could not have been done without the extensive work by the teams behind [spaCy](https://spacy.io/) and [DaCy](https://github.com/centre-for-humanities-computing/DaCy) as well as the datasets [DANSK](https://huggingface.co/datasets/chcaa/DANSK) and [DaNe+](https://huggingface.co/datasets/KennethEnevoldsen/dane_plus).

