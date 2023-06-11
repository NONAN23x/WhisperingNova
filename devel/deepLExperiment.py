import time
import requests
import json
import sys

startTime = time.time()

def make_deep_translate(text, source_lang, target_land):
    base_url = 'http://localhost:8080'
    data = {"text": text,
                "source_lang": source_lang,
                "target_lang": target_land}
    jsonData = json.dumps(data)
    print(jsonData)
    r = requests.post(f'{base_url}/translate', data=jsonData)

    
    return r.json()


def main():
    text = sys.argv[1]
    response = make_deep_translate(text, source_lang="EN", target_land="JA")
    print(response)

main()

endTime = time.time()

total = abs(endTime - startTime)
print(f"Program took {total} seconds.")