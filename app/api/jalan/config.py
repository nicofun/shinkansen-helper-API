import json

JALAN_API_KEY = json.load(open("api/settings.json", "r", encoding="utf8"))["jalan"]["key"]