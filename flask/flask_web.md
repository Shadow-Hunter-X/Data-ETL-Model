---
title : flask-web
---

* 初始化方法

~~~python
from flask import Flask
app = Flask(__name__)
~~~

The only required argument to the Flask class constructor is the name of the main module or package of the application. For most applications, Python’s __name__ variable is the correct value

作用： this argument to determine the root path of the application so that it later can find resource files relative to the location of the application。

* 路由

通过装饰器，进行构造路由。

* 上下文
  
    当Flask收到来自客户端的请求时，它需要提供一些对象处理它的视图函数。请求对象就是一个很好的例子
封装客户端发送的HTTP请求很明显，Flask可以让视图函数访问请求对象是通过将其作为参数发送的，但这将需要
申请有一个额外的参数。

    如果你考虑一下，事情会变得更复杂请求对象不是视图函数可能需要访问的唯一对象
满足一个请求为了避免视图函数中有很多可能需要也可能不需要的参数，Flask使用上下文临时地使某些对象可以全局访问。

~~~py
from flask import requestk
~~~

There are two contexts in Flask: the application context and the request context. 

|变量名|上下文|说明|
|-----|--------|-------|
|current_app|Application context|The application instance for the active application.|
|g|Application context|An object that the application can use for temporary storage during the handling of a request. This variable is reset with each request.|
|request|Request context|The request object, which encapsulates the contents of a HTTP request sent by the client|
|session|Request context|The user session, a dictionary that the application can use to store values that are “remembered” between requests.|



