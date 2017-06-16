
# 大藏经

欢迎加入龙泉大藏经平台开发.
QQ: 279197764

### Install Requires
```
Django==1.11.2
django-crispy-forms==1.6.1
django-formtools==2.0
django-reversion==2.0.8
djangorestframework==3.6.3
future==0.16.0
httplib2==0.9.2
pytz==2017.2
six==1.10.0
xadmin==0.6.1
```

### Install
通过virtualenv安装依赖包
```
~ git clone git@github.com:kangqiao/lqtripitaka.git
~ cd lqtripitaka
~ mkvirtualenv --no-site-packages --python=python3.5 lqtripitaka
~ pip install -r requirements.txt
```
#### Fix xadmin bug
由于pip中xadmin与python3存在兼容问题. 需要使用[github xadmin](https://github.com/sshwsfc/xadmin)中最新版本.
```
~ cd ..
~ git clone git@github.com:sshwsfc/xadmin.git
# 删除已安装的xadmin
~ rm -rf ~/.virtualenvs/lqtripitaka/lib/python3.5/site-packages/xadmin
# 复制git仓中xadmin到virtualenvs环境中.
~ cp -R xadmin/xadmin ~/.virtualenvs/lqtripitaka/lib/python3.5/site-packages
```

### Create admin
```
~ cd lqtripitaka
~ python manage.py createsuperuser
username: admin
e-mail: admin@126.com
password: `1q2w3e4r
```

### Initialization
```
~ cd lqtripitaka
~ workon lqtripitaka #激活已创建的lqtripitaka环境
~ python manage.py makemigrate
~ python manage.py migrate
# 加载初始数据
~ python manage.py loaddata data.json
# [Option]Collect media:
~ python manage.py collectstatic
~ python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser, the admin user password is admin


