FROM rackspacedot/python37

RUN mkdir /app

COPY . /app/

WORKDIR /app/

RUN pip install -r /app/requirements.txt && \
    bash -x /app/init.sh && \
    flask db init

CMD ["flask", "run"]