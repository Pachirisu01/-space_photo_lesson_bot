import os
import argparse
import requests
from datetime import datetime
from general_utils import  download_image, get_file_extension


def fetch_nasa_epic(api_key, count=10, date=None, folder="images"):
    os.makedirs(folder, exist_ok=True)

    try:
        url = "https://api.nasa.gov/EPIC/api/natural/images"
        params = {"api_key": api_key}
        if date:
            params["date"] = date

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к EPIC API: {e}")
        return False
    except ValueError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return False

    if not data:
        return False

    base_urls = []
    for item in data[:count]:
        try:
            date_str = item["date"]
            image_name = item["image"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            year = date_obj.strftime("%Y")
            month = date_obj.strftime("%m")
            day = date_obj.strftime("%d")
            base_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
            base_urls.append(base_url)
        except (KeyError, ValueError, TypeError) as e:
            print(f"Пропущено изображение из-за ошибки: {e}")
            continue

    if not base_urls:
        return False


    session = requests.Session()
    for img_number, base_url in enumerate(base_urls, 1):
        try:
            params = {"api_key": api_key}
            response = session.get(base_url, params=params, stream=True, timeout=10)
            response.raise_for_status()

            ext = get_file_extension(base_url)
            filename = f"epic_{img_number:03d}{ext}"
            filepath = os.path.join(folder, filename)

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"epic_{img_number:03d}{ext}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании {base_url}: {e}")
            continue

    return True
def main():
    parser = argparse.ArgumentParser(
        description="Скачивает изображения с NASA EPIC API"
    )
    parser.add_argument('--count', type=int, default=10,
                        help='количество изображений (По умолчанию 10)')
    parser.add_argument('--date',
                        help='конкретная дата в формате YYYY-MM-DD')
    parser.add_argument('--folder', default='images',
                        help='папка для сохранения (По умолчанию images)')
    args = parser.parse_args()

    api_key = os.environ.get('NASA_API_KEY')
    if not api_key:
        print("Ошибка: необходимо установить переменную окружения NASA_API_KEY")
        return

    if not fetch_nasa_epic(api_key=api_key, count=args.count, date=args.date, folder=args.folder):
        print("Не удалось получить изображения NASA EPIC")

if __name__ == '__main__':
    main()