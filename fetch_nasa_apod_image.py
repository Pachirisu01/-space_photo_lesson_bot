import os
import argparse
import requests
from datetime import datetime, timedelta
from general_utils import create_folder, download_image, get_file_extension


def fetch_nasa_apod(api_key, count=1, date=None, folder="images"):
    create_folder(folder)

    apod_urls = []

    if date:
        dates_to_check = [date]
    else:
        dates_to_check = []
        today = datetime.now()
        for day_offset in range(count * 3):
            dates_to_check.append(today - timedelta(days=day_offset))

    for check_date in dates_to_check:
        if len(apod_urls) >= count:
            break

        try:
            url = "https://api.nasa.gov/planetary/apod"
            params = {"api_key": api_key, "date": check_date.strftime("%Y-%m-%d")}
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get('media_type') == 'image':
                    image_url = data.get('url')
                    if image_url:
                        apod_urls.append(image_url)
        except Exception:
            continue

    if not apod_urls:
        return False

    for i, image_url in enumerate(apod_urls[:count], 1):
        ext = get_file_extension(image_url)
        filename = f"apod_{i:03d}{ext}"
        filepath = os.path.join(folder, filename)
        if download_image(image_url, filepath):
            print(f"apod_{i:03d}{ext}")

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', required=True)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--date')
    parser.add_argument('--folder', default='images')

    args = parser.parse_args()

    if args.date:
        try:
            date_obj = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("Неверный формат даты. Используйте YYYY-MM-DD")
            return
    else:
        date_obj = None

    if not fetch_nasa_apod(api_key=args.api_key, count=args.count, date=date_obj, folder=args.folder):
        print("Не удалось получить изображения NASA APOD")


if __name__ == '__main__':
    main()