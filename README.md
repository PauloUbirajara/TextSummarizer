# Text Summarizer
[demo.webm](https://github.com/PauloUbirajara/TextSummarizer/assets/49159843/7b4ec7ee-9484-461b-b2d5-73fa5481ba93)

> Summarize texts using Python

## Setup
> Application starts at [`http://localhost:8000`](http://localhost:8000)

### Using local Python
```sh
pip install -r requirements.txt
fastapi run main.py
```
### Using Docker
```sh
docker compose up
```

## Routes

### [`/`](http://localhost:8000)
> UI for choosing summarizer, language, row count and inputting the original text to be summarized

### [`/docs`](http://localhost:8000/docs) and [`/redoc`](http://localhost:8000/redoc)
> Documentation provided by FastAPI
