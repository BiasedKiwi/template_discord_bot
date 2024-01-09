FROM python:3.12.1-bookworm

WORKDIR /bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD ["python", "launcher.py"]
