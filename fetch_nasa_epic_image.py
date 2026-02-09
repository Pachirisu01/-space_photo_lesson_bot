import os
import argparse
import requests
from datetime import datetime
from general_utils import create_folder, download_image, get_file_extension


def fetch_nasa_epic(api_key="DEMO_KEY", count=10, date=None, folder="images"):
    create_folder(folder)

    try:
        url = "https://api.nasa.gov/EPIC/api/natural/images"
        params = {"api_key": api_key}

        if date:
            params["date"] = date

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return False

        data = response.json()

        if not data:
            return False

        image_urls = []

        for item in data[:count]:
            try:
                date_str = item["date"]
                image_name = item["image"]

                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                year = date_obj.strftime("%Y")
                month = date_obj.strftime("%m")
                day = date_obj.strftime("%d")

                image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={api_key}"
                image_urls.append(image_url)
            except Exception:
                continue

        if not image_urls:
            return False

        for i, image_url in enumerate(image_urls, 1):
            ext = get_file_extension(image_url)
            filename = f"epic_{i:03d}{ext}"
            filepath = os.path.join(folder, filename)
            if download_image(image_url, filepath):
                print(f"epic_{i:03d}{ext}")

        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', default="DEMO_KEY")
    parser.add_argument('--count', type=int, default=10)
    parser.add_argument('--date')
    parser.add_argument('--folder', default='images')

    args = parser.parse_args()

    if not fetch_nasa_epic(api_key=args.api_key, count=args.count, date=args.date, folder=args.folder):
        print("Не удалось получить изображения NASA EPIC")


if __name__ == '__main__':
    main()