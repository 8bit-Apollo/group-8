import csv
import json
import os
import requests

REPO = "scottyab/rootbeer"
SOURCE_FILES_CSV = "repo_mining/data/nevryk_file_rootbeer.csv"
OUTPUT_CSV = "repo_mining/data/nevryk_file_touches_authors_dates.csv"


def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {"Authorization": "Bearer {}".format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct


def load_source_files(path):
    source_files = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            if row[0] == "Filename":
                continue
            source_files.add(row[0])
    return source_files


def collect_file_touches(repo, source_files, lstTokens):
    ipage = 1
    ct = 0
    rows = []

    while True:
        spage = str(ipage)
        commitsUrl = (
            "https://api.github.com/repos/" + repo + "/commits?page=" + spage + "&per_page=100"
        )
        jsonCommits, ct = github_auth(commitsUrl, lstTokens, ct)

        if len(jsonCommits) == 0:
            break

        for shaObject in jsonCommits:
            sha = shaObject["sha"]
            author = shaObject["commit"]["author"]["name"]
            date = shaObject["commit"]["author"]["date"]

            shaUrl = "https://api.github.com/repos/" + repo + "/commits/" + sha
            shaDetails, ct = github_auth(shaUrl, lstTokens, ct)
            filesjson = shaDetails["files"]

            for filenameObj in filesjson:
                filename = filenameObj["filename"]
                if filename in source_files:
                    rows.append([filename, author, date])
                    print(f"{filename}\t{author}\t{date}")

        ipage += 1

    return rows


if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        print("Missing GITHUB_TOKEN. Run: export GITHUB_TOKEN=...")
        raise SystemExit(1)

    lstTokens = [token]

    source_files = load_source_files(SOURCE_FILES_CSV)
    touches = collect_file_touches(REPO, source_files, lstTokens)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "author", "date"])
        writer.writerows(touches)

    print(f"File written to: {OUTPUT_CSV}")
    print(f"Total author file touches: {len(touches)}")
