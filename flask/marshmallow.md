---
title : marshmallow的使用
---

## marshmallow的

marshmallow（Object serialization and deserialization, lightweight and fluffy）用于对象进行序列化和反序列化，并同步进行数据验证。

对对象进行序列化和反序列化需要一个中间载体，schema就是这个中间载体。

1 序列化：将对象转化为字节序列的过程
2 反序列化：将字节序列转化为对象的过程

所以marshmallow是序列化和反序列化间进行构建元数据关系，并提供对应的转化的方法。

## 构建用户测试的对象模型和schema

是一个转化的过程，所以明确这些

* 先构建一个对象模型

~~~python
import datetime as dt
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()
    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)
~~~

* 构建对象模型的Schema

~~~python
from marshmallow import Schema, fields

class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()
~~~

## 序列化演示

* 序列化操作-使用dump函数，返回字典

~~~python
from pprint import pprint

user = User(name="neo", email="neo@neo.com")
schema = UserSchema()
result = schema.dump(user)
pprint(result)

----计算的结果
{'created_at': '2020-09-03T15:32:44.591877',
 'email': 'neo@neo.com',
 'name': 'neo'
}

~~~

* 序列化操作-使用dumps函数，返回字符串

~~~python
user = User(name="neo", email="neo@neo.com")
schema = UserSchema()
result = schema.dumps(user)
pprint(result)

---计算的结果
('{"name": "neo", "email": "neo@neo.com", "created_at": '
 '"2020-09-03T15:35:12.663656"}')
~~~

* 序列化操作-输出特定字段，使用only或者exclude参数，设置many=True可以一次处理一个集合的对象

~~~python
user = User(name="neo", email="neo@neo.com")
schema = UserSchema(only=('name', ))
result = schema.dump(user)
pprint(result)

---计算的结果
{'name': 'neo'}
~~~

* 反序列化操作-使用load函数
  默认情况下，反序列化的load方法会返回一个字典
  
~~~python
user_data = {
    'created_at': '2014-08-11T05:26:03.869245',
    'name': 'neo',
    'email': 'neo@neo.com'
}

schema = UserSchema()
result = schema.load(user_data)
pprint(result)

---
{'created_at': datetime.datetime(2014, 8, 11, 5, 26, 3, 869245),
 'email': 'neo@neo.com',
 'name': 'neo'}
~~~

* 反序列化操作-为了能返回对象，在schema的一个方法加上post_load装饰器

~~~python
from marshmallow import Schema, fields, post_load

class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
		
user_data = {
    'name': 'neo',
    'email': 'neo@neo.com'
}

schema = UserSchema()
result = schema.load(user_data)
~~~

* 验证处理-Validation

load方法可以对字段进行验证，并引发ValidationError异常，可以调用ValidationError.valid_data查看通过验证的字段，
schema内置有常见类型的字段检查，例如：Email，URL等



