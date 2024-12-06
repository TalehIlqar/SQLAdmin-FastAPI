FROM python:3.10-slim

WORKDIR /code

# Lazımi alətləri quraşdırın
RUN apt-get update && apt-get install -y git gcc python3-dev libpq-dev && apt-get clean
RUN pip install --no-cache-dir itsdangerous

# Pip-in ən son versiyasını quraşdırın
RUN pip install --upgrade pip

# Asılılıqları quraşdırmaq üçün requirements.txt faylını əlavə edin
COPY requirements.txt .

# Asılılıqları quraşdırın
RUN pip install --no-cache-dir -r requirements.txt

# Static və templates qovluqlarını daxil edin
COPY ./static /code/static
COPY ./templates /code/templates

# Layihə fayllarını konteynerə əlavə edin
COPY . .
