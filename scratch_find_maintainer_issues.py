import json
import re
import time
import urllib.parse
import urllib.request


def fetch_issues():
    query = "repo:sktime/sktime is:issue is:open no:assignee author:fkiraly"
    url = (
        "https://api.github.com/search/issues?q="
        + urllib.parse.quote(query)
        + "&per_page=100"
    )

    issues = []
    for page in range(1, 4):
        try:
            req = urllib.request.Request(
                f"{url}&page={page}", headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                issues.extend(data.get("items", []))
            time.sleep(2)
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    query2 = "repo:sktime/sktime is:issue is:open no:assignee author:ciaran-g"
    url2 = (
        "https://api.github.com/search/issues?q="
        + urllib.parse.quote(query2)
        + "&per_page=100"
    )
    try:
        req = urllib.request.Request(
            f"{url2}&page={1}", headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            issues.extend(data.get("items", []))
    except Exception:
        pass

    return issues


issues = fetch_issues()

quant_keywords = re.compile(
    r"\b(volatility|garch|arch|arima|stochastic|markov|kalman|probabilistic|distribution|quantile|copula|covariance|vecm|state space|hmm|bayesian|mcmc|heteroskedastic|prediction interval|vector autoregression|cointegration|statsmodels)\b",
    re.IGNORECASE,
)

print(f"Total maintainer unassigned issues fetched: {len(issues)}")
count = 0

for issue in issues:
    if "pull_request" in issue:
        continue

    title = issue["title"]
    body = issue.get("body") or ""
    labels = [l["name"] for l in issue.get("labels", [])]
    comments = issue.get("comments", 0)

    # Ignore issues that have lots of comments (someone is probably working on it or it's contentious)
    if comments > 3:
        continue

    if (
        quant_keywords.search(title)
        or "module:proba" in labels
        or quant_keywords.search(body)
    ):
        print(f"#{issue['number']}: {title}")
        print(f"Author: {issue['user']['login']}")
        print(f"Comments: {comments}")
        print(f"URL: {issue['html_url']}")
        print("Body snippet: " + body[:200].replace("\n", " "))
        print("-" * 60)
        count += 1
        if count >= 10:
            break
