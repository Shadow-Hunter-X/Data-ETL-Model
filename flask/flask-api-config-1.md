---
title : flask-api-config
---

开始说明介绍Flask中的API


## Config

类定义： class flask.Config(root_path, defaults=None)

Works exactly like a dict but provides ways to fill it from files or special dictionaries. There are two common patterns to populate the config.

* Either you can fill the config from a config file 

~~~python
app.config.from_pyfile('yourconfig.cfg')
~~~

* alternatively you can define the configuration options in the module that calls from_object() or provide an import path to a module that should be loaded

~~~python
DEBUG = True
SECRET_KEY = 'development key'
app.config.from_object(__name__)
~~~

>>> In both cases (loading from any Python file or loading from modules), only uppercase keys are added to the config

### 具体加载配置信息的方法

* from_envvar(variable_name, silent=False)

Loads a configuration from an environment variable pointing to a configuration file.

* from_json(filename, silent=False)

Updates the values in the config from a JSON file. This function behaves as if the JSON object was a dictionary and passed to the from_mapping() function

* from_mapping(*mapping, **kwargs)

Updates the config like update() ignoring items with non-upper keys

* from_object(obj)

Updates the values from the given object. An object can be of one of the following two types:
a string: in this case the object with that name will be imported
an actual object reference: that object is used directly

* from_pyfile(filename, silent=False)

Updates the values in the config from a Python file. This function behaves as if the file was imported as module with the from_object() function

* get_namespace(namespace, lowercase=True, trim_namespace=True)

Returns a dictionary containing a subset of configuration options that match the specified namespace/prefix. Example usage:

~~~python
app.config['IMAGE_STORE_TYPE'] = 'fs'
app.config['IMAGE_STORE_PATH'] = '/var/app/images'
app.config['IMAGE_STORE_BASE_URL'] = 'http://img.website.com'
image_store_config = app.config.get_namespace('IMAGE_STORE_')
~~~



