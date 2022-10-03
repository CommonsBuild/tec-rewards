import pandas as pd
import os, sys


PATH = "./distribution_rounds"

folders = os.listdir(PATH)

combined_df = pd.DataFrame()

for folder in folders:
    try:
        filename = PATH + "/" + folder + "/praise_aragon_distribution.diff-1-2.csv"
        test = pd.read_csv(filename,header=None)
        combined_df = combined_df.append(test,  ignore_index=True)
        print(folder + " success")
    except:
        print("error in folder" + folder)




grouped_df  = combined_df.groupby([0])


aragon_df = pd.DataFrame(columns=["address", "amount", "token"])
for name, group in grouped_df:
    #print(name)
    #print(group[1].sum())
    aragon_df.loc[len(aragon_df.index)] = [name, group[1].sum(), "TEC"]

aragon_df.sort_values(by="amount", ascending=False, ignore_index=True, inplace=True)

print(aragon_df)
aragon_df.to_csv("aragon_combined_diff_1-16.csv", index=False, header=False)



