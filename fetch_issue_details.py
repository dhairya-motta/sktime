import json
import urllib.request

for issue_num in [10189, 9634, 9904]:
    url = f"https://api.github.com/repos/sktime/sktime/issues/{issue_num}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"Issue #{issue_num}: {data['title']}")
            print("=" * 40)
            print(data.get("body", "")[:1000] + "...\n")
    except Exception as e:
        print(f"Failed to fetch {issue_num}: {e}")
