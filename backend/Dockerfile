FROM python:3.7-stretch
LABEL maintainer="vedanshi283@gmail.com"
EXPOSE 8000
RUN  mkdir -p  /ResSum-Backend
WORKDIR  /ResSum-Backend
RUN pip install --no-cache-dir -U pip
COPY requirements.txt .
ENV MAX_WORKERS="1"
ENV WEB_CONCURRENCY="1"
RUN pip install -r requirements.txt
RUN pip install psutil
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader omw-1.4
COPY  . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]