---
title : Airflow Conpect
---

Airflow平台是一个用于描述、执行、监控工作流的工具。通过编写Python脚本，支持不同类型的任务。

## 主要概念&核心构架

对Airflow中最核心的概念和构架思想进行说明,并在最后结合对应API进行演示操作。

### DAG-有向无环图

DAG-有向无环图，是要运行的所有Tasks的集合，组织方式反映了Task的关系和依赖。DAG通过Python脚本编写，以代码定义了DAG的结构，包括具体的任务和任务间的依赖关系。
DAG描述的是期望如何执行工作流程，但并不关心任务具体要做了什么，DAG的任务就是确保它们所做的任何事情在正确的时间、以正确的顺序、或以正确的方式处理各种类型的任务。
DAG通过Python文件定义，存在在定义的DAG_FOLDER文件夹下，执行每个文件中的代码来动态构建DAG对象。

DAG的配置参数，配置参数字典被传递到DAG，将把它们应用任何操作符上。这使得可以很容易地将一个通用参数应用于多个操作符，而不必多次键入它。
以下是常用的配置产生。

~~~python
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
~~~

创建还是用DAG的基本代码。
~~~python
# 1-导入必要的库
from airflow import DAG
from airflow.utils.dates import days_ago

# 2-设置DAG参数
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
} 

# 3-创建DAG
dag = DAG(
    'test',
    default_args=default_args,
    description='simple test DAG',
    schedule_interval=timedelta(days=1),
)
~~~

### Operator

DAG描述如何运行一个工作流，实际完成何种操作由Operator来定义。Operator描述工作流中的单个任务,可以独立运行,不需要与其他Operator共享资源。
DAG将确保Operator以正确的顺序运行,除了这些依赖关系,Operator通常独立运行。如果两个Operator需要共享信息,比如文件名或少量数据,
可以考虑将它们合并到一个操作符中，或使用XComs。

在Airflow中，提供了必要的常用Operator，如下所示。

|Operator|功能|
|---------|--------|
|BashOperator|执行Bash命令|
|PythonOperator|执行Python函数|
|EmailOperator|用于发送邮件|
|SimpleHttpOperator|用于发送HTTP请求|
|DockerOperator|Docker操作相关|
|HiveOperator|Hive操作|
|MySqlOperator, SqliteOperator, PostgresOperator, MsSqlOperator, OracleOperator, JdbcOperator等|用于执行SQL|

Operator只有在被分配到DAG时才会被加载，所以Operator的创建方法和分配的代码如下。

~~~python
# 导入必要的库
from airflow import DAG
from airflow.operators.bash_operator import *

dag = DAG('my_dag', start_date=datetime(2020, 1, 1))

# 立即分配到dag
explicit_op = DummyOperator(task_id='op1', dag=dag)

# 推迟分配到dag
deferred_op = DummyOperator(task_id='op2')
deferred_op.dag = dag
~~~

### Relationship

前面讲述的DAG、Operator相关的概念。并通过代码简单演示了创建方法、分配方式。对于Operator间的执行顺序、依赖关系在这小节说明。
通过使用set_upstream()和set_downstream()函数,或使用 >>、<<操作符。

~~~python

from airflow import DAG
from airflow.operators.bash_operator import *

dag = DAG('my_dag', start_date=datetime(2020, 1, 1))
op1 = DummyOperator(task_id='op1', dag=dag)
op2 = DummyOperator(task_id='op2', dag=dag)

# 1-任务op1在任务op2之前执行,使用 >> 操作符和 set_downstream 函数 
op1 >> op2
op1.set_downstream(op2)

# 2-任务op2在任务op1之后执行,使用 << 操作符和 set_upstream 函数 
op2 << op1
op2.set_upstream(op1)

# 3-在关系链中直接使用DAG
dag >> op1 >> op2
#等价于
op1.dag=dag
op1.set_downstream(op2)

# 4-针对任务列表的使用
op3 = DummyOperator(task_id='op3', dag=dag)
op4 = DummyOperator(task_id='op4', dag=dag)
op1 >> [op3,op4] >> op2
#等价于
op1 >> op3 >> op2
op1 >> op4 >> op2

# 5-可以使用chain、cross_downstream 在特定情况下更容易设置操作符之间关系的方法
[op1, op2, op3] >> op4
[op1, op2, op3] >> op5
[op1, op2, op3] >> op6
# 等价于
cross_downstream([op1, op2, op3], [op4, op5, op6])


op1 >> op2 >> op3 >> op4 >> op5
#等价于
chain(op1, op2, op3, op4, op5)
~~~


### Tasks

一旦Operator被实例化，它就被称为-任务。参数化任务成为DAG中的一个节点。任务实例表示任务的特定运行，并被描述为DAG、任务和时间点的组合。任务实例还具有指示性状态，可以是运行、成功、失败、跳过、重试等。

任务的完整生命周期如下所示:
No Status: 调度器创建了空任务实例
Scheduled: 调度程序确定的任务实例需要运行
Queued: 调度器将任务发送给executor以在队列上运行
Running: worker拾取任务并正在运行它
Success: 任务完成

![Task生命周期](res/task_lifecycle_diagram.png)


