import json
jsonPath = r"./keyword.json"

def loadJson():
    with open(jsonPath, 'r') as f:
        data = json.load(f)
        print(data["keyword"])
    return data

def writeJson(content):
    data = loadJson()
    for keyword in content:
        data['keyword'].remove(keyword)

    with open(jsonPath, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# testdata = ['聽說']

# writeJson(testdata)

msg = "聽說, 聽說, 聽說, "

print(msg[:-2])