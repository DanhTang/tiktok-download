# Sử dụng Python image chính thức
FROM python:3.11

# Cài đặt các thư viện cần thiết
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Sao chép mã nguồn vào container
COPY bot.py bot.py

# Cấu hình lệnh để chạy ứng dụng
CMD ["python", "bot.py"]
