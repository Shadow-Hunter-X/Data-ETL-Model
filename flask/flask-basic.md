---
title : flask-basic
---

### 应用

* 描述：导入flask中的Flask模块，并实例化Flask对象，构建WSGI应用程序。
  
~~~python
app = Flask(__name__)   # 构建Flask对象
...
app.run                 # 执行
~~~

### 路由

* 描述： 将URL绑定到对应的函数

* 相关函数 ：

|函数|功能|
|----|-----|
|@app.route('...')|将URL和函数绑定|
|add_url_rule()|同样将URL绑定函数的功能|
|url_for()|动态构建特定函数的URL非常有用|

* 对于路由中参数的传递：

    变量部分标记为<variable-name>，如@app.route('/hello/<name>')

* 定义路由的规则，保持URL是唯一，URL结尾处添加"/"


### HTTP方法

HTTP请求对象： from flask import request 

默认情况下Flask路由响应Get请求，可以通过route装饰器提供的方法改变此选项，方法如下：

@app.route('/login',methods = ['POST', 'GET'])

表示这个路由接受Post和Get请求，如果使用了没有指定的HTTP请求方法，则会出现Method Not Allowed的错误。

针对从客户端发送的HTTP请求中，通过 request.method 判断具体的请求方式。

* post ： request.form['']       获取表单数据
* get  ： request.args.get('')   获取URL中的参数

对于request对象包含以下的重要的属性：

|属性|说明|
|-----|-----|
|form|它是一个字典对象，包含表单参数及其值的键和值对|
|args|解析查询字符串的内容，它是问号（？）之后的URL的一部分|
|cookies|保存Cookie名称和值的字典对象|
|files|与上传文件有关的数据|
|method|当前请求方法|

### 模板--Jinja2

相关内容，参考前面文章的说明。

Flask将尝试在templates文件夹中找到HTML文件进行处理。

### 静态文件

Web应用程序通常需要静态文件，例如javascript文件或支持网页显示的CSS文件。通常，配置Web服务器并为您提供这些服务，但在开发过程中，这些文件是从static文件夹中获取。

使用Jinja2中的url_for函数进行加载JavaScript文件，具体的操作如下：

~~~js
<script type = "text/javascript" 
    src = "{{ url_for('static', filename = 'jquery.js') }}" >
</script>
~~~

### Cookie

Cookie以文本文件的形式存储在客户端的计算机上。其目的是记住和跟踪与客户使用相关的数据，以获得更好的访问者体验和网站统计信息。

Cookie处理：

* 设置Cookie 

flask中想向前端返回数据，使用Response对象。对应的函数是make_response。
  
~~~python
resp = make_response("success")   # 设置响应体:字符串或html页面
resp.set_cookie("key", "value")
~~~

* 获取Cookie

~~~python
cookie = request.cookies.get("key")
~~~

* 删除cookie ，只是让cookie过期

~~~python
resp = make_response("del success")  # 设置响应体
resp.delete_cookie("key")
~~~

### Session

session 在服务器端，cookie 在客户端（浏览器）
session 默认被存在在服务器的一个文件里（不是内存）
session 的运行依赖session id，而session id 是存储在cookie 中的。如果浏览器禁用了cookie ，同时 session 也会失效（但不绝对）
session 可以放在 文件、数据库、或内存中都可以。
用户验证这种场合一般会用 session 因此，维持一个会话的核心就是客户端的唯一标识，即 session id

flask框架session存储有两种方式:
第一种方式：直接存在客户端的cookies中
第二种方式：存储在服务端，如：redis,memcached,mysql，file,mongodb等等，存在flask-session第三方库

操作步骤：
SECRET_KEY 配置变量是通用密钥, 可在 Flask 和多个第三方扩展中使用。如其名所示, 加密的强度取决于变量值的机密度。 
不同的程序要使用不同的密钥, 而且要保证其他人不知道你所用的字符串。其主要作用应该是在各种加密过程中加盐以增加安全性。
在实际应用中最好将这个参数存储为系统环境变量

~~~python
from flask import Flask,session
import os
from datetime import timedelta
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
# 添加数据到session中
# 操作session的时候 跟操作字典是一样的。
# SECRET_KEY

@app.route('/')
def hello_world():
    session['username'] = 'zhangsan'
    # 如果没有指定session的过期时间，那么默认是浏览器关闭就自动结束
    # 如果设置了session的permanent属性为True，那么过期时间是31天。
    session.permanent = True
    return 'Hello World!'

@app.route('/get/')
def get():
    # session['username']   如果username不存在则会抛出异常
    # session.get('username')   如果username不存在会得到 none 不会报错 推荐使用
    return session.get('username')

@app.route('/delete/')
def delete():
    print(session.get('username'))
    session.pop('username')
    print(session.get('username'))
    return 'success'

@app.route('/clear/')
def clear():
    print(session.get('username'))
    # 删除session中的所有数据
    session.clear()
    print(session.get('username'))
    return 'success'

if __name__ == '__main__':
    app.run(debug=True)

~~~

### 重定向和消息闪现

* Flask类有一个redirect()函数。调用时，它返回一个响应对象，并将用户重定向到具有指定状态代码的另一个目标位置

~~~python
Flask.redirect(location, statuscode, response)
~~~

* Flask模块包含flash()方法,提示给用户的消息:flash(message, category)

~~~python
@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('watchlist'))
~~~

message参数是要闪现的实际消息;category参数是可选的。它可以是error，info或warning

当get_flashed_message()函数被调用时，session中存储的所有消息都会被移除。

~~~html
<main>
    {% for message in get_flashed_messages() %}
        <div class="alert">{{ message }}</div>
    {% endfor %}
    {% block content %}{% endblock %}
</main>
~~~

### flask文件上传

在Flask中处理文件上传非常简单。它需要一个HTML表单，其enctype属性设置为“multipart / form-data”，将文件发布到URL。
URL处理程序从request.files[]对象中提取文件，并将其保存到所需的位置。

~~~html
<html>
   <body>
   
      <form action = "http://localhost:5000/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>
~~~

~~~python
from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(debug = True)
~~~
