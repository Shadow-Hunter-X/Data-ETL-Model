---
title : Transformation操作
---

本篇将进行详细的说明Transformation的操作，涉及各方面。在本例中将构造一个时间计算的例子进行说明，
模拟一家公司的员工的上班的打卡记录，并通过和上班时间对比进行绩效的判定。

## 构造时间计算的Transformation

* 使用Data Grid构建时间数据用于测试： Design --> Input -- > Data Grid .
  
  将鼠标悬停在Data Grid上，就会有Step的说明 ： 输入静态的行数据，用于数据的测试、引用或demo 。

* 在Data Grid中构建数据 ： 左键双击或右键点击选Edit；在元数据(Meta)标签下输入列名类型和格式，在数据(Data)标签下输入数据。

  数据的原型为： 员工编号 、 打卡时间  、 上班时间  ；并向其中插入3条数据 。

![创建Data Grid并使用测试数据](res/2-transformation-grid-data.gif)

* 创建Calculate，用于计算员工是否有迟到:  Design --> Transform -- > Calculator

将鼠标悬停在Calculator上查看其说明： 通过简单的计算，创建新的列，新列的类型为 **整型**

* 通过Hop将Data Grid和Calculator连接，并在Calculator中用work_in - clock_in，以分钟计算。

![创建Calculator计算时间差](res/2-transformation-calculator.gif)

* 使用Number Ranger对计算打卡时间差评定绩效：如果不确定 Number Ranger在哪个标签下，可以在Steps搜索框中进行搜索

评定的标准为:  提前10分钟到为优 ； 提前10分钟以内为良 ； 迟到大于10分钟为差 

* 通过Hop将Calculator和Number ranger连接

![使用Number Ranger进行评级](res/2-transformation-number.gif)


## 构造脏数据用于调试和错误说明


## 流的概念

1 注意在input和output列

2 其他的就看PDF中的内容吧