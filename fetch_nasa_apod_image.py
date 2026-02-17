import os
import argparse
import requests
from datetime import datetime, timedelta
from general_utils import download_image, get_file_extension


def fetch_nasa_apod(api_key, count=1, date=None, folder="images"):
    os.makedirs(folder, exist_ok=True)
    apod_urls = []

    if date:
        dates_to_check = [date]
    else:
        today = datetime.now()
        dates_to_check = [today - timedelta(days=i) for i in range(count * 3)]

    for check_date in dates_to_check:
        if len(apod_urls) >= count:
            break

        try:
            url = "https://api.nasa.gov/planetary/apod"
            params = {
                "api_key": api_key,
                "date": check_date.strftime("%Y-%m-%d")
            }
            response = requests.get(url, params=params, timeout=10)
            if not response.ok:
                print(f"HTTP {response.status_code} для {check_date.strftime('%Y-%m-%d')}")
                continue
            data = response.json()

            if data.get('media_type') != 'image':
                continue
            image_url = data.get('url')
            if not image_url:
                continue
            apod_urls.append(image_url)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса для даты {check_date.strftime('%Y-%m-%d')}: {e}")
            continue
        except ValueError as e:
            print(f"Ошибка обработки JSON для даты {check_date.strftime('%Y-%m-%d')}: {e}")
            continue
        except (KeyError, TypeError, AttributeError) as e:
            print(f"Ошибка данных для даты {check_date.strftime('%Y-%m-%d')}: {e}")
            continue

    if not apod_urls:
        return False

    for img_number, image_url in enumerate(apod_urls[:count], 1):
        ext = get_file_extension(image_url)
        filename = f"apod_{img_number:03d}{ext}"
        filepath = os.path.join(folder, filename)
        if download_image(image_url, filepath):
            print(f"apod_{img_number:03d}{ext}")

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Скачивает изображения с NASA APOD API"
    )
    parser.add_argument('--count', type=int, default=1,
                        help='количество изображений (По умолчанию 1')
    parser.add_argument('--date',
                        help='конкретная дата в формате YYYY-MM-DD')
    parser.add_argument('--folder', default='images',
                        help='папка для сохранения (По умолчанию images)')

    args = parser.parse_args()

    api_key = os.environ.get('NASA_API_KEY')
    if not api_key:
        print("Ошибка: необходимо установить переменную окружения NASA_API_KEY")
        return

    if args.date:
        try:
            date_obj = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("Неверный формат даты. Используйте YYYY-MM-DD")
            return
    else:
        date_obj = None

    if not fetch_nasa_apod(api_key=api_key,
                           count=args.count,
                           date=date_obj,
                           folder=args.folder):
        print("Не удалось получить изображения NASA APOD")

if __name__ == '__main__':
    main()