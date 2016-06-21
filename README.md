#### Django REST framework tutorial
知道有这个东西，干看文档没看出个一二三来，然后按照官方示例试了试，发现挺好理解的～

#### Django和Django REST framework的区别
1. 前者是基于Python的一个web框架，后者是基于Django实现的一个RESTful框架（名字上就很直观），至于什么是RESTful架构请看[链接](http://www.ruanyifeng.com/blog/2011/09/restful)，关于RESTful API的设计请看[链接](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)
2. 这个框架的优势相对于Django在哪里呢？看官方定义：Django REST framework is a powerful and flexible toolkit for building Web APIs. 是一套构建web API的灵活的工具.也就是说构建API的时候非常方便，具体怎么方便看下面～

PS：其实我开始也很好奇是什么意思，之前一直在用Django，也知道REST，然后写的接口也是在按照这个原则来写的，为什么又多了个DRF呢？我也十分不理解，然后就有了这个项目（其实只是按照官方文档做了一下就大概了解了）

#### 快速入门(摘自[官方文档](http://www.django-rest-framework.org/))

##### requirements
REST framework requires the following:

1. Python (2.7, 3.2, 3.3, 3.4, 3.5)
2. Django (1.7+, 1.8, 1.9)

The following packages are optional:

1. Markdown (2.1.0+) - Markdown support for the browsable API.
2. django-filter (0.9.2+) - Filtering support.
3. django-crispy-forms - Improved HTML display for filtering.
4. django-guardian (1.1.1+) - Object level permissions support.

目前只是实验性质，所以只安装必要的那2个就可以了，详细见requirements.txt

##### install
1. Install using pip, including any optional packages you want...

```
pip install djangorestframework
pip install markdown      
pip install django-filter  
```

2. Add rest_framework to your INSTALLED_APPS setting（默认创建了Django项目，没有创建使用django-admin startproject xxx命令来创建，同时python manage.py migrate数据库，创建superuser等）.

```
INSTALLED_APPS = (
    'rest_framework',
)
```

3. If you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views. Add the following to your root urls.py file.
```
    urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))]
```

##### example
准备工作前边已经做完了，下面开始正式的例子，利用DR创建一个关于自带的User Model的API，实现的功能是创建user和获取user列表。

1. DRF全局配置放在一个名为REST_FRAMEWORK的字典中，字典放在settings.py下面，如下：

```
    REST_FRAMEWORK = {
    
    'DEFAULT_PERMISSION_CLASSES': [
    
        'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
        
        'PAGE_SIZE': 10
    ]
}
```

2. 使用django-admin startapp xxx命令创建一个Django app，本文使用quickstart名称。
3. define some serializers（不知道怎么翻译这个词比较好）.创建```quickstart/serializers.py```文件，内容如下：

```
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
```
        
4. 修改views.py

```
    from django.contrib.auth.models import User, Group
    from rest_framework import viewsets
    from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
```

5. 修改urls
    
```
    from django.conf.urls import url, include
    
    from rest_framework import routers
    
    from tutorial.quickstart import views
    
    router = routers.DefaultRouter()
    
    router.register(r'users', views.UserViewSet)
    
    router.register(r'groups', views.GroupViewSet)

    urlpatterns = [
        url(r'^', include(router.urls)),
        
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]
```

6. test
使用```python manage.py runserver```运行项目，浏览器打开```127.0.0.1```
然后就可以看见登录页面了，如下：
![login](http://o7fm0rolr.bkt.clouddn.com/Screenshot%20-%202016%E5%B9%B406%E6%9C%8821%E6%97%A5%20-%2021%E6%97%B631%E5%88%8640%E7%A7%92.png)
点击右上角登录，输入superuser的帐号密码就可以了。
![home_page](http://o7fm0rolr.bkt.clouddn.com/Screenshot%20-%202016%E5%B9%B406%E6%9C%8821%E6%97%A5%20-%2021%E6%97%B631%E5%88%8656%E7%A7%92.png)
用户列表
![user list](http://o7fm0rolr.bkt.clouddn.com/Screenshot%20-%202016%E5%B9%B406%E6%9C%8821%E6%97%A5%20-%2021%E6%97%B632%E5%88%8635%E7%A7%92.png)
可以从下面post添加账户
![add user](http://o7fm0rolr.bkt.clouddn.com/add.png)
用户详细信息
![user detail](http://o7fm0rolr.bkt.clouddn.com/Screenshot%20-%202016%E5%B9%B406%E6%9C%8821%E6%97%A5%20-%2021%E6%97%B633%E5%88%8624%E7%A7%92.png)
删除
![delete user](http://o7fm0rolr.bkt.clouddn.com/after%20delete.png)
