import urllib.request, json
req = urllib.request.Request('https://api.github.com/repos/sktime/sktime/issues?per_page=100&state=open', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
issues = json.loads(resp.read())
for i in issues:
    if 'pull_request' not in i and i['comments'] <= 1 and 'fkiraly' not in i['user']['login']:
        text = (i['title'] + ' ' + (i.get('body') or '')).lower()
        if any(w in text for w in ['quant', 'finance', 'forecasting', 'econometrics', 'trading', 'volatility', 'garch', 'arima', 'portfolio', 'vecm', 'var']):
            print(f"#{i['number']}: {i['title']}")
