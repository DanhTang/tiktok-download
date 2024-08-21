import os
import uuid
import asyncio
import re
import httpx
import yt_dlp as youtube_dl
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hàm kiểm tra link TikTok
def is_tiktok_link(url: str) -> bool:
    tiktok_regex = r'https?://(www\.)?tiktok\.com/.*'
    return re.match(tiktok_regex, url) is not None

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào mừng! Hãy gửi cho tôi liên kết TikTok để tải video.")

# Hàm xử lý khi người dùng gửi link TikTok
async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id

    if not is_tiktok_link(url):
        await update.message.reply_text("Hãy nhập link TikTok vào đây.")
        return

    unique_id = str(uuid.uuid4())  # Tạo ID duy nhất
    file_path = f'downloaded_video_{unique_id}.mp4'

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': file_path,
        'noplaylist': True,  # Chỉ tải video đơn
    }

    try:
        logger.info("Đang tải video từ TikTok...")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
        logger.info("Video đã tải xuống thành công.")

        # Kiểm tra kích thước video
        file_size = os.path.getsize(file_path)
        max_size = 50 * 1024 * 1024  # 50MB

        if file_size > max_size:
            await update.message.reply_text("Video quá lớn để gửi qua Telegram.")
            os.remove(file_path)
            return

        # Gửi video qua Telegram
        if os.path.exists(file_path):
            logger.info("Đang gửi video qua Telegram...")
            async with httpx.AsyncClient(timeout=120) as client:
                context.bot.request._client = client  # Sử dụng httpx client tùy chỉnh
                with open(file_path, 'rb') as video_file:
                    await context.bot.send_video(chat_id=chat_id, video=video_file)
                logger.info("Video đã được gửi thành công.")
        else:
            logger.error("Tệp video không tồn tại.")
            await update.message.reply_text("Đã xảy ra lỗi: Tệp video không tồn tại.")

        # Xóa tệp sau khi gửi xong
        os.remove(file_path)

    except Exception as e:
        logger.error("Đã xảy ra lỗi khi gửi video:", exc_info=True)
        await update.message.reply_text(f"Đã xảy ra lỗi: {e}")

# Hàm chính để khởi chạy bot
async def main():
    TOKEN = os.getenv('TOKEN')  # Lấy token từ biến môi trường

    # Cấu hình ứng dụng Telegram
    application = ApplicationBuilder().token(TOKEN).build()

    # Thêm handler cho lệnh /start
    application.add_handler(CommandHandler("start", start))

    # Thêm handler cho các tin nhắn văn bản khác
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))

    # Chạy polling để lắng nghe các sự kiện từ Telegram
    await application.run_polling()

# Khởi chạy chương trình
if __name__ == '__main__':
    asyncio.run(main())
