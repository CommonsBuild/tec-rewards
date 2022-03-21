import pandas as pd
import numpy as np


# FUNCTIONS FROM THE IH DISTRIBUTION NOTEBOOK

# To be called from outside

def resource_percentage(x, p):
    relevant_percentile = np.percentile(x, p)
    filtered_x = x[x > relevant_percentile]
    pct = np.sum(filtered_x)/np.sum(x)
    return pct


def calc_shannon_entropies(x):
    my_entropy = shannon_entropy(x)
    max_entropy = np.log2(len(x))
    rel_entropy = my_entropy/max_entropy
    return [my_entropy, max_entropy, rel_entropy]


def nakamoto_coeff(x, key):
    sorted_x = x.sort_values(by=key, ascending=False)
    tot_sum = np.array(sorted_x[key].cumsum())
    try:
        winner = np.array([k for k in range(len(tot_sum))
                          if tot_sum[k] > 0.5]).min() + 1
    except:
        winner = -1
    return winner


def gini_gt_p(x, p):
    pct = np.percentile(x, p)
    filtered_x = x[x >= pct]
    gini = gini_coefficient(filtered_x)
    return gini


# To be used internally

def gini_coefficient(x):
    n = len(x)
    x_bar = np.mean(x)
    abs_diffs = np.array([np.sum(np.abs(x[i] - x)) for i in range(n)])
    sum_abs_diffs = np.sum(abs_diffs)
    denominator = 2*n*n*x_bar
    return sum_abs_diffs/denominator


def shannon_entropy(x):
    filtered_x = x[x > 0]  # remove any 0 values
    # normalize to proportion/probability if not already
    p = filtered_x/np.sum(filtered_x)
    log_2_p = np.log2(filtered_x)
    calc = -np.dot(p, log_2_p)
    return calc

# courtesy of @inventandchill
# n_senders: Left side. Praise senders. n largest ones + rest (others)
# n_receivers: Right side. Praise receivers. n largest ones + rest (others)


def prepare_praise_flow(dataframe_in, n_senders, n_receivers):
    reference_df = dataframe_in[['FROM', 'TO', 'FINAL QUANT']].copy()
    reference_df.reset_index(inplace=True, drop=True)
    reference_df.dropna(subset=['FROM', 'TO', 'FINAL QUANT'], inplace=True)
    reference_df.reset_index(inplace=True, drop=True)

    # sank_df1=df1.copy()
    # Left side. Praise senders. X largest ones + rest (others). (-1 because of zero-counting)
    n1 = n_senders - 1
    # Right side. Praise receivers. Y larget one + rest (others) (-1 because of zero-counting)
    n2 = n_receivers - 1

    df_from = reference_df.groupby(['FROM']).sum().copy()
    df_from.reset_index(inplace=True, drop=False)
    min_from = df_from['FINAL QUANT'].sort_values(ascending=False).unique()[n1]
    df_from2 = df_from.copy()
    df_from2.loc[df_from2['FINAL QUANT'] < min_from, 'FROM'] = 'Rest from 1'

    df_to = reference_df.groupby(['TO']).sum().copy()
    df_to.reset_index(inplace=True, drop=False)
    min_to = df_to['FINAL QUANT'].sort_values(ascending=False).unique()[n2]
    df_to2 = df_to.copy()
    df_to2.loc[df_to2['FINAL QUANT'] < min_to, 'TO'] = 'Rest to 1'

    df3 = reference_df.copy()
    i = 0

    length_data = df3.shape[0]

    while (i < length_data):
        if (not(df3.at[i, 'FROM'] in df_from2['FROM'].unique())):
            df3.at[i, 'FROM'] = 'REST FROM'
        if (not(df3.at[i, 'TO'] in df_to2['TO'].unique())):
            df3.at[i, 'TO'] = 'REST TO'

        i = i+1

    df4 = df3.copy()

    # Change to "df4=df4.groupby(['From', 'To']).count().copy()" in case you need count of events, but not sum of IH
    df4 = df4.groupby(['FROM', 'TO']).sum().copy()

    df4.reset_index(inplace=True, drop=False)
    df4['TO'] = df4['TO']+' '
    # df_to2=reference_df.groupby(['To']).sum().copy()

    # df3=reference_df.copy()
    #df3.loc[df3['nominated_stake']<nominated_stake_min, 'id_validator1']='rest_validators'

    return df4
