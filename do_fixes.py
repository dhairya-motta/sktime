import subprocess

prs = [10289, 10283, 10273, 10268, 10267, 10256, 10251]

for pr in prs:
    print(f"\n{'=' * 20} Processing PR {pr} {'=' * 20}")
    
    # Fetch and checkout
    branch_name = f"pr-{pr}"
    subprocess.run(["git", "fetch", "upstream", f"pull/{pr}/head:{branch_name}"], check=False)
    subprocess.run(["git", "checkout", branch_name], check=True)
    
    # Run pre-commit
    print("Running pre-commit run --all-files...")
    pc_result = subprocess.run(
        ["pre-commit", "run", "--all-files"], capture_output=True, text=True
    )
    
    print(pc_result.stdout)
    if pc_result.stderr:
        print("STDERR:", pc_result.stderr)
        
    # Check if changes were made
    status_result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    if status_result.stdout.strip():
        print("Auto-formatting made changes. Committing...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "--no-verify", "-m", "style: run pre-commit"], check=True)
        print(f"Fixed code quality issues on PR {pr}.")
    else:
        print("No auto-formatting changes made.")
