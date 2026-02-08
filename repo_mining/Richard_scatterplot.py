
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Configurations
CSV_PATH = "data/file_touches_authors_dates.csv"
TOP_N_FILES = 50
AUTHOR_COL = "AuthorLogin"
DATE_COL = "CommitDate"
FILE_COL = "Filename"

OUTPUT_FIG_CAL = "data/figures/weeks_vs_files_calendar.png"
OUTPUT_FIG_NUM = "data/figures/weeks_vs_files_numeric.png"
OUTPUT_FIG_TOP_AUTHORS_AND_FILES = "data/figures/top_authors_and_files.png"
OUTPUT_FIG_TOP_AUTHORS = "data/figures/top_authors.png"
OUTPUT_FIG_TOP_FILES = "data/figures/top_files.png"
OUTPUT_FIG_BOTTOM_AUTHORS = "data/figures/bottom_authors.png"
OUTPUT_FIG_BOTTOM_FILES = "data/figures/bottom_files.png"

# Load & preprocess
df = pd.read_csv(CSV_PATH)
df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce", utc=True)
df = df.dropna(subset=[DATE_COL, FILE_COL])
df[AUTHOR_COL] = df[AUTHOR_COL].fillna("unknown").astype(str)

# Short file names
df["ShortFile"] = df[FILE_COL].apply(lambda x: os.path.basename(x))

# Week start (calendar)
df["WeekStart"] = df[DATE_COL].dt.to_period("W").dt.start_time

# Numeric project week (0 = first week of project)
project_start = df["WeekStart"].min()
df["ProjectWeek"] = ((df["WeekStart"] - project_start).dt.days // 7).astype(int)

# Reduce to top-N files
top_files = df["ShortFile"].value_counts().head(TOP_N_FILES).index.tolist()
dff = df[df["ShortFile"].isin(top_files)].copy()

# Map files to x positions
file_to_x = {f: i for i, f in enumerate(top_files)}
dff["x"] = dff["ShortFile"].map(file_to_x)

# Colors per author (use matplotlib defaults)
authors = sorted(dff[AUTHOR_COL].unique())
color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
author_to_color = {a: color_cycle[i % len(color_cycle)] for i, a in enumerate(authors)}

# Plot 1: Showing Calendar weeks on Y-axis
plt.figure(figsize=(16, 10))
for author in authors:
    sub = dff[dff[AUTHOR_COL] == author]
    plt.scatter(sub["x"], sub["WeekStart"], label=author, s=35, alpha=0.75,
                c=author_to_color[author])

plt.xticks(range(len(top_files)), top_files, rotation=45, ha="right")
plt.xlabel("File")

ax = plt.gca()
ax.yaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.yaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.ylabel("Weeks")

plt.title("Source File Touches Over Time — Weeks vs Files (Colored by Author)")
plt.legend(title="Author", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()

os.makedirs(os.path.dirname(OUTPUT_FIG_CAL), exist_ok=True)
plt.savefig(OUTPUT_FIG_CAL, dpi=300)
#plt.show()

# Plot 2: Showing Numeric project weeks on Y-axis (Main scatter plot required for the exercise)
plt.figure(figsize=(12, 6))
for author in authors:
    sub = dff[dff[AUTHOR_COL] == author]
    plt.scatter(sub["x"], sub["ProjectWeek"], label=author, s=35, alpha=0.75,
                c=author_to_color[author])

plt.xticks(range(len(top_files)), top_files, rotation=45, ha="right",fontsize=10)
plt.xlabel("File",  fontsize=12)
plt.ylabel("Project Weeks (0 = project start)",  fontsize=12)

# Make numeric scale readable
plt.yticks(range(0, dff["ProjectWeek"].max() + 1, 25), fontsize=10)

plt.title("Source File Touches Over Project Lifetime — Weeks vs Files (Colored by Author)", fontsize=14)
plt.legend(title="Author", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
plt.tight_layout()
os.makedirs(os.path.dirname(OUTPUT_FIG_NUM), exist_ok=True)
plt.savefig(OUTPUT_FIG_NUM, dpi=300, bbox_inches="tight")
#plt.show()

OUTPUT_FIG_CAL, OUTPUT_FIG_NUM


### Additional Insights for the executive summary report..

# parse dates
df['CommitDate'] = pd.to_datetime(df['CommitDate'])

# top authors by touches
top_authors = df['AuthorLogin'].value_counts().head(15)

top_files = df['ShortFile'].value_counts().head(15)

bottom_authors = df['AuthorLogin'].value_counts().tail(15)

bottom_files = df['ShortFile'].value_counts().tail(15)

top_authors, top_files , bottom_authors , bottom_files


plt.figure(figsize=(12, 4))  

plt.subplot(1, 2, 1)
top_files.plot(kind="bar")
plt.title("Top Source Files by Touches", fontsize=14)
plt.ylabel("Number of Touches", fontsize=12)
plt.xlabel("File", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=10)

plt.subplot(1, 2, 2)
top_authors.plot(kind="bar")
plt.title("Top Authors by Source-File Touches", fontsize=14)
plt.ylabel("Number of Touches", fontsize=12)
plt.xlabel("Author", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=10)

plt.tight_layout()
#plt.savefig("figures/bar_charts.png", dpi=300, bbox_inches="tight")
os.makedirs(os.path.dirname(OUTPUT_FIG_TOP_AUTHORS_AND_FILES), exist_ok=True)
plt.savefig(OUTPUT_FIG_TOP_AUTHORS_AND_FILES, dpi=300,bbox_inches="tight")
#plt.show()

plt.figure()
top_authors.plot(kind='bar')
plt.title("Top Authors by Source-File Touches")
plt.ylabel("Number of Touches")
plt.xlabel("Author")
plt.tight_layout()
os.makedirs(os.path.dirname(OUTPUT_FIG_TOP_AUTHORS), exist_ok=True)
plt.savefig(OUTPUT_FIG_TOP_AUTHORS, dpi=300)
#plt.show()

plt.figure()
top_files.plot(kind='bar')
plt.title("Top Source Files by Touches")
plt.ylabel("Number of Touches")
plt.xlabel("File")
plt.tight_layout()
os.makedirs(os.path.dirname(OUTPUT_FIG_TOP_FILES), exist_ok=True)
plt.savefig(OUTPUT_FIG_TOP_FILES, dpi=300)
#plt.show()

plt.figure()
bottom_authors.plot(kind='bar')
plt.title("Bottom Authors by Source-File Touches")
plt.ylabel("Number of Touches")
plt.xlabel("Author")
plt.tight_layout()
os.makedirs(os.path.dirname(OUTPUT_FIG_BOTTOM_AUTHORS), exist_ok=True)
plt.savefig(OUTPUT_FIG_BOTTOM_AUTHORS, dpi=300)
#plt.show()

plt.figure()
bottom_files.plot(kind='bar')
plt.title("Bottom Source Files by Touches")
plt.ylabel("Number of Touches")
plt.xlabel("File")
plt.tight_layout()
os.makedirs(os.path.dirname(OUTPUT_FIG_BOTTOM_FILES), exist_ok=True)
plt.savefig(OUTPUT_FIG_BOTTOM_FILES, dpi=300)
#plt.show()