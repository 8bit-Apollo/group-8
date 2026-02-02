import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os

# global information
repo = 'scottyab/rootbeer'

file = repo.split('/')[1]
fileInput = 'data/file_' + file + '.csv'

# load data
authorFileTouches = pd.read_csv(fileInput)

# convert dates to weeks
authorFileTouches['datetime'] = pd.to_datetime(authorFileTouches['date'])
authorFileTouches['week'] = authorFileTouches['datetime'].dt.to_period('W').apply(lambda r: r.start_time)

# make alias for file name including its extension
unique_files = authorFileTouches['filename'].unique()
mapping = {}
for i, name in enumerate(unique_files):
    ext = os.path.splitext(name)[1]
    mapping[name] = f"File {i+1}  ({ext})"
authorFileTouches['alias'] = authorFileTouches['filename'].map(mapping)

# plot
plt.figure(figsize=(12,5.5))
sns.set_style("whitegrid")

custom_palette = sns.color_palette("tab20") + sns.color_palette("Set1")[:2]
plot = sns.scatterplot(
    data=authorFileTouches,
    x='alias',
    y='week',
    hue='author',
    palette=custom_palette,
    s=100,
    alpha=0.75
)

# change y-axis labels to every 50 weeks
ax = plt.gca()
ax.yaxis.set_major_locator(mdates.WeekdayLocator(interval=50))

plt.title('Author file touches', fontsize=16)
plt.xlabel(None)
plt.ylabel(None)
plt.tick_params(axis='y', labelsize=14)
plt.xticks(rotation=65, ha='right')
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left', title='Authors')
plt.tight_layout()

fileOutput = 'data/plot_' + file + '.png'
plt.savefig(fileOutput)
print(f"Scatterplot saved to: {fileOutput}")