---
title : SQLAlchemy的使用
---

## 基本概念

|概念|对应的概念|说明|
|---|---|---|
|Engine|数据库连接|数据库驱动引擎|
|Session|连接实例|与Engine对应，隶属关系|
|Model|数据库中的数据模型|以ORM技术，将表映射为对象|
|Column|对应表中的列|是对应对象中的属性|


## 使用步骤

* 初始化数据库连接,创建engine

SQLALchemy本身无法操作数据库，其必须依赖pymysql等第三方库。在连接的字符串中标明对应的第三方库，如下所示使用的pymysql。

~~~python
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:iamneo@127.0.0.1:3306/test")  #简单形式

engine = create_engine("mysql+pymysql://root:iamneo@127.0.0.1:3306/test",  # 包含其他的可选参数
            echo=True,													   # 将orm语句转化为sql语句打印，一般debug的时候可用
            pool_size=8,												   # 连接池的大小，默认为5个，设置为0时表示连接无限制
            pool_recycle=60*30											   # 设置时间以限制数据库多久没连接自动断开
            )
~~~

创建了Engine，Engine内部维护了一个Pool(连接池)和Dialect识别具体连接数据库种类。
创建好了Engine的同时，Pool和Dialect也已经创建好了，但是此时并没有真正与数据库连接，等到执行具体的语句.connect()等时才会连接到数据库。

* 在engine基础上 创建连接会话

通过sessionmaker调用创建一个工厂，并关联Engine以确保每个session都可以使用该Engine连接资源。所有对象的载入和保存都需要通过session对象。

~~~python
from sqlalchemy.orm import sessionmaker
 
DbSession = sessionmaker(bind=engine)   # 创建session
session = DbSession()
~~~

 session的常见操作方法包括：
	flush-预提交，提交到数据库文件，还未写入数据库文件中
	commit-提交了一个事务
	rollback-回滚
	close-关闭
	
* 创建数据库模型

~~~python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()	# declarative_base()是sqlalchemy内部封装的一个方法，通过其构造一个基类，这个基类和它的子类，将Python类和表关联映射起来

class Users(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	name = Column(String(64), unique=True)
	email = Column(String(64))
	
	def __init__(self, name, email):
		self.name = name
		self.email = email
~~~

declarative_base()是sqlalchemy内部封装的一个方法，通过其构造一个基类，这个基类和它的子类，将Python类和表关联映射起来
数据库表模型类通过__tablename__和表关联起来，Column表示数据表的列。


* 生成数据库表

~~~python
Base.metadata.create_all(engine)
~~~

创建表，如果存在则忽略，执行以上代码，就会发现在db中创建了users表。

接下来，以常见的增删改查方式进行演示的说明：

* 数据库-增操作

session.add()将会把Model加入当前session维护的持久空间(可以从session.dirty看到)中，直到commit时提交到数据库。
批量插入共有以下几种方法，对它们的批量做了比较，分别是：
session.add_all() < bulk_save_object() < bulk_insert_mappings() < SQLAlchemy_core()

~~~python
add_user = Users("test", "test@test.com")
session.add(add_user)   
session.commit()    
~~~

* 数据库-查操作

通过session.query()我们查询返回了一个Query对象，此时还没有去具体的数据库中查询，只有当执行具体的 .all()，.first()等函数时才会真的去操作数据库

query有filter和filter_by两个过滤方法

~~~python
users = session.query(Users).filter_by(id=1).all()
for item in users:
  print(item.name)
  
users = session.query(Users).filter_by(Users.id == 1).all()
~~~

* 数据库-改操作

更新数据有两种方法，一种是使用query中的update方法；另一种是操作对应的表模型：

~~~python
session.query(Users).filter_by(id=1).update({'name': "test1"})     # update方法

users = session.query(Users).filter_by(name="test").first()   	  # 操作对应的表模型
users.name = "test1"
session.add(users)
~~~

* 数据库-删操作

删除数据也有两种方法，第一种使用delete函数；第二种操作对应的表模型

~~~python
session.query(Users).filter(Users.name=="test").delete()
session.commit()

delete_users = session.query(Users).filter(Users.name == "test").first()
if delete_users:
	session.delete(delete_users)
	session.commit()
~~~

## 关于Flask-SQLAlchemy

Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks。

~~~python
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True)
	
CREATE TABLE person (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id)
);

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)
		
CREATE TABLE address (
	id INTEGER NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(person_id) REFERENCES person (id)
);
~~~

If you would want to have a one-to-one relationship you can pass uselist=False to relationship()
nullable=False tells SQLAlchemy to create the column as NOT NULL.

backref is a simple way to also declare a new property on the Address class. You can then also use my_address.person to get to the person at that address. lazy defines when SQLAlchemy will load the data from the database.











