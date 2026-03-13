import os
import time
import zipfile
import base64
from github import Github, GithubException

TOKEN = os.environ["GITHUB_TOKEN"]
REPO_NAME = "Elghazawy5367/NBSV-v1"
ZIP_PATH = "attached_assets/nbsv-github-repo_1773407481525.zip"
PREFIX_TO_STRIP = "nbsv-repo/"

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

print(f"Connected to repo: {repo.full_name}")
print(f"Opening zip: {ZIP_PATH}")

skipped = 0
pushed = 0
errors = 0

with zipfile.ZipFile(ZIP_PATH, "r") as zf:
    all_names = zf.namelist()
    files = [n for n in all_names if not n.endswith("/")]
    print(f"Total files in zip: {len(files)}")
    print("-" * 60)

    for i, name in enumerate(files, 1):
        # Strip leading prefix
        if name.startswith(PREFIX_TO_STRIP):
            path = name[len(PREFIX_TO_STRIP):]
        else:
            path = name

        if not path:
            continue

        try:
            content = zf.read(name)
        except Exception as e:
            print(f"[{i}/{len(files)}] ERROR reading {name}: {e}")
            errors += 1
            continue

        # Try to push/update
        try:
            try:
                existing = repo.get_contents(path)
                repo.update_file(
                    path=path,
                    message=f"Update {path}",
                    content=content,
                    sha=existing.sha,
                )
                print(f"[{i}/{len(files)}] UPDATED: {path}")
            except GithubException as ge:
                if ge.status == 404:
                    repo.create_file(
                        path=path,
                        message=f"Add {path}",
                        content=content,
                    )
                    print(f"[{i}/{len(files)}] CREATED: {path}")
                else:
                    raise

            pushed += 1
        except Exception as e:
            print(f"[{i}/{len(files)}] ERROR pushing {path}: {e}")
            errors += 1
            continue

        time.sleep(0.3)

print("-" * 60)
print(f"Done. Pushed: {pushed}, Skipped: {skipped}, Errors: {errors}")
