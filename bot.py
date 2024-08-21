import logging
import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Cấu hình logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token của bot Telegram
BOT_TOKEN = 'YOUR_BOT_TOKEN'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gửi tin nhắn chào mừng khi người dùng bắt đầu trò chuyện với bot."""
    await update.message.reply_text('Chào bạn! Gửi cho tôi một liên kết video TikTok để tải về.')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xử lý liên kết TikTok và tải video về."""
    if update.message.text:
        url = update.message.text
        if 'tiktok.com' in url:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        # Giả sử bạn có một hàm để xử lý video từ URL
                        video_data = await response.read()
                        
                        # Gửi video về cho người dùng
                        await update.message.reply_video(video_data)
            except Exception as e:
                logger.error(f"Error downloading video: {e}")
                await update.message.reply_text("Có lỗi xảy ra khi tải video.")
        else:
            await update.message.reply_text("Đây không phải là một liên kết TikTok hợp lệ.")
    else:
        await update.message.reply_text("Vui lòng gửi liên kết video TikTok.")

async def main() -> None:
    """Khởi tạo và chạy bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Đăng ký các handler
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Chạy bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
