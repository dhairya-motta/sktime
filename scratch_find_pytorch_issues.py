import json
import re
import urllib.request

repo = "sktime/pytorch-forecasting"
url = f"https://api.github.com/repos/{repo}/issues?state=open&per_page=100"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        issues = json.loads(response.read().decode())
except urllib.error.HTTPError as e:
    if e.code == 404:
        print(f"Repo {repo} not found. Trying jdb78/pytorch-forecasting...")
        repo = "jdb78/pytorch-forecasting"
        url = f"https://api.github.com/repos/{repo}/issues?state=open&per_page=100"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            issues = json.loads(response.read().decode())
    else:
        raise

quant_keywords = re.compile(
    r"\b(volatility|garch|arch|arima|stochastic|markov|kalman|probabilistic|distribution|quantile|copula|covariance|vecm|state space|hmm|bayesian|mcmc|heteroskedastic|prediction interval|loss|metric)\b",
    re.IGNORECASE,
)

print(f"Quant-related issues in {repo}:")
count = 0
for issue in issues:
    if "pull_request" in issue:
        continue

    title = issue["title"]
    body = issue.get("body") or ""

    # Exclude if fkiraly commented or created it
    # We can't easily check all comments in one go without another API request, but we check author first.
    if issue["user"]["login"] == "fkiraly":
        continue

    if issue["comments"] > 0:
        continue  # "no comment"

    if quant_keywords.search(title) or quant_keywords.search(body):
        print(f"#{issue['number']}: {title}")
        print(f"URL: {issue['html_url']}")
        print(f"Author: {issue['user']['login']}")
        print("-" * 40)
        count += 1
        if count >= 15:
            break
