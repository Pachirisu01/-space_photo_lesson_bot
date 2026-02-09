import os
import argparse
import requests
from general_utils import create_folder, download_image, get_file_extension


def fetch_spacex_images(launch_id=None, folder="images", count=10):
    create_folder(folder)

    if launch_id:
        url = f"https://api.spacexdata.com/v4/launches/{launch_id}"
    else:
        url = "https://api.spacexdata.com/v4/launches/latest"

    try:
        response = requests.get(url)
        response.raise_for_status()
        launch_data = response.json()

        if 'links' not in launch_data or 'flickr' not in launch_data['links'] or 'original' not in launch_data['links'][
            'flickr']:
            return False

        image_urls = launch_data['links']['flickr']['original'][:count]

        if not image_urls:
            return False

        for i, image_url in enumerate(image_urls, 1):
            ext = get_file_extension(image_url)
            filename = f"spacex_{i:03d}{ext}"
            filepath = os.path.join(folder, filename)
            if download_image(image_url, filepath):
                print(f"spacex_{i:03d}{ext}")

        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', default=None)
    parser.add_argument('--folder', default='images')
    parser.add_argument('--count', type=int, default=10)

    args = parser.parse_args()

    if not fetch_spacex_images(launch_id=args.id, folder=args.folder, count=args.count):
        print("Не удалось получить изображения SpaceX")


if __name__ == '__main__':
    main()