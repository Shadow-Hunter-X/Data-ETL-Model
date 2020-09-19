---
title : Flask-SQLAlchemy
---

## Flask-SQLAlchemy

Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using 
SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

### 1-Flask应用环境

使用的场景：多应用或应用创建的时机
However if you want to use more than one application or create the application dynamically in a function you want to read on.

If you define your application in a function, but the SQLAlchemy object globally, how does the latter learn about the former? 
The answer is the **init_app()**  function

~~~python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)			# Because there might be more than one application created
    return app
~~~

how does SQLAlchemy come to know about your application.the answer is : setup an application context 。

~~~python
def my_function():
    with app.app_context():
        user = db.User(...)
        db.session.add(user)
        db.session.commit()
~~~

针对单应用程序，直接将SQLAlchemy和Flask绑定即可。

~~~python
app = Flask(__name__)
db = SQLAlchemy(app)
~~~

## 2-Configuration

A list of configuration keys currently understood by the extension.

[](res/flask-sqlalchemy-config.png)

## 3-模型定义

Things to keep in mind:

The baseclass for all your models is called db.Model. It’s stored on the SQLAlchemy instance you have to create. See Quickstart for more details.

Some parts that are required in SQLAlchemy are optional in Flask-SQLAlchemy. For instance the table name is automatically set for you unless overridden. It’s derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case”. To override the table name, set the __tablename__ class attribute.

~~~python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
~~~

### One-to-Many Relationships

relationships are declared before they are established you can use strings to refer to classes that are not created yet 

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

### Many-to-Many Relationships

If you want to use many-to-many relationships you will need to define a helper table that is used for the relationship. For this helper table it is strongly recommended to not use a model but an actual table。

~~~python
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',backref=db.backref('pages', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
~~~


Here we configured Page.tags to be loaded immediately after loading a Page, but using a separate query. This always results in two queries when retrieving a Page, but when querying for multiple pages you will not get additional queries.

## Select, Insert, Delete

### Insert

Inserting data into the database is a three step process:

* Create the Python object
* Add it to the session
* Commit the session

The session here is not the Flask session, but the Flask-SQLAlchemy one. It is essentially a beefed up version of a database transaction. This is how it works:

~~~python
>>> from yourapp import User
>>> me = User('admin', 'admin@example.com')
>>> db.session.add(me)
>>> db.session.commit()
~~~

### Deleting Records

Deleting records is very similar, instead of add() use delete():

~~~python
>>> db.session.delete(me)
>>> db.session.commit()
~~~

### Querying Records

So how do we get data back out of our database? For this purpose Flask-SQLAlchemy provides a query attribute on your Model class

You can then use methods like filter() to filter the records before you fire the select with all() or first()

~~~python
>>> peter = User.query.filter_by(username='peter').first()
>>> peter.id
2
>>> peter.email
u'peter@example.org'
~~~

## Multiple Databases with Bind

Starting with 0.12 Flask-SQLAlchemy can easily connect to multiple databases. To achieve that it preconfigures SQLAlchemy to support multiple "binds"

What are binds? In SQLAlchemy speak a bind is something that can execute SQL statements and is usually a connection or engine. In Flask-SQLAlchemy binds are always engines that are created for you automatically behind the scenes. Each of these engines is then associated with a short key (the bind key). This key is then used at model declaration time to assocate a model with a specific engine。

If no bind key is specified for a model the default connection is used instead (as configured by SQLALCHEMY_DATABASE_URI)

The following configuration declares three database connections. The special default one as well as two others named users (for the users) and appmeta (which connects to a sqlite database for read only access to some data the application provides internally)

~~~
SQLALCHEMY_DATABASE_URI = 'postgres://localhost/main'
SQLALCHEMY_BINDS = {
    'users':        'mysqldb://localhost/users',
    'appmeta':      'sqlite:////path/to/appmeta.db'
}
~~~

The create_all() and drop_all() methods by default operate on all declared binds, including the default one. This behavior can be customized by providing the bind parameter. It takes either a single bind name, '__all__' to refer to all binds or a list of binds. The default bind (SQLALCHEMY_DATABASE_URI) is named None:

>>> db.create_all()
>>> db.create_all(bind=['users'])
>>> db.create_all(bind='appmeta')
>>> db.drop_all(bind=None)

### Referring to Binds

If you declare a model you can specify the bind to use with the __bind_key__ attribute:

~~~python
class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
~~~

Internally the bind key is stored in the table’s info dictionary as 'bind_key'. This is important to know because when you want to create a table object directly you will have to put it in there

~~~python
user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
    info={'bind_key': 'users'}
)
~~~

If you specified the __bind_key__ on your models you can use them exactly the way you are used to. The model connects to the specified database connection itself.