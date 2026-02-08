# Author: Matthew Jackson 
# creates a scatterplot of weeks vs file variables

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv
import os

#change file paths as needed
file = "scatterplot"
fileOutput = "C:/Users/HP/Desktop/Projects/cs472/group-8/repo_mining/data/RootbeerCommit.png"
csv_file = "C:/Users/HP/Desktop/Projects/cs472/group-8/repo_mining/data/file_rootbeerCOMMITMORE.csv"
CommitDF = pd.read_csv(csv_file)

# return weeks since start date
CommitDF['Date'] = pd.to_datetime(CommitDF['Date'])
start = CommitDF['Date'].min()
CommitDF['Week'] = (CommitDF['Date'] - start).dt.days // 7

files = CommitDF['Filename']
authors = CommitDF['Author'].unique()

# scatter plot
cmap = plt.get_cmap('tab20')
author_cmap = {author: cmap(i%20) for i, author in enumerate(authors)}
CommitDF['Color'] = CommitDF['Author'].map(author_cmap)

plt.figure(figsize=(14,10))
scatterplot = plt.scatter(
    x=CommitDF['Week'],
    y=CommitDF['Filename'],
    c=CommitDF['Color'],
    alpha=0.6,
    edgecolors='w',
    s=100)

plt.yticks(fontsize=6)

plt.title("Timine of modification by Author and Density")
plt.xlabel("weeks since start")
plt.ylabel("Files Modified")
plt.grid(True, linestyle='--', alpha=0.2)

legend = [
    mpatches.Patch(color=color, label=author)
    for author, color, in author_cmap.items()
]
plt.legend(handles=legend, title="Authors")

plt.savefig(fileOutput)
plt.show()