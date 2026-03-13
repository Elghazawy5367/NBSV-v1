import os
from github import Github, GithubException

TOKEN = os.environ["GITHUB_TOKEN"]
REPO_NAME = "Elghazawy5367/NBSV-v1"
SRC_PATH = "tracker/index.html"
DST_PATH = "docs/index.html"

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

print(f"Connected to: {repo.full_name}")

# Step 1: Get the source file
print(f"Reading {SRC_PATH}...")
src_file = repo.get_contents(SRC_PATH)
content = src_file.decoded_content

# Step 2: Create the destination file
print(f"Creating {DST_PATH}...")
try:
    existing = repo.get_contents(DST_PATH)
    repo.update_file(
        path=DST_PATH,
        message=f"Move {SRC_PATH} to {DST_PATH}",
        content=content,
        sha=existing.sha,
    )
    print(f"  Updated existing {DST_PATH}")
except GithubException as e:
    if e.status == 404:
        repo.create_file(
            path=DST_PATH,
            message=f"Move {SRC_PATH} to {DST_PATH}",
            content=content,
        )
        print(f"  Created {DST_PATH}")
    else:
        raise

# Step 3: Delete the source file
print(f"Deleting {SRC_PATH}...")
repo.delete_file(
    path=SRC_PATH,
    message=f"Remove {SRC_PATH} (moved to {DST_PATH})",
    sha=src_file.sha,
)
print(f"  Deleted {SRC_PATH}")

print("\nDone! File successfully moved.")
