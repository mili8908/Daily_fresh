# Daily_fresh
a Django project

<----------------------------------------------------------------------->
Redis
# 启动redis  // sudo redis-server /usr/local/redis-3.2.8/etc/redis.conf
# 查看redis pid  // ps aux | grep redis
# 停止 // sudo kill -9 pid
# redis客户端 // redis-cli
#             // redis-cli -h ip -p port
# 客户端帮助  // redis-cli --help
<----------------------------------------------------------------------->
Celery
# celery 启动 // celery -A celery_tasks.tasks worker -l info

<----------------------------------------------------------------------->
FDFS
#nginx配置 // sudo vim /usr/local/nginx/conf/nginx.conf
#配置 // sudo vim /etc/fdfs/mod_fastdfs.conf
#配置 // sudo vim /etc/fdfs/storage.conf
#配置 // sudo vim /etc/fdfs/client.conf
#storage启动 // fdfs_storaged /etc/fdfs/storage.conf
#tracker启动 // fdfs_trackerd /etc/fdfs/tracker.conf
#nginx启动 // sudo /usr/local/nginx/sbin/nginx
#nginx重启 // sudo /usr/local/nginx/sbin/nginx -s reload
#nginx关闭 // sudo /usr/local/nginx/sbin/nginx -s stop
