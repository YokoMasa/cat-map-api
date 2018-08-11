FROM python:3.6.5
ENV PYTHONUNBUFFERED 1
RUN mkdir app
WORKDIR app
COPY ./requirement.txt .
RUN pip install -r requirement.txt 
COPY . .

