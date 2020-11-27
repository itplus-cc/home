FROM rackspacedot/python37

RUN mkdir /app

COPY . /app/

RUN pip install -r /app/requirements.txt && \
    cp  /app/config/local_demo.py  /app/config/development.py && \
    cat >> .env  <<ENV \
        FLASK_ENV=development \
        FLASK_DEBUG=1 \
        FLASK_RUN_PORT=8001 \
        ENV && \
    flask db init

WORKDIR /app/

CMD ["flask", "run"]