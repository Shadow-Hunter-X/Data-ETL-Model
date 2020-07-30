---
title : flask extension
---

Flask通常被称为微框架,只有Web开发中的基础的功能。对于开发完备的Web应用还是不足的，但Flask扩展就具备这样的功能。
Flask扩展是一个Python模块，它向Flask应用程序添加了特定类型的支持。Flask Extension Registry（Flask扩展注册表）是一个可用的扩展目录。
可以通过pip实用程序下载所需的扩展名。

### flask email

基于web的应用程序通常需要具有向用户/客户端发送邮件的功能。安装Flask-Mail扩展:pip install Flask-Mail。

在代码中从flask-mail模块导入Mail和Message类
~~~python
from flask_mail import Mail, Message
~~~

配置Flask-Mail
~~~python
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
~~~

使用配置好的数据，构建Mail类。
~~~python
mail = Mail(app)
~~~

通过URL规则，构建发送
~~~python
@app.route("....")
def send_mail():
   msg = Message('Hello', sender = 'your@gmail.com', recipients = ['xxxx@gmail.com'])
   msg.body = "This is the email body"
   mail.send(msg)
   return "Sent"
~~~

### flask wtf

HTML提供了一个<form>标签，用于设计界面。可以适当地使用Form（表单）元素:文本输入、单选按钮、选择等。

用户输入的数据以Http请求消息的形式通过GET或POST方法提交给服务器端脚本。
* 服务器端脚本必须从http请求数据重新创建表单元素。实际上表单元素必须定义两次 - 一次在HTML中，另一次在服务器端脚本中。
* 使用HTML表单的另一个缺点是很难（如果不是不可能的话）动态呈现表单元素。HTML本身无法验证用户的输入

这就是WTForms的作用，一个灵活的表单、渲染和验证库。能够方便使用,Flask-WTF扩展为这个WTForms库提供了一个简单的接口。
安装wtf：pip install flask-WTF

WTforms包中包含各种表单字段的定义,如下表所示：

|关键字|描述|
|-----|-----|
|TextField|表示\<input type ='text'\> HTML表单元素|
|BooleanField|表示\<input type ='checkbox'\> HTML表单元素|
|DecimalField|用于显示带小数的数字的文本字段|   
|IntegerField|用于显示整数的文本字段|
|RadioField|表示\<input type = 'radio'\> HTML表单元素|
|SelectField|表示选择表单元素|
|TextAreaField|表示\<testarea\>HTML表单元素|
|PasswordField|表示\<input type = 'password'\> HTML表单元素|
|SubmitField|表示\<input type = 'submit'\>表单元素|



