---
title : Airflow Python API -- 常用操作
---

## 常用Operator
	
	日常工作中使用较多的是shell、Python等脚本、网络连接操作、SSH连接等。所以在接下来的演示中将对常用的脚本的使用说明，并延伸到
不同场景下的任务。但是保持的原则还是侧重流程，针对功能以输出信息为主。

### Python Operator

	使用PythonOperator进行操作,主要的代码如下。
	
~~~python

# 1-导入必要的库PythonOperator
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

# 2-设置DAG参数
args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': ,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# 3-创建DAG对象
dag = DAG(
    'py_op_test',
    default_args=args,
    description='Python Operator Test',
    schedule_interval=timedelta(days=1),
)

# 4-Python回调处理函数
def print_context(ds, **kwargs):
    print("------information------\n")
    pprint(kwargs)
    print(ds)
    print("------information------\n")
    return 'done'
	
# 5-定义Python Operator	
run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)

~~~
	
### Bash Operator
	
### Http Operator

### SSH Operator

### 依赖关系
	
### 执行周期

