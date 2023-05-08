import git
import os
import requests
from bs4 import BeautifulSoup

# Base URL for searching repositories on GitHub
baseUrl = f"GITHUB SEARCH QUERY LINK"

# Directory to save downloaded repositories
repoDirectory = r"PATH TO SAVE REPOS"

def main():
    count = 1
    url = checkNextPage(count)
    while url != "N/A":
        print("Moving to page " + str(count))
        count = count + 1
        getAllLinks(url)
        url = checkNextPage(count)

# Function to check the next page of search results on GitHub
def checkNextPage(count):
    newUrl = baseUrl + str(count)
    response = requests.get(newUrl)
    if response.status_code == 200:
        return newUrl
    else:
        return "N/A"

# Function to download a repository from GitHub
def downloadRepo(gitUrl):
    repo_name = gitUrl.split("/")[-1]
    repo_path = os.path.join(repoDirectory, repo_name)
    if os.path.exists(repo_path):
        print(f"Repository {repo_name} already exists in {repoDirectory}")
    else:
        git.Repo.clone_from(gitUrl, repo_path)
        
    # Check if file size of items with same name are different and rename if necessary
    for filename in os.listdir(repo_path):
        path = os.path.join(repo_path, filename)
        if os.path.isfile(path):
            name, extension = os.path.splitext(filename)
            for i in range(1, 100):
                new_name = f"{name} ({i}){extension}"
                new_path = os.path.join(repo_path, new_name)
                if not os.path.isfile(new_path) or os.path.getsize(new_path) == os.path.getsize(path):
                    break
            if new_name != filename:
                os.rename(path, new_path)

# Function to get all the links for the repositories on a given GitHub search results page
def getAllLinks(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    repo_links = soup.find_all("a", {"class": "v-align-middle"})
    links = [link["href"] for link in repo_links]

    for link in links:
        downloadRepo("https://github.com/" + link)

# Call the main function to run the script
main()