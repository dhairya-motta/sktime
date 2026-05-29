import urllib.request, json
issues = [10240, 10255, 10236, 10204, 10202, 10200]
clean_issues = []
for i in issues:
    req = urllib.request.Request(f'https://api.github.com/repos/sktime/sktime/issues/{i}/timeline', headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.mockingbird-preview'})
    resp = urllib.request.urlopen(req)
    events = json.loads(resp.read())
    has_commits = any(e['event'] in ['cross-referenced', 'connected', 'referenced', 'committed'] for e in events)
    if not has_commits:
        clean_issues.append(i)
print("CLEAN ISSUES:", clean_issues)
