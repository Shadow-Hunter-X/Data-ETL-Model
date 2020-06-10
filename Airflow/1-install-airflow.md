---
title : 安装Airflow
---

## 快速安装
在联网状态下，在线安装过程很简单,操作过程如下：

~~~shell

# 首先为Airflow配置一个家目录，默认情况下在 ~/ariflow , 可以通过配置变量AIRFLOW_HOME进行修改。
export AIRFLOW_HOME=~/airflow

# 通过pip安装Airflow
pip install apache-airflow

# 初始化数据库，默认使用的sqlite.所以无需做其他而外配置
airflow initdb

#开启Airflow Web服务
airflow webserver -p 8888

#开启调度器

airflow scheduler

~~~

## 配置说明

成功安装后，在AIRFLOW_HOME目录中，生成一个名为airflow.cfg的文件。airflow.cfg是配置的方法之一，另一个方法是直接配置环境变量,
就像前面安装中的export AIRFLOW_HOME=~/airflow 操作。其实在airflow.cfg中的配置信息到使用环境变量的对应关系如下：
以下以cfg文件的格式：通过方括号定义配置小节，如[core]、[secrets]、[secrets]、[hive]等，在这些小节下以key=value格式配置。
所有想要通过环境变量对应的格式就变为：AIRFLOW__{SECTION}__{KEY}

~~~shell

[core]
dags_folder = /home/neo/airflow/dags
base_log_folder = /home/neo/airflow/logs
executor = SequentialExecutor

sql_alchemy_conn = sqlite:////home/neo/airflow/airflow.db
.......................

[secrets]
backend =
backend_kwargs =
.....

[cli]
api_client = airflow.api.client.local_client
endpoint_url = http://localhost:8080

[api]
auth_backend = airflow.api.auth.backend.default

[operators]
........
default_owner = airflow
default_cpus = 1
default_ram = 512
default_disk = 512
default_gpus = 0

[hive]
default_hive_mapred_queue =

~~~

### 数据库的配置

由于Airflow默认使用Sqlite作为数据库，在执行完airflow initdb后，就在数据库文件中创建表，创建的表如下所示：

![airflow-database-table](res/1-airflow-db.png)

理解了这些数据库表的,能更好的理解Airflow的处理流程，以下对一些表进行说明。

如果要配置使用其他的数据（Mysql、Postgres），则修改airflow.cfg中的sql_alchemy_conn字段后，重新调用airflow initdb命令。
针对不同的配置方式：mysql+mysqldb://user:password@host[:port]/dbname



