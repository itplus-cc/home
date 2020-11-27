#!/bin/bash
# 方便docker部署

cp  /app/config/local_demo.py  /app/config/development.py
cat >> .env  <<ENV
    FLASK_ENV=development
    FLASK_DEBUG=0
    FLASK_RUN_PORT=8001
    FLASK_RUN_HOST=0.0.0.0
ENV
