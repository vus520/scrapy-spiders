
###文档

http://doc.scrapy.org/en/latest/intro/tutorial.html

###部署文档

step 1, 确认python版本 >= 2.7，文末有文档
step 2, 安装pip
step 3, 安装scrapy

```shell

yum install -y gcc
yum install -y libxslt-devel libxml2-devel sqlite-devel python-devel

yum groupinstall -y "Development tools"
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel ibffi-devel

yum remove python-pip -y

# 安装最新版本的pip
yum install -y easy_install
#wget https://bootstrap.pypa.io/ez_setup.py -O - | python

easy_install pip
#/usr/local/bin/easy_install pip

/usr/local/bin/pip install scrapy scrapy-redis pysqlite --upgrade

```

### 运行任务

```shell

#保存为文件
scrapy crawl googleplay -o items.json -t json

```

### 通过Redis分布式抓取

```shell

#先添加一个redis项目的入口
redis-cli lpush redis:start_urls 'https://play.google.com/store/apps/category/FAMILY_BR
scrapy crawl googleplay 

```


### supervisor 守护

```
pip install supervisor
echo_supervisord_conf > /etc/supervisord.conf
cat supervisor.conf >> /etc/supervisord.conf

supervisord -c /etc/supervisord.conf
supervisorctl start gp
```

### 附1 Python 2.7的安装方法

> http://toomuchdata.com/2014/02/16/how-to-install-python-on-centos/


```

# Python 2.7.6:
wget http://python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
tar xf Python-2.7.6.tar.xz
cd Python-2.7.6
./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make && make altinstall

# 解决python 只支持2.6及以下版本的问题
sed -i '1s/^.*$/#!\/usr\/bin\/python2.6/' /usr/bin/yum
mv /usr/bin/python /usr/bin/python2x
ln -s /usr/local/bin/python2.7 /usr/bin/python

curl https://bootstrap.pypa.io/ez_setup.py | python

```

### 附2 Python 3的安装方法

```

# Python 3.3.5:
wget http://python.org/ftp/python/3.3.5/Python-3.3.5.tar.xz
tar xf Python-3.3.5.tar.xz
cd Python-3.3.5
./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make && make altinstall

# 解决python 只支持2.6及以下版本的问题
sed -i '1s/^.*$/#!\/usr\/bin\/python2.6/' /usr/bin/yum
mv /usr/bin/python /usr/bin/python2x
ln -s /usr/local/bin/python3.3 /usr/bin/python

curl https://bootstrap.pypa.io/ez_setup.py | python
```