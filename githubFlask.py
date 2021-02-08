from flask import Flask, render_template, request
from github import Github
import threading

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/userDataMethod', methods=['POST'])
def userDataMethod():
    username = request.form['username']
    git = Github()
    return interogateGit(git.get_user(username), "public")


@app.route('/keyDataMethod', methods=['POST'])
def keyDataMethod():
    accessKey = request.form['key']
    git = Github(accessKey)
    return interogateGit(git.get_user(), "")


# function to open a thread on each repository
def repoThreadBuilder(repo, test=False):
    # grab relevant global variables
    global languages, contents, commits, repoContents, repoCommits, repoNames

    local_languages = repo.get_languages()
    local_commits = []
    local_contents = []
    for commit in repo.get_commits():
        local_commits.append(commit)

    content = repo.get_contents("")
    while content:
        file_content = content.pop(0)
        if file_content.type == "dir":
            content.extend(repo.get_contents(file_content.path))
        else:
            local_contents.append(file_content)
    lock = threading.Lock()
    lock.acquire()
    try:
        repoNames.append(repo.full_name.split("/")[1])
        repoContents.append(len(local_contents))
        repoCommits.append(len(local_commits))
        contents = contents + local_contents
        commits = commits + local_commits
        for language in local_languages:
            if language in languages:
                languages[language] += local_languages[language]
            else:
                languages[language] = local_languages[language]
    finally:
        print("finished - ", repo.full_name)
        lock.release()
        if test:
            return([len(local_commits), local_languages, len(local_contents)])


# small function to asssign colour values to bars based on their percentage of the maximum value
def backgroundColours(inputList):
    colours = []
    for item in inputList:
        if item < 0:
            colours = []
            break
        else:
            colours.append("#" + hex(round((item / max(inputList)) * 200) + 55)[2:] + "0000")
    return colours


# interogate the github api to recieve the required data
def interogateGit(user, public, test=False):
    # create and initialise our global variables
    global commits, contents, languages, repoContents, repoCommits, repoNames
    repoCommits = []
    repoContents = []
    repoNames = []
    languages = {}
    commits = []
    contents = []
    threads = []

    # thread loops
    for repo in user.get_repos():
        threads.append(threading.Thread(target=repoThreadBuilder, args=(repo, ), daemon=True))

    for i in range(len(threads)):
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    # assign values to our derived variables
    languageValues = list(languages.values())
    languageNames = list(languages.keys())
    numberOfLanguages = len(languageNames)

    userName = user.login
    repos = user.get_repos()
    numRepos = repos.totalCount
    numCommits = len(commits)
    numContents = len(contents)
    averageContent = round(numContents / numRepos, 2)
    averageCommits = round(numCommits / numRepos, 2)

    repoCommitColours = backgroundColours(repoCommits)
    repoContentColours = backgroundColours(repoContents)
    languageColours = backgroundColours(languageValues)

    languageLegend = "Languages: <br> "
    languageTableData = ""
    firstLanguage = True

    for language in languages:
        languageLegend += language + " - " + str(languages[language]) + " <br/> "
        if firstLanguage:
            languageTableData += "<td> " + language + "</td> </tr>"
            firstLanguage = False
        else:
            languageTableData += "<tr> <td> " + language + "</td> </tr>"

    if not test:
        # pass all of our data to our html template
        return render_template('output.html',
                               userName=userName,
                               repoNames=repoNames,
                               commitColours=repoCommitColours,
                               contentColours=repoContentColours,
                               languageColours=languageColours,
                               contentsByRepo=repoContents,
                               commitsByRepo=repoCommits,
                               totalRepos=numRepos,
                               totalContents=numContents,
                               totalCommits=numCommits,
                               averageContent=averageContent,
                               averageCommits=averageCommits,
                               numberOfLanguages=numberOfLanguages,
                               languageLegend=languageLegend,
                               languageNames=languageNames,
                               languageValues=languageValues,
                               languageTableData=languageTableData,
                               public=public)
    else:
    	#pass all data to our unit tests 
        return [userName,
                sorted(repoNames),
                sorted(repoCommitColours),
                sorted(repoContentColours),
                sorted(languageColours),
                sorted(repoContents),
                sorted(repoCommits),
                numRepos,
                numContents,
                numCommits,
                averageContent,
                averageCommits,
                numberOfLanguages,
                sorted(languageNames),
                sorted(languageValues),
                public]


if __name__ == '__main__':
    app.run(debug=True, extra_files=["/githubVisualiser.css"])
