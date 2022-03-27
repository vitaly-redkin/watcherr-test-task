FROM python:3.10-alpine
RUN mkdir /app
ADD . /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8888
CMD ["python", "main.py"]
