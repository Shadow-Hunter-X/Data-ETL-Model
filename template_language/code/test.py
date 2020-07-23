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