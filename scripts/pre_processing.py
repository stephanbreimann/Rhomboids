"""
This is a script for cysteine proteases screening (Rhomboid like).

Notes
-----
Following criteria are applied on polytopic transmembrane proteins:
    a) Polytopic: n TMD >= 2
    b) Cys in TMD (n>=1 Cys in n>=1 TMDs)
    c) His in TMD (n>=1 His in n>=1 TMDs, where at least one TMD different to Cys TMD)
    d) TM proteins with unknown function (i.e., just structural characterization in gene names)
        Via filter gene names for
        1. TLCD (TLC domain-containing protein)
        2. TMX (Transmembrane X superfamily, X=1...9)
        3. TMC (Transmembrane channel like protein)
        4. TMEM (Transmembrane protein)
        5. TMIGD3 (Transmembrane domain-containing)
    e) Flanking Gly (G[xx]C[xx]G, e.g. GxCG
    f) 6 TM

Next, structural comparison should be applied using Alpha Fold Structures (or PDB) to find a possible active center,
    defined as C and H in spatial proximity (3-10 Angström, bonding distance).

See Also
--------
https://alphafold.ebi.ac.uk/

"""
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import scripts._utils as ut
import scripts.config as conf

# Settings
pd.set_option('expand_frame_repr', False)  # Single line print for pd.Dataframe

COL_ENTRY = "entry"
COL_TRANSMEMBRANE = "transmembrane"
COL_START_STOP = "start_stop"
COL_SEQ = "sequence"
COL_N_TMDs = "n_tmds"

# TODO Filter pattern
# TODO check AlphaFold


# I Helper Functions
def get_multi_pass_tm(df=None, min_n=2, term="TRANSMEM"):
    """"""
    df = ut.standardize_col(df=df.copy())
    list_ids = []
    list_n_tmd = []
    list_tm = []
    list_start_stop = []
    for i, row in df.iterrows():
        tmd_id = row[COL_ENTRY]
        transmem = row[COL_TRANSMEMBRANE]
        seq = row[COL_SEQ]
        if str(transmem) != "nan" and transmem.count(term) >= min_n:
            list_ids.append(tmd_id)
            f = lambda x: tuple([int(i) for i in x.lstrip().split(" ")[1].split("..")])
            start_stop = [f(i) for i in transmem.split(";") if term in i]
            list_n_tmd.append(len(start_stop))
            list_start_stop.append(start_stop)
            list_tm.append([seq[i[0]-1:i[1]] for i in start_stop])
    df_f = df[df["entry"].isin(list_ids)].copy()
    df_f[COL_N_TMDs] = list_n_tmd
    df_f[COL_TRANSMEMBRANE] = list_tm
    df_f[COL_START_STOP] = list_start_stop
    return df_f


def filter_str(df=None, query_str=None, query_col="gene names"):
    """"""
    df = df.copy()
    list_ids = []
    for i, row in df.iterrows():
        tmd_id = row[COL_ENTRY]
        name = row[query_col]
        if isinstance(name, str) and name.startswith(query_str):
            list_ids.append(tmd_id)
    return list_ids


def filter_aa(df=None, aa="C", dist_to_terminus=3, min_hits=1):
    """Filter for all proteins containing distinct amino acid in tmds"""
    df = df.copy()
    list_ids = []
    list_count_hit = []
    list_tm_hit = []
    for i, row in df.iterrows():
        tmd_id = row[COL_ENTRY]
        tm = row[COL_TRANSMEMBRANE]
        tm_short = [x[dist_to_terminus:-dist_to_terminus] for x in tm]
        tm_hit = [i + 1 for i, x in enumerate(tm_short) if aa in x]
        n_hits = len([x for x in tm_short if aa in x])
        if n_hits >= min_hits:
            list_ids.append(tmd_id)
            list_count_hit.append(n_hits)
            list_tm_hit.append(tm_hit)
    df_f = df[df["entry"].isin(list_ids)].copy()
    col_name = f"n {aa}"
    df_f[col_name] = list_count_hit
    col_name = f"TM with {aa}"
    df_f[col_name] = list_tm_hit
    return df_f


# II Main Functions
def filter_unkown_function(df=None):
    list_query_str = ["TLCD", "TM2", "TM4", "TM6", "TM7", "TM9", "TMC", "TMEM", "TMIGD3"]
    list_ids = []
    for query_str in list_query_str:
        list_ids.extend(filter_str(df=df, query_str=query_str))
    df = df[df["entry"].isin(list_ids)].copy()
    return df


def remove_hits_in_same_tm(df=None):
    """"""
    list_ids = list(df[(df["n H"] == 1) & (df["n C"] == 1) & (df["TM with C"] == df["TM with H"])]["entry"])
    df = df[~df["entry"].isin(list_ids)]
    return df


# III Test/Caller Functions
def uniprot_parsing():
    """"""
    file = "uniprot_filtered_human.tab"
    df = pd.read_csv(conf.folder_data + file, sep="\t")
    df = get_multi_pass_tm(df=df)
    df = filter_unkown_function(df=df)
    df = filter_aa(df=df, aa="C")
    df = filter_aa(df=df, aa="H")
    df = remove_hits_in_same_tm(df=df)
    df = df.sort_values(by="n_tmds", ascending=False).reset_index(drop=True)
    df.to_excel(conf.folder_results + "polytopic_tmps_with_cystein.xlsx", index=False)


# IV Main
def main():
    t0 = time.time()
    uniprot_parsing()
    t1 = time.time()
    print("Time:", t1 - t0)


if __name__ == "__main__":
    main()
