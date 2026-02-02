import json
import requests
import csv

import os

'''
zachary-sin_CollectFiles: find all unique files (or source files) and count the number of times it was touched
zachary-sin_authorsFileTouches: find all unique files (or source files) and track the author and date for each touch on that file
'''
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
def countfiles(authorFileTouches, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

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

                # Get primary author and date information for the commit
                author = shaObject['commit']['author']['name']
                date = shaObject['commit']['author']['date']

                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    # check file type
                    if SOURCE_FILES_ONLY:
                        if filename.endswith(SOURCE_FILE_EXT):
                            authorFileTouches.append([filename, author, date])
                            print(f"Source file touch: {filename}\t{author}\t{date}")
                        elif filename.endswith(CONFIG_FILE_EXT):
                            print(f"Skipping touch on configuration file: {filename}")
                        else:
                            print(f"Skipping touch on other file: {filename}")
                    else:
                        authorFileTouches.append([filename, author, date])
                        print(f"File touch: {filename}\t{author}\t{date}")
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

# control flag
SOURCE_FILES_ONLY = True

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# differentiate between source and config files using file extensions
CONFIG_FILE_EXT = (".xml", ".json", ".yaml", ".gradle", ".properties", ".mk", ".pro", ".iml")
SOURCE_FILE_EXT = (".java", ".py", ".kt", ".kts", ".c", ".cpp", ".h", ".sh")

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = []

authorFileTouches = []
countfiles(authorFileTouches, lstTokens, repo)
print('Total number of file touches: ' + str(len(authorFileTouches)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'

with open(fileOutput, 'w', newline='', encoding='utf-8') as fileCSV:
    writer = csv.writer(fileCSV)

    # col  names
    writer.writerow(["filename", "author", "date"])

    # all rows
    writer.writerows(authorFileTouches)

print(f"File written to: {fileOutput}")
print(f"Total author file touches: {len(authorFileTouches)}")