FROM python:3.7.3-stretch
LABEL maintainer="vedanshi283@gmail.com"
RUN  mkdir -p  /ResSum-Backend
WORKDIR  /ResSum-Backend
RUN pip install --no-cache-dir -U pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY  . .
CMD ["python", "main.py"]