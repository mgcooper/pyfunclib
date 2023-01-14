# Utility functions

# Plot results
import os
import glob
import yaml
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def load_yaml_file(yaml_file):
    """
    Load a yaml file

    Parameters
    ----------
    yaml_file: str
        Path to yaml file

    Returns
    -------
    dict or None:
        Dictionary of YAML information. None returned if error occured
    """

    try:
        with open( yaml_file, 'r') as f:
            yaml_dict = yaml.safe_load(f)
    except IOError:
        message = f'Error: Could not read file {yaml_file}'
        print(message)
        yaml_dict = None
    except yaml.YAMLError as exc:
        message = f'Error in configuration file: {yaml_file}'
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            message += "\nError position: ({}:{})".format(mark.line+1, mark.column+1)

        print(message)
        yaml_dict = None

    return yaml_dict


def save_yaml_dict(yaml_dict, yaml_file):
    """
    Save dict to yaml file

    Parameters
    ----------
    yaml_dict: Dict
        Dictionary to save

    yaml_file: str
        Path to yaml file to save

    """

    with open(yaml_file, 'w') as f:
        yaml.dump(yaml_dict, f)

#############################################################################
# Model Naming Function
#############################################################################

def get_model_id(model_name, name_prefix):
    model_split = model_name.split(name_prefix)

    model_id_str = model_split[-1]

    first_letter = model_id_str[0]

    model_id = -1
    if first_letter.isdigit():
        model_id = int(model_id_str)

    return(model_id)


def get_model_name(name_prefix, model_dir, reuse_name=False):
    """
    Get name of next model

    Parameters
    ----------
    name_prefix: str
        Model prefix

    model_dir: str
        Directory to store model

    reuse_name: bool, default=False
        Reuse last model name

    Returns
    -------
    model_name: str
        Name to save model as
    """


    # Get sorted model ids
    models = [ os.path.basename(f) for f in glob.glob(os.path.join(model_dir, name_prefix) + '*')]
    
    if len(models) == 0:
        return "{}1".format(name_prefix)

    model_ids = [get_model_id(m, name_prefix) for m in models]
    model_ids.sort()
    model_name = ""

    # Get latest model id
    latest_id = model_ids[-1]
    # If want to reuse, use same model name
    if reuse_name:
        model_name =  "{}{}".format(name_prefix, str(latest_id))
    # Create new model name
    else:
        new_id = latest_id + 1
        model_name = "{}{}".format(name_prefix, str(new_id))

    return model_name

#############################################################################
# Data Functions
#############################################################################
def load_discharge_and_perm_data(discharge_file = "../data/all_ensemble_q_updated.csv",
                                 perm_file ="../data/ensemble_para.csv",
                                 perm_field_list = ['s3', 's6', 'g1', 'g5', 'g7']):
    """
    Loads the discharge time series data from the supplied file.
    
    This function is used in notebook train_nn_model.ipynb
    
    Parameters
    ----------
    discharge_file: str
        CSV File with the time series data
        
    perm_file: str
        CSV file with subsurface permeabilitiy data
        
    perm_field_list: List[str]
        List of permeabilities to read
        
    Returns
    -------
    q_ens_df: pandas.DataFrame
        Dataframe of time series discharge
        
    q_times: pandas.DataFrame
        Time stamps associated with discharge data
        
    perm_df: pandas.DataFrame
        Datframe of permeability data
    """
    
    # Load discharge data
    print("Loading discharge data")
    q_df = pd.read_csv(discharge_file)

    # Limit to only first 2 years: 2014-08-31 to 2016-08-31
    start_date = '2014-08-31'
    end_date = '2016-09-01'
    
    start_frame = q_df['datetime'] >= start_date
    end_frame = q_df['datetime'] < end_date
    time_frame = start_frame & end_frame
    q_df = q_df[time_frame]


    # Separate observation and time columns
    q_cols = list(q_df.columns)
    q_ens_cols = q_cols[2:]
    q_ens_df = q_df[q_ens_cols]
    q_times = q_df['datetime']
    q_obs = q_df['q_obs']
        
    # Load permeability fields 
    para_df = pd.read_csv(perm_file, index_col=0)

    # Keep only relevant fields, if specified
    para_df = para_df[perm_field_list]

    # Filter permeability parameters to only be same for discharge fieles
    ens_start = len('q_ats_')
    ens_rows = [ x[ens_start:] for x in q_ens_cols]
    perm_df = para_df.loc[ens_rows]
    
    perm_df = perm_df.transpose()
    
    # Rename columns
    new_cols = [ f"q_ats_{x}" for x in perm_df.columns]
    perm_df.columns = new_cols
    
    return q_ens_df, q_times, perm_df


# #############################################################################
# # Plots
# #############################################################################
def plot_perm_one_to_one(y_true, y_pred, perm_field_list, units = "$log_{10}(m^2)$"):
    """
    Create a one-to-one plot of the estimated and real subsurface permability values
    
    Args:
        y_true (nsamples, P): True permeability values. P is the number of permeabilities 
        y_pred (nsamples, P): Estimated permeability values
        perm_field_list (P): List of permeabilitiy values
        units: Units to display in plot

    """

    title_fontsize = 28
    yfontsize = 24
    xfontsize = yfontsize
    tick_fontsize=20

    nperms = len(perm_field_list)

    fig_width = 16

    figsize = (fig_width, 10)

    min_vals = np.min(y_true, axis=0)
    max_vals = np.max(y_true, axis=0)


    nrows = int(np.ceil(nperms/3))
    ncols = int(np.ceil(nperms/nrows))

    total_subs = nrows*ncols
    turn_off = total_subs - nperms

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    # Turn off unused axis
    for a in range(1, turn_off+1):
        axs[-1, -1*a].axis('off')

    my_ticks = None

    for index in range(nperms):
        x=y_true[:, index]
        y=y_pred[:, index]

        plt.subplot(nrows, ncols, index+1)

        comp = perm_field_list[index]

        ax = sns.scatterplot(x=x, y=y)

        min_val = min_vals[index]
        max_val = max_vals[index]

        if index % 3 == 0:
            ax.set_ylabel(f'Predicted - {units}', fontsize=yfontsize)

        ax.set_xlabel(f'Real - {units}', fontsize=xfontsize)

        ax.tick_params(axis="both", labelsize=tick_fontsize)

        ax = sns.lineplot(x=[min_val, max_val], y=[min_val, max_val], color="r", ax=ax)

        ax.set_title(f'{comp}', fontsize=title_fontsize)

    plt.tight_layout()




