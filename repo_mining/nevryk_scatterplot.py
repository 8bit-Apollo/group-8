import csv
import os
from datetime import datetime

import matplotlib.pyplot as plt

INPUT_CSV = "repo_mining/data/nevryk_file_touches_authors_dates.csv"
OUTPUT_PNG = "repo_mining/data/nevryk_weeks_vs_files.png"


def parse_date(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_touches(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0] == "filename":
                continue
            filename, author, date_str = row
            rows.append((filename, author, parse_date(date_str)))
    return rows


def main():
    rows = load_touches(INPUT_CSV)
    if not rows:
        print("No data found in", INPUT_CSV)
        return

    start_date = min(r[2] for r in rows)

    file_to_idx = {}
    author_to_color = {}
    color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    x_vals = []
    y_vals = []
    colors = []

    for filename, author, dt in rows:
        if filename not in file_to_idx:
            file_to_idx[filename] = len(file_to_idx)

        if author not in author_to_color:
            author_to_color[author] = color_cycle[len(author_to_color) % len(color_cycle)]

        week_index = (dt - start_date).days // 7
        x_vals.append(week_index)
        y_vals.append(file_to_idx[filename])
        colors.append(author_to_color[author])

    plt.figure(figsize=(12, 6))
    plt.scatter(x_vals, y_vals, c=colors, s=30, alpha=0.75)

    file_labels = [os.path.basename(f) for f in file_to_idx.keys()]
    plt.yticks(range(len(file_labels)), file_labels)
    plt.xlabel("Weeks since project start")
    plt.ylabel("File")
    plt.title("Weeks vs Files (colored by author)")

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300)
    print(f"Scatterplot saved to: {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
