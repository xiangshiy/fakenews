import json

with open("./content5.json", "w", encoding="utf-8") as f:
    data = []
    with open("./[OCR]_content3_20240121_1500.json", "r", encoding="utf-8") as q:
        line = q.readline()
        while line != "":
            # data.append(eval(line))
            data_ = eval(line)
            data__ = data_["data"]
            result = ""
            flag = False
            for i in data__:
                if i["text"] == "真相":
                    flag = True
                    continue
                if flag:
                    if i["text"].startswith("（来源"):
                        break
                    result += i["text"]
            if result != "":
                data.append({
                    "proveId": data_["fileName"].split(".")[0],
                    "content": result
                })
            line = q.readline()
    json.dump(data, f, indent=4, skipkeys=True, ensure_ascii=False)
