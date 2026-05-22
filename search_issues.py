import json
import urllib.request


def search_issues(repo, query):
    url = f"https://api.github.com/search/issues?q=repo:{repo}+is:open+is:issue+{query}"
    print(f"Fetching: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("items", [])
    except Exception as e:
        print(f"Error fetching {repo}: {e}")
        return []


def print_issues(repo, items):
    if not items:
        print(f"No issues found for {repo}.")
        return
    for item in items:
        print(f"Issue #{item['number']}: {item['title']}")
        print(f"URL: {item['html_url']}")
        print(f"Comments: {item['comments']}")
        print("-" * 40)


queries = [
    "quantile author:fkiraly comments:0",
    "quantile comments:0",
    "probabilistic author:fkiraly comments:0",
]

for repo in ["sktime/sktime", "sktime/skpro"]:
    print(f"\n{'=' * 20} {repo} {'=' * 20}")
    for q in queries:
        print(f"\nQuery: {q}")
        query_str = "+".join(q.split())
        items = search_issues(repo, query_str)
        print_issues(repo, items)
