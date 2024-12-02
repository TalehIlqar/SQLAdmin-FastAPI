FROM python:3.10-slim

WORKDIR /code

# Lazımi alətləri quraşdırın
RUN apt-get update && apt-get install -y git gcc python3-dev libpq-dev && apt-get clean

# Pip-in ən son versiyasını quraşdırın
RUN pip install --upgrade pip

# Asılılıqları quraşdırmaq üçün requirements.txt faylını əlavə edin
COPY requirements.txt .

# Asılılıqları quraşdırın
RUN pip install --no-cache-dir -r requirements.txt

# Layihə fayllarını konteynerə əlavə edin
COPY . .
