FROM rackspacedot/python37

RUN mkdir /app

COPY . /app/

RUN pip install -r /app/requirements.txt && \
    bash -x /app/init.sh && \
    flask db init

WORKDIR /app/

CMD ["flask", "run"]