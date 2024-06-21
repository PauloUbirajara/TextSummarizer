FROM python:3.9
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"
COPY . .

CMD ["fastapi", "run"]
