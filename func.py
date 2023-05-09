import re, json, os

def extract_role_id(text):
    pattern = r'<@&(\d+)>'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    return None

def check():
    jsonPath = r"./data.json"
    if not os.path.isfile(jsonPath):
        with open(jsonPath, "w") as f:
            f.write(json.dumps({"data": []}, sort_keys=True, indent=4))
