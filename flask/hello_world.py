from flask import Flask    # 必须在项目中导入Flask模块，Flask类的一个对象是WSGI应用程序
app = Flask(__name__)      # 当前模块（__name __）的名称作为参数构建Flask实例

@app.route('/')            # 通过装饰器指定URL路由,将路由绑定到hello_world函数
def hello_world():         
   return 'Hello World'

if __name__ == '__main__':  
   app.run()               # 调试执行 

'''
对于装饰器的理解：
1 装饰函数 以函数作为参数，在调用参数函数的前后执行的装饰的功能
2 functions.wrap装饰器，用于消除装饰函数中的特殊属性
3 调用方式使用@ + 装饰函数
'''