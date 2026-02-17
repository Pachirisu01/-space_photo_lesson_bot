import os, random, telegram, time
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv("TOKEN")

bot = telegram.Bot(token=TOKEN)

chat_id = os.getenv("CHAT_ID")

delay_hours_str = os.getenv("DELAY_HOURS")

while True:
    try:
        delay_hours = float(delay_hours_str)
        images = os.listdir("images")
        with open(os.path.join('images', random.choice(images)), 'rb') as photo:
            bot.send_photo(chat_id=chat_id, photo=photo, caption='New photo in channel!')
        time.sleep(delay_hours * 3600)
    except KeyboardInterrupt:
        break
    except Exception:
        time.sleep(60)