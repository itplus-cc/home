# Home导航

基于webstack模版扩展的网址导航

## 新增Docker部署

```
git clone https://github.com/Brooke9537/home.git
cd home
docker build -t home .
docker run -itd --name home --network host home
# 默认使用8001端口，host网络模式，可直接ip:port访问，需要修改请看init.sh
docker logs -f home
```


###  安装运行环境

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

###  创建配置文件

```
cp  config/local_demo.py  config/development.py
# 可选择数据库MySQL或SQLite，修改移步app.py 使用SQLite无需配置DATABASE_CONF
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

