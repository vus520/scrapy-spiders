
###文档

http://doc.scrapy.org/en/latest/intro/tutorial.html

###部署文档

```shell

yum install -y gcc
yum install -y libxslt-devel libxml2-devel sqlite-devel

yum groupinstall -y "Development tools"
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

yum remove python-pip -y

# 安装最新版本的pip
easy_install pip
/usr/local/bin/pip install scrapy pysqlite

```

### 运行任务

```shell

scrapy crawl googleplay -o items.json -t json

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
sed -i '1s/^.*$/#!\/usr\/bin\/python2x/' /usr/bin/yum
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
sed -i '1s/^.*$/#!\/usr\/bin\/python2x/' /usr/bin/yum
mv /usr/bin/python /usr/bin/python2x
ln -s /usr/local/bin/python3.3 /usr/bin/python

curl https://bootstrap.pypa.io/ez_setup.py | python
```