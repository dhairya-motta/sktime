import json
import urllib.request

issues = [5588, 4431, 4420, 5586]
for issue_num in issues:
    print(f"=== Issue/PR #{issue_num} ===")
    url = f"https://api.github.com/repos/sktime/sktime/issues/{issue_num}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print("Title:", data.get("title"))
            print("Author:", data.get("user", {}).get("login"))
            body = data.get("body") or ""
            print("Body:", body[:500].replace("\n", " ") + "...")

            # Fetch comments
            comments_url = data.get("comments_url")
            if comments_url:
                creq = urllib.request.Request(
                    comments_url, headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(creq) as cresponse:
                    cdata = json.loads(cresponse.read().decode())
                    for idx, c in enumerate(cdata[:3]):
                        c_body = c.get("body") or ""
                        print(
                            f" Comment {idx + 1} by {c.get('user', {}).get('login')}: {c_body[:200].replace(chr(10), ' ')}"
                        )
            print("\n")
    except Exception as e:
        print(f"Error fetching {issue_num}:", e)
