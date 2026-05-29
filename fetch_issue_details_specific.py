import json
import urllib.request

for repo, issue_num in [
    ("sktime/skpro", 966),
    ("sktime/skpro", 977),
    ("sktime/sktime", 4520),
    ("sktime/skpro", 390),
]:
    url = f"https://api.github.com/repos/{repo}/issues/{issue_num}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(
                f"Issue {repo}#{issue_num} by {data['user']['login']}: {data['title']}"
            )
            print("=" * 40)
            print(data.get("body", "")[:300])
            print("\n" + "-" * 60 + "\n")
    except Exception as e:
        print(f"Failed to fetch {repo}#{issue_num}: {e}")
