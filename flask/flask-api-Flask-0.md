---
title: flask.Flask
---

## Flask 

类：class flask.Flask(import_name, static_url_path=None, static_folder='static', static_host=None, host_matching=False, subdomain_matching=False, template_folder='templates', instance_path=None, instance_relative_config=False, root_path=None)

The flask object implements a WSGI application and acts as the central object. It is passed the name of the module or package of the application. Once it is created it will act as a central registry for the view functions, the URL rules, template configuration and much more


Usually you create a Flask instance in your main module or in the __init__.py file of your package like this:

~~~python
from flask import Flask
app = Flask(__name__)
~~~

### 类中的方法

* add_template_filter(f, name=None)
	Register a custom template filter. Works exactly like the template_filter() decorator.
	
* add_template_global(f, name=None)
	Register a custom template global function. Works exactly like the template_global() decorator
	
* add_template_test(f, name=None)
	Register a custom template test. Works exactly like the template_test() decorator

* add_url_rule(rule, endpoint=None, view_func=None, provide_automatic_options=None, **options)
Connects a URL rule. Works exactly like the route() decorator. If a view_func is provided it will be registered with the endpoint.

* after_request(f)
Register a function to be run after each request

* app_context()

Create an AppContext. Use as a with block to push the context, which will make current_app point at this application.

An application context is automatically pushed by RequestContext.push() when handling a request, and when running a CLI command. Use this to manually create a context outside of these situations