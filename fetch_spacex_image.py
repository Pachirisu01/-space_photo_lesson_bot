import os
import argparse
import requests
from general_utils import  download_image, get_file_extension


def fetch_spacex_images(folder="images", count=10):
    os.makedirs(folder, exist_ok=True)

    try:
        response = requests.get("https://api.spacexdata.com/v4/launches/latest")
        response.raise_for_status()
        launch_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети или HTTP: {e}")
        return False
    except ValueError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return False


    flickr_original = launch_data.get('links', {}).get('flickr', {}).get('original')
    if not flickr_original:
        print("У последнего запуска нет фотографий в Flickr.")
        return False


    image_urls = flickr_original[:count]
    if not image_urls:
        return False


    for img_number, image_url in enumerate(image_urls, 1):
        ext = get_file_extension(image_url)
        filename = f"spacex_{img_number:03d}{ext}"
        filepath = os.path.join(folder, filename)
        if download_image(image_url, filepath):
            print(f"spacex_{img_number:03d}{ext}")
        else:
            print(f"Не удалось скачать {image_url}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Скачивает изображения Earth Polychromatic Imaging Camera (EPIC) с NASA EPIC API"
    )
    parser.add_argument('--count', type=int, default=10,
                        help='количество изображений (По умолчанию 10')
    parser.add_argument('--folder', default='images',
                        help='папка для сохранения(По умолчанию папка images ')
    args = parser.parse_args()

    if not fetch_spacex_images(folder=args.folder, count=args.count):
        print("Не удалось получить изображения SpaceX")


if __name__ == '__main__':
    main()