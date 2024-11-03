import requests
import os


"""
This script downloads all .py files from the specified GitHub repository.
"""


OWNER = "Matthev00"
REPO = "Oxford_Pet_Recognition"


def fetch_py_files(path=""):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    response = requests.get(url)
    items = response.json()

    for item in items:
        if item["type"] == "dir":
            fetch_py_files(item["path"])
        elif item["type"] == "file" and item["name"].endswith(".py"):
            file_url = item["download_url"]
            file_content = requests.get(file_url).text

            os.makedirs(os.path.dirname("data/raw/" + item["path"]), exist_ok=True)
            with open("data/raw/" + item["path"], "w") as f:
                f.write(file_content)
            print(f"Pobrano: {item['path']}")


def main():
    fetch_py_files()


if __name__ == "__main__":
    main()
