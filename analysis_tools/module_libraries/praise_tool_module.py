import pandas as pd
import numpy as np


# courtesy of @inventandchill
# n_senders: Left side. Praise senders. n largest ones + rest (others)
# n_receivers: Right side. Praise receivers. n largest ones + rest (others)


def prepare_praise_flow(dataframe_in, n_senders, n_receivers):
    reference_df = dataframe_in[['FROM', 'TO', 'AVG SCORE']].copy()
    reference_df.reset_index(inplace=True, drop=True)
    reference_df.dropna(subset=['FROM', 'TO', 'AVG SCORE'], inplace=True)
    reference_df.reset_index(inplace=True, drop=True)

    # sank_df1=df1.copy()
    # Left side. Praise senders. X largest ones + rest (others). (-1 because of zero-counting)
    n1 = n_senders - 1
    # Right side. Praise receivers. Y larget one + rest (others) (-1 because of zero-counting)
    n2 = n_receivers - 1

    df_from = reference_df.groupby(['FROM']).sum().copy()
    df_from.reset_index(inplace=True, drop=False)
    min_from = df_from['AVG SCORE'].sort_values(ascending=False).unique()[n1]
    df_from2 = df_from.copy()
    df_from2.loc[df_from2['AVG SCORE'] < min_from, 'FROM'] = 'Rest from 1'

    df_to = reference_df.groupby(['TO']).sum().copy()
    df_to.reset_index(inplace=True, drop=False)
    min_to = df_to['AVG SCORE'].sort_values(ascending=False).unique()[n2]
    df_to2 = df_to.copy()
    df_to2.loc[df_to2['AVG SCORE'] < min_to, 'TO'] = 'Rest to 1'

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
    #df3.loc[df3['nominated_stake']<
    return df4