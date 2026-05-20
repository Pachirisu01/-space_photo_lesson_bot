import os
import requests

def download_image(url, filepath):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open(filepath, 'wb') as f:
        f.write(response.content)

def get_file_extension(url):
    _, ext = os.path.splitext(url.split("/")[-1])
    return ext.lower() if ext else ".jpg"