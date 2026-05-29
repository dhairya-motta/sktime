import urllib.request, json
req = urllib.request.Request('https://api.github.com/repos/sktime/sktime/issues/10173/timeline', headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.mockingbird-preview'})
resp = urllib.request.urlopen(req)
events = json.loads(resp.read())
for e in events:
    if e['event'] in ['cross-referenced', 'connected', 'referenced']:
        print(e['event'])
        print(e.get('source', {}).get('issue', {}).get('html_url') or e.get('commit_id') or e.get('commit_url'))
