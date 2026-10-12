"""README의 LANGUAGES 마커 사이를 소유 레포 전체의 언어 비중으로 갱신한다.

GH_TOKEN이 사용자 PAT면 private 레포까지, 아니면 public 레포만 집계한다.
사용: python3 languages.py <owner> <README 경로>
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

LIMIT = 8   # 표시할 언어 수 (나머지는 Other)
BAR = 25    # 막대 길이
START, END = "<!-- LANGUAGES:START -->", "<!-- LANGUAGES:END -->"


def get(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if os.environ.get("GH_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GH_TOKEN']}")
    with urllib.request.urlopen(req) as res:
        return json.load(res)


def paged(path):
    page = 1
    while True:
        items = get(f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        yield from items
        if len(items) < 100:
            return
        page += 1


def owned_repos(owner):
    try:
        repos = list(paged("/user/repos?affiliation=owner"))
    except urllib.error.HTTPError:
        # Actions 기본 토큰은 /user 접근 불가 → public 레포만
        repos = list(paged(f"/users/{owner}/repos?type=owner"))
    return [r for r in repos
            if r["owner"]["login"].lower() == owner.lower()
            and not r["fork"]
            and r["name"].lower() != owner.lower()]


def render(totals, repo_count):
    total = sum(totals.values())
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    rows = ranked[:LIMIT]
    rest = sum(v for _, v in ranked[LIMIT:])
    if rest:
        rows.append(("Other", rest))
    width = max(len(name) for name, _ in rows)
    lines = []
    for name, size in rows:
        pct = 100 * size / total
        filled = round(BAR * size / total)
        lines.append(f"{name:<{width}}  {'█' * filled}{'░' * (BAR - filled)}  {pct:5.1f}%")
    return "\n".join([
        START,
        "```text",
        *lines,
        "```",
        f"<sub>레포 {repo_count}개의 코드량(bytes) 기준 · 매시간 자동 갱신</sub>",
        END,
    ])


def main(owner, readme):
    repos = owned_repos(owner)
    totals = {}
    for r in repos:
        for lang, size in get(f"/repos/{r['full_name']}/languages").items():
            totals[lang] = totals.get(lang, 0) + size
    block = render(totals, len(repos))
    print(block)

    text = open(readme, encoding="utf-8").read()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        sys.exit(f"{readme}에 {START} / {END} 마커가 없음")
    open(readme, "w", encoding="utf-8").write(pattern.sub(lambda _: block, text))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
