import json
import urllib.request

for repo, issue_num in [("sktime/sktime", 6548), ("sktime/skpro", 369)]:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_num}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"Issue {repo}#{issue_num}: {data['title']}")
            print("=" * 40)
            print(data.get("body", ""))
            print("\n" + "-" * 60 + "\n")
    except Exception as e:
        print(f"Failed to fetch {repo}#{issue_num}: {e}")
