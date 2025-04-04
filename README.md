# Domestic Background Removal
This tool uses the [rembg](https://github.com/danielgatis/rembg) library to perform background removal on pictures. It's structured as an API.

## Run the app
```
uv sync
uv run rembg.py
```

## Request
After running the API you can access it via POST under `http://127.0.0.1:8008/rembg`. Put the image_url in the request's JSON body.

```curl
curl --location 'http://127.0.0.1:8008/rembg' \
--header 'Content-Type: application/json' \
--data '{"image_url" : "https://upload.wikimedia.org/wikipedia/commons/f/f2/Platypus.jpg"}'
```

```python
import requests
import json

url = "http://127.0.0.1:8008/rembg"

payload = json.dumps({
 "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Platypus.jpg"
})
headers = {
	'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```