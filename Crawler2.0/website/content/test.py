import json

keys = []
with open("./content3.json", "w+", encoding="utf-8") as f:
    js = json.load(f)
    f.seek(0)
    for i in js:
        i["keyword"] = i["keyword"][4:]
    json.dump(js, f, indent=4, skipkeys=True, ensure_ascii=False)
