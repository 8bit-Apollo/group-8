import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

 

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    # detect languages once
    languages = get_repo_languages(repo, lsttokens)
    print("Detected languages:", languages)
    
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    # if not is_source_file(filename, languages):
                    #     continue
                    # dictfiles[filename] = dictfiles.get(filename, 0) + 1
                    # print(filename)
                    if not filename:
                        continue
                    # ONLY count source files
                    if is_source_file(filename, languages):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)


# Retrieve the set of languages used in the given GitHub repo
def get_repo_languages(repo, lsttokens):
    """
    Uses GitHub REST API to retrieve the language breakdown:
    GET https://api.github.com/repos/{owner}/{repo}/languages
    Returns a set of language names, e.g. {"Java", "Kotlin", "C++", "CMake"}.
    """
    url = f"https://api.github.com/repos/{repo}/languages"
    data, _ = github_auth(url, lsttokens, 0)
    if data:
        return set(data.keys())
    return set()


# Map GitHub language names -> file extensions considered "source"
LANGUAGE_EXTENSIONS = {
    "Java": {".java"},
    "Kotlin": {".kt", ".kts"},
    "C": {".c", ".h"},
    "C++": {".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx", ".h"},
    "CMake": {".cmake", "CMakeLists.txt"},
}

def is_source_file(filename, languages):
    # handle special filenames
    if filename.endswith("CMakeLists.txt") and "CMake" in languages:
        return True

    _, ext = os.path.splitext(filename.lower())

    allowed_exts = set()
    for lang in languages:
        allowed_exts |= {e.lower() for e in LANGUAGE_EXTENSIONS.get(lang, set())
                         if e.startswith(".")}

    return ext in allowed_exts

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["",
             "" ]

languages = get_repo_languages(repo, lstTokens)
print(f"Repo languages: {languages}")

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))


file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
