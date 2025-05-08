FROM python:3.13-slim
WORKDIR /app
# Install uv and dependencies
RUN pip install --no-cache-dir uv
# Copy and install dependencies with uv
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt && \
    python -c "import nltk; nltk.download('punkt', download_dir='/root/nltk_data')"
ENV NLTK_DATA=/root/nltk_data
# Copy project files
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]