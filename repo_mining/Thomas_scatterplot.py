import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Structured after CollectFiles.py
try:
    df = pd.read_csv('data/authorsAndDates_rootbeer.csv')

    # load the data from the csv file 
    # Give each unique filename an index
    uniqueFileNames = df['File'].unique()
    fileIndex = {}
    index = 0
    for file in uniqueFileNames:
        fileIndex[file] = index
        index += 1
    # add another column that assigns each file an unique index
    df['FileIndex'] = df['File'].map(fileIndex)

    # apply same logic to assign each author an unique color index
    uniqueAuthors = df['Author'].unique()
    authorIndex = {}
    index = 0
    for author in uniqueAuthors:
        authorIndex[author] = index
        index += 1
    df['AuthorColorIndex'] = df['Author'].map(authorIndex)

    # convert to weeks
    df['Date'] = pd.to_datetime(df['Date'])
    df['Week'] = df['Date'].dt.isocalendar().week   
except:
    print ("Error reading data")
    exit(0)
    
# create scatter plot
plt.figure(figsize=(9, 5))
scatter = plt.scatter(
df['FileIndex'],
df['Week'],
c = df['AuthorColorIndex'],
cmap = 'tab20',
alpha = 0.8
)

# labels for x, y axis
plt.xlabel("File")
plt.ylabel("Weeks")

# legend for each author to their colors
handles, _ = scatter.legend_elements()
plt.legend(
    handles,
    uniqueAuthors,
    title="Authors",
    bbox_to_anchor=(1.05, 1),
    loc='upper left'
)

# show plot
plt.tight_layout()
plt.show()