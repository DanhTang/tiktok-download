# Sử dụng hình ảnh Python chính thức
FROM python:3.11-slim

# Cài đặt các phụ thuộc hệ thống
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép tệp yêu cầu và mã nguồn vào hình ảnh
COPY requirements.txt requirements.txt
COPY bot.py bot.py

# Cài đặt các phụ thuộc Python
RUN pip install --no-cache-dir -r requirements.txt

# Chạy ứng dụng khi hình ảnh được khởi chạy
CMD ["python", "downloadvideo.py"]
