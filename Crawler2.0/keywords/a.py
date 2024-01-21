import json

with open("./3.json", "r", encoding="utf-8") as f:
    a = json.load(f)
    for i in a:
        i["keyword_order"] = int(i["keyword_order"])
    with open("./3+.json", "w+", encoding="utf-8") as fg:
        json.dump(a, fg, indent=4, ensure_ascii=False)
