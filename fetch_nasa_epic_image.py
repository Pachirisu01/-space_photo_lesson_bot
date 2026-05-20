import os
import argparse
import requests
from datetime import datetime
from general_utils import get_file_extension, download_image


def fetch_epic_metadata(api_key, date=None):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}
    if date:
        params["date"] = date

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError("API вернул пустой список изображений")
    return data


def build_epic_urls(metadata, count):
    base_urls = []
    for item in metadata[:count]:
        if "date" not in item or "image" not in item:
            print("Пропущено изображение: отсутствуют ключи 'date' или 'image'")
            continue

        date_str = item["date"]
        image_name = item["image"]

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            print(f"Пропущено изображение: неверный формат даты '{date_str}'")
            continue

        year = date_obj.strftime("%Y")
        month = date_obj.strftime("%m")
        day = date_obj.strftime("%d")
        url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
        base_urls.append(url)

    return base_urls


def download_epic_images(urls, api_key, folder):
    downloaded = 0
    for img_number, url in enumerate(urls, 1):
        full_url = f"{url}?api_key={api_key}"
        ext = get_file_extension(url)
        filename = f"epic_{img_number:03d}{ext}"
        filepath = os.path.join(folder, filename)
        download_image(full_url, filepath):
    return downloaded


def fetch_nasa_epic(api_key, count=10, date=None, folder="images"):
    abs_folder = os.path.abspath(folder)
    os.makedirs(folder, exist_ok=True)

    metadata = fetch_epic_metadata(api_key, date)
    urls = build_epic_urls(metadata, count)

    if not urls:
        return False

    downloaded = download_epic_images(urls, api_key, folder)
    return downloaded > 0

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
    try:
        fetch_nasa_epic(api_key=api_key, count=args.count, date=args.date, folder=args.folder)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к EPIC API: {e}")
    except ValueError as e:
        print(f"Ошибка обработки данных: {e}")
    except RuntimeError as e:
        print(f"Ошибка при скачивании: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == '__main__':
    main()