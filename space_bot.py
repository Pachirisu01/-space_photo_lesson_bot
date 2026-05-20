import os, random, telegram, time
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()

    TOKEN = os.getenv("TG_TOKEN")

    bot = telegram.Bot(token=TOKEN)

    chat_id = os.getenv("TG_CHAT_ID")

    delay_hours = float(os.getenv("DELAY_HOURS", 0)) * 3600

    while True:
        try:
            images = os.listdir("images")
            if not images:
                raise FileNotFoundError
            with open(os.path.join('images', random.choice(images)), 'rb') as photo:
                bot.send_photo(chat_id=chat_id, photo=photo, caption='New photo in channel!')
            time.sleep(delay_hours)
        except FileNotFoundError:
            print("Папка images пуста, повтор через 60с")
            time.sleep(60)
        except PermissionError:
            print("Нет доступа к папке, повтор через 60с")
            time.sleep(60)
        except telegram.error.TelegramError as e:
            print(f"Ошибка Telegram: {e}, повтор через 60с")
            time.sleep(60)
        except KeyboardInterrupt:
            break
        except (OSError, ValueError) as e:
            print(f"Ошибка ввода-вывода или преобразования: {e}, повтор через 60с")
            time.sleep(60)