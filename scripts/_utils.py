"""
This is a script for ...
"""
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import scripts.config as conf

# Settings
pd.set_option('expand_frame_repr', False)  # Single line print for pd.Dataframe


# I Helper Functions


# II Main Functions
def standardize_col(df, reset_index=True):
    """Standardize columns uniprot_id and gen_name"""
    if reset_index is True:
        df.reset_index(drop=True, inplace=True)
    df.columns = [x.lower() for x in list(df.columns)]
    dict_name_list = {'entry': ['tmd_id', 'id', 'uniprot_id'],
                      'name': ['gen_name', 'entry_name', "entry name"],
                      'mean': ['total_mean'],
                      'sequence': ['seq'],
                      'start': ['start_region', 'start_tmd'],
                      'stop': ['stop_region', 'stop_tmd'],
                      'subcellular location': ["subcellular location [cc]"]}
    for key in dict_name_list:
        for name in dict_name_list[key]:
            if name in list(df.columns):
                df.rename(columns={name: key}, inplace=True)
    return df

# III Test/Caller Functions


# IV Main
def main():
    t0 = time.time()
    t1 = time.time()
    print("Time:", t1 - t0)


if __name__ == "__main__":
    main()
