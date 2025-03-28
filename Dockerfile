FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["venv/bin/python", "src/main.py"]