import networkx as nx #networks package we will use for demos
import matplotlib.pyplot as plt #networkx uses matplotlib to generate its plots
import numpy as np #this is the linear algebra package for working with matrices
import pandas as pd #pandas is a dataframe package that is useful for managing network attributes
import math #use this package to take the log of a scalar, use numpy to take the element-wise log of an array
import os
import scipy
from collections import Counter
import csv

f = open('hubAuth_result.csv', 'w')

# create the csv writer
writer = csv.writer(f)

df = pd.read_csv('final_cleaned.csv', sep=",", header = None)

df.columns = ["Order","Language", "Influenced By", "Influenced", "Year"]

df.at[462,"Influenced By"] = "[Self, Lisp, Smalltalk]"
df.loc[df['Language'] == "Squeak"]
df.at[464,"Influenced"] = "[StarLogo, Scratch]"
df.loc[df['Language'] == "Etoys"]
G = nx.DiGraph()
G_test = nx.DiGraph()

for index, row in df.iterrows():
    lang = row["Language"]
    G_test.add_node(lang)
    if type(row["Influenced"]) == str:
        st = row["Influenced"]
        lis_infl = st.strip('][').split(', ')
        
        for infl in lis_infl:
            G_test.add_edge(lang, infl)

    if type(row["Influenced By"]) == str:
        st_by = row["Influenced By"]
        lis_inf_by = st_by.strip('][').split(', ')
        
        for inf_by in lis_inf_by:
            G_test.add_edge(inf_by, lang)

h, a = nx.hits(G_test)

top5 = dict(Counter(h).most_common(5))
for x,y in top5.items():
    print(x,y)
    row = x,y
    writer.writerow(row)



top5 = dict(Counter(a).most_common(5))
for x,y in top5.items():
    print(x,y)
    row = x,y
    writer.writerow(row)


writer.close()


