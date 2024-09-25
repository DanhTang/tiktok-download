# import logging
# import requests
# import re
# import asyncio
# from aiogram import Bot, Dispatcher, types
# import yt_dlp
# import os

# # Cấu hình header
# headers = requests.utils.default_headers()
# headers.update({'User-Agent': 'Mozilla/5.0 (X22; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})

# # Thêm token của bạn vào đây
# API_TOKEN = os.getenv('TOKEN')

# # Cấu hình logging
# logging.basicConfig(level=logging.INFO)

# # Khởi tạo bot
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)

# @dp.message_handler()
# async def echo(message: types.Message):
#     xurl = message.text  # URL đầy đủ

#     # Kiểm tra nếu URL chứa "tiktok.com"
#     if "tiktok.com" in xurl:
#         await message.answer("[+] Please Wait")
#         try:
#             ydl_opts = {
#                 'format': 'best',
#                 'quiet': True,
#                 'outtmpl': '%(id)s.%(ext)s',
#             }
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info_dict = ydl.extract_info(xurl, download=True)
#                 video_url = info_dict.get("url", None)
#                 title = info_dict.get("title", "Không tìm thấy tiêu đề")
                
#                 if video_url:
#                     await message.answer(title)
#                     await message.answer(f"URL: {video_url}")
#                 else:
#                     await message.answer("[+] Error: Could not find video URL.")
#         except Exception as e:
#             await message.answer(f"[+] Error: {str(e)}")
#     # else:
#     #     await message.answer("[+] invalid url")

# async def main():
#     await dp.start_polling()

# if __name__ == '__main__':
#     asyncio.run(main())



import logging
import requests
import re
import asyncio
from aiogram import Bot, Dispatcher, types
import yt_dlp
import os
from urllib.parse import urlparse, parse_qs, urlencode

# Cấu hình header
headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X22; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})

# Thêm token của bạn vào đây
API_TOKEN = os.getenv('TOKEN')

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

# Khởi tạo bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
    xurl = message.text  # URL đầy đủ

    # Kiểm tra nếu URL chứa "tiktok.com"
    if "tiktok.com" in xurl:
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
                title = info_dict.get("title", "Không tìm thấy tiêu đề")
                
                if video_url:
                    # Chuyển đổi video_url sang định dạng cũ
                    parsed_url = urlparse(video_url)
                    query_params = parse_qs(parsed_url.query)

                    # Sắp xếp các tham số theo thứ tự mong muốn
                    new_params = {
                        "video_id": query_params.get("video_id", [""])[0],
                        "line": query_params.get("line", ["0"])[0],
                        "is_play_url": query_params.get("is_play_url", ["1"])[0],
                        "file_id": query_params.get("file_id", [""])[0],
                        "item_id": query_params.get("item_id", [""])[0],
                        "signaturev3": query_params.get("signaturev3", [""])[0],
                        "shp": query_params.get("shp", [""])[0],
                        "shcp": query_params.get("shcp", [""])[0],
                    }

                    # Tạo URL mới theo định dạng cũ
                    new_video_url = f"https://api16-normal-useast5.tiktokv.us/aweme/v1/play/?{urlencode(new_params)}"
                    
                    await message.answer(title)
                    await message.answer(f"URL: {new_video_url}")
                else:
                    await message.answer("[+] Error: Could not find video URL.")
        except Exception as e:
            await message.answer(f"[+] Error: {str(e)}")
    # else:
    #     await message.answer("[+] invalid url")

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
