import json
import re
import urllib.request

repo = "sktime/pytorch-forecasting"
url = f"https://api.github.com/repos/{repo}/issues?state=open&creator=fkiraly&per_page=100"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        issues = json.loads(response.read().decode())
except Exception as e:
    print("Error:", e)
    issues = []

quant_keywords = re.compile(
    r"\b(volatility|garch|arch|arima|stochastic|markov|kalman|probabilistic|distribution|quantile|copula|covariance|vecm|state space|hmm|bayesian|mcmc|heteroskedastic|prediction interval|loss|metric|conformal)\b",
    re.IGNORECASE,
)

print(f"Quant-related issues by fkiraly in {repo}:")
count = 0
for issue in issues:
    if "pull_request" in issue:
        continue

    title = issue["title"]
    body = issue.get("body") or ""

    if quant_keywords.search(title) or quant_keywords.search(body):
        print(f"#{issue['number']}: {title}")
        print(f"URL: {issue['html_url']}")
        print(f"Comments: {issue['comments']}")
        print("-" * 40)
        count += 1
        if count >= 10:
            break

if count == 0:
    print(
        "No quanty issues found by fkiraly in pytorch-forecasting. Checking sktime/sktime instead..."
    )
    url = "https://api.github.com/repos/sktime/sktime/issues?state=open&creator=fkiraly&per_page=100"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            issues = json.loads(response.read().decode())
        for issue in issues:
            if "pull_request" in issue:
                continue
            title = issue["title"]
            body = issue.get("body") or ""
            if issue["comments"] == 0 and (
                quant_keywords.search(title) or quant_keywords.search(body)
            ):
                print(f"sktime #{issue['number']}: {title}")
                print(f"URL: {issue['html_url']}")
                print(f"Comments: {issue['comments']}")
                print("-" * 40)
                count += 1
                if count >= 10:
                    break
    except Exception as e:
        print("Error fetching sktime:", e)
