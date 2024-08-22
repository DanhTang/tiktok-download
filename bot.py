import logging
import requests
import re
import asyncio
from aiogram import Bot, Dispatcher, types, Router
import yt_dlp

# Cấu hình header
headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X22; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})

# Thêm token của bạn vào đây
API_TOKEN = '6879930539:AAHJdB2e8I4pIHSyXejGEx5xlxcuz-JbdzI'

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

# Khởi tạo bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

@router.message()
async def echo(message: types.Message):
    username = message.chat  # Tên người dùng trên Telegram
    xurl = message.text  # URL đầy đủ

    if "https://vm.tiktok.com/" in xurl or "https://www.tiktok.com/@" in xurl:
        await message.answer("[+] Please Wait")
        try:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
                'outtmpl': '%(id)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(xurl, download=False)
                video_url = info_dict.get("url", None)
                if video_url:
                    await message.answer("[+] Done! " + video_url)
                else:
                    await message.answer("[+] Error: Could not find video URL.")
        except Exception as e:
            await message.answer(f"[+] Error: {str(e)}")
    else:
        await message.answer("[+] invalid url")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
