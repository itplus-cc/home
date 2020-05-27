# Home导航

基于webstack模版扩展的网址导航



###  安装运行环境

```
python3 -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt
```

###  创建配置文件

```
\cp  config/local_demo.py  config/development.py
cat >> .env  <<ENV
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_RUN_PORT=8001
ENV
```

### 初始化数据表

```
flask db init
```

###  开发环境运行

```
flask run 
```

###  生产环境运行

```
\cp  config/local_demo.py  config/production.py
\cp  wsgi.ini-default  wsgi.ini
uwsgi --ini wsgi.ini #启动
uwsgi --reload  /tmp/xx.pid #重启
```

###  生产nginx配置

```
server
{
         listen      443 ssl;
         server_name home.itplus.cc;
         charset     utf-8;

         access_log /data/logs/nginx/home_access.log main;

         client_max_body_size 75m;   # adjust to taste

         location /static {

                 alias /data/code/home/static;
         }
         location / {
                 uwsgi_pass 127.0.0.1:3402;
                 include    uwsgi_params;

         }
 }
```


## 访问

```
https://home.itplus.cc/ #web
https://home.itplus.cc/admin #管理
```

