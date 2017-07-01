
# 大藏经

欢迎加入龙泉大藏经平台开发.

QQ: 279197764

Demo:
 
 [后台管理入口](http://dev.lqtripitaka.longquan.org/xadmin/)  
 [REST API 接口列表](http://dev.lqtripitaka.longquan.org/api/)


[生产环境部署文档](https://github.com/kangqiao/lqtripitaka/Deployment.md)


## 开发环境部署

### 环境
- Python 3.6.1
- Django 1.11.2
- xadmin 0.6.1

[Dependent packages](https://github.com/kangqiao/lqtripitaka/requirements.txt)

### Install
通过virtualenv安装依赖包
```
~ git clone git@github.com:kangqiao/lqtripitaka.git
~ cd lqtripitaka
~ mkvirtualenv --no-site-packages --python=python3.5 lqtripitaka
~ pip install -r requirements.txt
```
##### Xadmin Install
由于pip中xadmin与python3存在兼容问题.
使用pip从[github xadmin](https://github.com/sshwsfc/xadmin)安装最新版本.
```
~ pip uninstall xadmin
~ pip install git+https://github.com/sshwsfc/xadmin.git
```
##### Fix mysql bug
PyMySQL需要在项目设置包中settings.py 中增加:
```
import pymysql
pymysql.install_as_MySQLdb()
```

### Create admin
```
~ cd lqtripitaka
~ python manage.py createsuperuser
username: admin
e-mail: admin@126.com
password: admin 
```

### Initialization
```
~ cd lqtripitaka
~ workon lqtripitaka #激活已创建的lqtripitaka环境
~ export DJANGO_SETTINGS_MODULE=setting.settingsdev 
~ python manage.py makemigrations
~ python manage.py migrate
# 加载初始数据
~ python manage.py loaddata data.json
# Collect media:
~ python manage.py collectstatic
~ python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and [http://127.0.0.1:8000/api](http://127.0.0.1:8000/api) in your browser, the admin user password is admin

![xadmin 首页](https://github.com/kangqiao/lqtripitaka/blob/master/conf/lqtripitaka_xmain.png)

![API 首页](https://github.com/kangqiao/lqtripitaka/blob/master/conf/lqtripitaka_api.png)

```
////////////////////////////////////////////////////////////////////
//                          _ooOoo_                               //
//                         o8888888o                              //
//                         88" . "88                              //
//                         (| ^_^ |)                              //
//                         O\  =  /O                              //
//                      ____/`---'\____                           //
//                    .'  \\|     |//  `.                         //
//                   /  \\|||  :  |||//  \                        //
//                  /  _||||| -:- |||||-  \                       //
//                  |   | \\\  -  /// |   |                       //
//                  | \_|  ''\---/''  |   |                       //
//                  \  .-\__  `-`  ___/-. /                       //
//                ___`. .'  /--.--\  `. . ___                     //
//              ."" '<  `.___\_<|>_/___.'  >'"".                  //
//            | | :  `- \`.;`\ _ /`;.`/ - ` : | |                 //
//            \  \ `-.   \_ __\ /__ _/   .-` /  /                 //
//      ========`-.____`-.___\_____/___.-`____.-'========         //
//                           `=---='                              //
//      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        //
//                         南无阿弥陀佛                            //
////////////////////////////////////////////////////////////////////

```