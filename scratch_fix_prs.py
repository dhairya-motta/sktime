import json
import subprocess

prs = [10267, 10261, 10256, 10251]
repo = "sktime/sktime"

for pr in prs:
    print(f"\n{'=' * 10} Processing PR {pr} {'=' * 10}")
    subprocess.run(["gh", "pr", "checkout", str(pr), "-R", repo], check=True)

    result = subprocess.run(
        ["gh", "pr", "view", str(pr), "-R", repo, "--json", "files"],
        capture_output=True,
        text=True,
        check=True,
    )
    files_data = json.loads(result.stdout)
    changed_files = [f["path"] for f in files_data["files"]]

    if not changed_files:
        print("No files changed.")
        continue

    print(f"Running pre-commit on: {changed_files}")
    pc_result = subprocess.run(
        ["pre-commit", "run", "--files"] + changed_files, capture_output=True, text=True
    )

    print(pc_result.stdout)
    if pc_result.stderr:
        print("STDERR:", pc_result.stderr)

    status_result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    if status_result.stdout.strip():
        print("Auto-formatting made changes. Committing...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "--no-verify", "-m", "style: run pre-commit"], check=True
        )
        subprocess.run(["git", "push"], check=True)
        print("Pushed changes.")
    else:
        print("No auto-formatting changes made.")
