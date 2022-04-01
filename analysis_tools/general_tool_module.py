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

nominated_stake_min, 'id_validator1']='rest_validators'

    return df4
