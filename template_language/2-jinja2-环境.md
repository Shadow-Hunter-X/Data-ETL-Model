---
title : jinja2-环境
---

Jinja2 uses a central object called the template Environment. Instances of this class are used to store the configuration and global objects, and are used to load templates from the file system or other locations. Even if you are creating templates from strings by using the constructor of Template class, an environment is created automatically for you, albeit a shared one.

Most applications will create one Environment object on application initialization and use that to load templates. In some cases however, it’s useful to have multiple environments side by side, if different configurations are in use.

Jinja2中的一个主要概念是模板环境。初始化的模板环境用于存储配置的信息和全局对象，且被用来从文件系统或其他地址中加载模板。即便是
以字符串作为参数创建模板类，这样还是隐式的创建一个环境对象。

绝大多数的Jinja2应用，在一个初始化是创建一个环境用于加载模板。但在某些情况下，使用多个环境对象能带来极大的便利性。

### 构建模板对象的方法

最简单构建模板对象的方法如下所示：

~~~python
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('yourapplication', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
~~~

Environment支持两种加载方式：**PackageLoader：包加载器** 和 **FileSystemLoader：文件系统加载器**

* 包加载方式

~~~python
from jinja2 import PackageLoader,Environment

#PackageLoader()的两个参数为：python包的名称，以及模板目录名称。
env = Environment(loader=PackageLoader('python_project','templates'))    # 创建一个包加载器对象
 
#get_template()：获取模板目录下的某个具体文件。
template = env.get_template('bast.html')  

#render()：接受变量，对模板进行渲染
template.render()  
~~~

* 文件系统加载方式

文件系统加载器，不需要模板文件存在某个Python包下，可以直接访问系统中的文件

### 演示模板继承

~~~python

# coding:utf-8

with open(u'大地.txt', encoding='utf-8', mode='w') as file:
    file.write(u"""
{% block template %}大地.txt{% endblock template %}
大地：一切开始的地方......
{#- "开始" Base中的内容 #}
{% block begin %}
    大地承载着万物
{%- endblock begin %}
无望无际""".strip())

with open(u'树.txt', encoding='utf-8', mode='w' ) as file:
    file.write(u"""
{% extends "大地.txt" %}
{# 重写template块，从大地.txt继承来的 #}
{% block template %}树.txt{% endblock template %}
{#- 重写begin块 #}
{% block begin %}
	树在大地上生长
{%- endblock begin %}""".strip())

with open(u'四季.txt',encoding='utf-8', mode='w') as file:
    file.write(u"""
{% extends "树.txt" %}
{# 重写template块，从树.txt继承来的 #}
{% block template %}四季.txt{% endblock template %}
{% block begin %}
	走过四季
{%- endblock begin %}""".strip())

from jinja2 import Environment, FileSystemLoader
env = Environment()

# tell the environment how to load templates
env.loader = FileSystemLoader('.')

# look up our template
tmpl = env.get_template('大地.txt')

# render it to default output
print ( tmpl.render() )

# loads child.html and its parent
tmpl = env.get_template('树.txt')
print ( tmpl.render() )

# loads other.html and its parent
print ( env.get_template('四季.txt').render() )

~~~

