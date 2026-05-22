import json
import re
import urllib.request

url = "https://api.github.com/repos/sktime/sktime/issues?state=open&per_page=100"
issues = []
for page in range(1, 6):
    try:
        req = urllib.request.Request(
            f"{url}&page={page}", headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            issues.extend(data)
    except Exception:
        pass

quant_keywords = re.compile(
    r"\b(volatility|garch|arch|arima|stochastic|markov|kalman|probabilistic|distribution|quantile|copula|covariance|vecm|state space|hmm|bayesian|mcmc|heteroskedastic|prediction interval)\b",
    re.IGNORECASE,
)

print("Quant-related issues:")
count = 0
for issue in issues:
    if "pull_request" in issue:
        continue

    title = issue["title"]
    body = issue.get("body") or ""
    labels = [l["name"] for l in issue.get("labels", [])]

    if (
        quant_keywords.search(title)
        or "module:proba" in labels
        or ("module:forecasting" in labels and quant_keywords.search(body))
    ):
        if "good first issue" not in labels:
            print(f"#{issue['number']}: {title}")
            print(f"URL: {issue['html_url']}")
            print("-" * 40)
            count += 1
            if count >= 10:
                break
