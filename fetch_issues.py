import urllib.request, json
req = urllib.request.Request('https://api.github.com/repos/sktime/sktime/issues?per_page=100&state=open', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
issues = json.loads(resp.read())
filtered = [i for i in issues if 'pull_request' not in i and i['comments'] <= 1 and i['user']['login'] != 'fkiraly']
for i in filtered:
    labels = [l['name'] for l in i['labels']]
    print(f"#{i['number']}: {i['title']} | Comments: {i['comments']} | Labels: {labels}")
