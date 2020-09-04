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




 
 
