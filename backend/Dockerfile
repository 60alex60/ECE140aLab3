FROM  python:3.9
ENV PYTHONUNBUFFERED 1

COPY ./src/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

EXPOSE 5001
CMD python backend.py