
import csv
import os
import time

# Reuse github_auth + countfiles from Richard_CollectFiles.py
from RichardSserunjogi_CollectFiles import github_auth, countfiles


# Configurations
repo = "scottyab/rootbeer" 
lstTokens = ["", ""] #DO NOT COMMIT real tokens

OUTPUT_CSV = "data/file_touches_authors_dates.csv"
PER_PAGE = 100


# Collect touches per file (author + date)
def collect_file_touches(repo, source_files, lstTokens):
    """
    For each source file, fetch commits touching that file and
    collect (author, date) information.
    """
    ct = 0
    rows = []

    for idx, filename in enumerate(source_files, start=1):
        print(f"[{idx}/{len(source_files)}] Processing: {filename}")

        page = 1
        while True:
            safe_filename = filename.replace(" ", "%20")

            commitsUrl = (
                f"https://api.github.com/repos/{repo}/commits"
                f"?path={safe_filename}&page={page}&per_page={PER_PAGE}"
            )

            jsonCommits, ct = github_auth(commitsUrl, lstTokens, ct)

            # stop if no more commits for this file
            if not jsonCommits:
                break

            for commitObj in jsonCommits:
                sha = commitObj.get("sha")

                # GitHub user (may be None)
                authorObj = commitObj.get("author") or {}
                author_login = authorObj.get("login")

                # Commit metadata (always present)
                commitMeta = commitObj.get("commit") or {}
                commitAuthor = commitMeta.get("author") or {}

                rows.append({
                    "filename": filename,
                    "sha": sha,
                    "author_login": author_login,
                    "author_name": commitAuthor.get("name"),
                    "author_email": commitAuthor.get("email"),
                    "date_iso": commitAuthor.get("date")
                })

            page += 1

    return rows


# Write output to CSV 
def write_touches_csv(output_path, rows):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Filename",
            "CommitSHA",
            "AuthorLogin",
            "AuthorName",
            "AuthorEmail",
            "CommitDate"
        ])

        for r in rows:
            writer.writerow([
                r["filename"],
                r["sha"],
                r["author_login"],
                r["author_name"],
                r["author_email"],
                r["date_iso"]
            ])


if __name__ == "__main__":
    # 1) Call adapted countfiles() from Richard_CollectFiles.py
    #    This already filters to SOURCE FILES ONLY
    source_files_dict = {}
    countfiles(source_files_dict, lstTokens, repo)

    source_files = list(source_files_dict.keys())
    print(f"Total source files detected: {len(source_files)}")

    # 2) Collect author + date touches
    touches = collect_file_touches(repo, source_files, lstTokens)

    # 3) Write results to CSV
    write_touches_csv(OUTPUT_CSV, touches)

    print(f"Done. Output written to: {OUTPUT_CSV}")
