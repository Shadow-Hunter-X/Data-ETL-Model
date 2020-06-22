---
title : airflow
---

通过使用Airflow中的Python代码，强化前面学些的相关概念，其次对Python API的具象认识。
以下代码是官方提供的tutorial.py脚本


## tutorial.py脚本代码

~~~python
from datetime import timedelta  
from airflow import DAG   								 # 导入DAG对象      
from airflow.operators.bash_operator import BashOperator # 导入具体的Operator
from airflow.utils.dates import days_ago    			 # 日期计算             

# 配置参数，构建DAG时传入，可应用于所有的任务
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

# 创建DAG对象：第一个参数DAG名字，第二个参数配置参数，第三个参数描述信息，第四个参数执行周期
dag = DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
)

# 创建t1 Operator,任务id为 print_date,任务命令为date,并绑定到dag
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

# 创建t2 Operator,任务id为 sleep,任务命令为sleep 5,并绑定到dag
t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)


# 添加dag和task的说明文档
dag.doc_md = __doc__

t1.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
"""

# Airflow利用Jinja模板实现参数化功能，以下定义模板参数后传入任务中
templated_command = """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
    echo "{{ params.my_param }}"
{% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag,
)

# 设置任务间的依赖关系
t1 >> [t2, t3]
~~~

## 测试和执行

* 首先将上述的脚本保存到Airflow中在airflow.cfg配置DAG文件夹下，默认在~/airflow/dags。

~~~shell
python ~/airflow/dags/tutorial.py
~~~

如果成功执行，则说明脚本没有严重的错误，接下来对使用airflow命令对任务进行测试。

~~~shell
airflow list_dags     		 # 查看当前使用的dag

airflow list_tasks tutorial  # 通过dag_id：turorial查看其下的任务

airflow list_tasks tutorial --tree   # 通过dag_id：turorial查看其下的任务，以层级关系体现
~~~

~~~shell

airflow test tutorial print_date 2020-06-22   # 测试print_date任务，执行时间为2020-06-22

airflow test tutorial sleep 2020-06-22        # 测试sleep任务，执行时间为2020-06-22

airflow test tutorial templated 2020-06-22    # 测试templated任务，执行时间为2020-06-22
   