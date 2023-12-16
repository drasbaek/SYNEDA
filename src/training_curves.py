'''
Script for plotting loss and eval curves
'''
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_wb_log(log_filename, log_path):
    '''
    Load wandb log file into pandas dataframe

    Args
        log_filename: name of wandb log file
        log_path: path to wandb log file
    
    Returns
        log_df: pandas dataframe with wandb log data
    '''
    # define path 
    log_file = log_path / log_filename

    # define wandb header columns
    wandb_header = ["E", "#", "LOSS TRANSFORMER", "LOSS NER", "ENTS_F", "ENTS_P", "ENTS_R", "SCORE"]

    # read log file into pandas dataframe with wandb header
    log_df = pd.read_csv(log_file, sep="\s+", names=wandb_header)

    return log_df

def plot_curve(logs, y_col, y_col_name, x_col ="#", save_path=None):
    '''
    Plot a single plot of model curves from wandb logfiles from particular column (e.g., loss or F1)

    Args
        logs: dictionary of pandas dataframes with wandb log data
        x_col: col name for x-axis
        y_col: col name for y-axis
        y_col_name: name for y-axis on the plot
        save_path: path to save plot (defaults to None, which does not save plot)

    Returns
        plt: matplotlib plot
    '''

    # define figure size 
    plt.figure(figsize=(10, 5))

    # define curves 
    plt.plot(logs["SYNEDA"][x_col], logs["SYNEDA"][y_col], label='SYNEDA')
    plt.plot(logs["DANSK"][x_col], logs["DANSK"][y_col], label='DANSK')
    plt.plot(logs["SYNEDA_DANSK"][x_col], logs["SYNEDA_DANSK"][y_col], label='SYNEDA_DANSK')
    
    # labels 
    plt.xlabel('Steps')
    plt.ylabel(y_col_name)

    # find which model has highest max steps
    max_steps = max(logs["SYNEDA"][x_col].max(), logs["DANSK"][x_col].max(), logs["SYNEDA_DANSK"][x_col].max())

    # spread out x-axis ticks (currently goes from 0 to 1000, to 2000, etc., i want more space)
    plt.xticks(range(0, max_steps, 400))

    # layout
    plt.legend()
    plt.grid(True)

    # save 
    if save_path:
        plt.savefig(save_path)

    return plt

import matplotlib.pyplot as plt

def plot_curve(logs, y_col1, y_col2, y_col_name1, y_col_name2, x_col="#", save_path=None, font_family=None):
    '''
    Plot curves from wandb logfiles from particular columns in two subplots.

    Args:
        logs: dictionary of pandas dataframes with wandb log data
        x_col: col name for x-axis
        y_col1: col name for the first y-axis
        y_col2: col name for the second y-axis
        y_col_name1: name for the first y-axis on the plot
        y_col_name2: name for the second y-axis on the plot
        save_path: path to save plot (defaults to None, which does not save plot)

    Returns:
        fig: matplotlib figure
    '''
    # set font to times
    if font_family:
        plt.rcParams["font.family"] = font_family

    # subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    # curves and labels for 1 subplot
    ax1.plot(logs["SYNEDA"][x_col], logs["SYNEDA"][y_col1], label='SYNEDA', color="#65BBF3")
    ax1.plot(logs["DANSK"][x_col], logs["DANSK"][y_col1], label='DANSK', color="#F36965")
    ax1.plot(logs["SYNEDA_DANSK"][x_col], logs["SYNEDA_DANSK"][y_col1], label='SYNEDA + DANSK', color="#9966FF")
    ax1.set_title(f"[A] {y_col_name1.split(' ')[0]}", size=18)
    ax1.set_ylabel(y_col_name1)
    ax1.grid(True)

    # curves and labels 2 subplot
    ax2.plot(logs["SYNEDA"][x_col], logs["SYNEDA"][y_col2], label='SYNEDA', color="#65BBF3")
    ax2.plot(logs["DANSK"][x_col], logs["DANSK"][y_col2], label='DANSK', color="#F36965")
    ax2.plot(logs["SYNEDA_DANSK"][x_col], logs["SYNEDA_DANSK"][y_col2], label='SYNEDA DANSK', color="#9966FF")
    ax2.set_title(f"[B] {y_col_name2.split(' ')[0]}", size=18)
    ax2.set_xlabel('Steps')
    ax2.set_ylabel(y_col_name2)
    ax2.grid(True)

    # find which model has highest max steps
    max_steps = max(logs["SYNEDA"][x_col].max(), logs["DANSK"][x_col].max(), logs["SYNEDA_DANSK"][x_col].max())

    ## LEGEND FIXES
    # mv ax1 legend outside of plot
    legend = ax1.legend(bbox_to_anchor=(0.85, 1.1), loc='upper left', borderaxespad=0.)
    legend.get_frame().set_alpha(None)

    for label in legend.get_texts():
        label.set_fontsize(13)  

    for line in legend.get_lines():
        line.set_markersize(13)  

    # spread out x-axis ticks 
    ax2.set_xticks(range(0, max_steps, 400))
    ax1.set_xticks(range(0, max_steps, 400))

    # save
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=600)

    return fig

def main(): 
    # define paths 
    path = pathlib.Path(__file__)
    log_path = path.parents[1] / "training" / "logs"

    # load a single log file
    log_filenames = ["SYNEDA.log", "DANSK.log", "SYNEDA_DANSK.log"]

    # extract model names from log filenames
    model_names = [log_filename.split(".")[0] for log_filename in log_filenames]

    # load all log files
    logs = {}

    for model_name, log_filename in zip(model_names, log_filenames):
        log_df = load_wb_log(log_filename, log_path)
        logs[f"{model_name}"] = log_df
    
    # plot loss 
    plot_curve(logs, x_col="#", y_col1="LOSS NER", y_col2="ENTS_F", y_col_name1="Loss (NER)", y_col_name2="F1 Score (ENTS)", save_path=path.parents[1] / "plots" / "curves.png", font_family="Times New Roman")





if __name__ == "__main__":
    main()