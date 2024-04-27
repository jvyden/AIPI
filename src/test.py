import requests
import json
import pprint

def main():
    with open("cat.jpg", "rb") as f:
        image_bytes = f.read()

    url = "http://localhost:5000/eva/predict?threshold=0.75"
    response = requests.post(url, data=image_bytes, headers={'Content-Type': 'application/octet-stream'})

    content_type = response.headers.get("Content-Type")
    if content_type and content_type == "application/json":
        print(pprint.pformat(response.json(), compact=False))
    else:
        print(response.text)

if __name__ == "__main__":
    main()