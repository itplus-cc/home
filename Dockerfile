FROM rackspacedot/python37

RUN mkdir /app

COPY . /app/

WORKDIR /app/

#RUN pip install -r /app/requirements.txt && \
# 国内环境可自行替换为国内源
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt && \
    bash -x /app/init.sh && \
    flask db init

CMD ["flask", "run"]