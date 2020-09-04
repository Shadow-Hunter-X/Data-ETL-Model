---
title : Postman - 使用
---

鉴于使用Flask编写Restful API，对其进行测试时候，使用Postman进行测试。所以这里先对Postman的使用方法进行说明。

## 关于Postman

Postman is a collaboration platform for API development. Postman's features simplify each step of building an API and streamline collaboration so you can create better APIs—faster。

Postman是API开发的协作平台。Postman的功能简化了构建API的每一步，简化了协作，因此可以更快地创建更好的API。

官方文档中，主要说明如下：

* Making requests
* Testing APIs
* Building and managing APIs
* Publishing APIs
* Collaborating with your team
* Developing with Postman

## Sending requests

If you're building a client app or just need to connect to an API, check out some Postman essentials 。

进行首次使用Postman Request请求中的演示，如下图的Gif所示，对官方提供的API： postman-echo.com/get进行请求 。

[请求演示](res/1-request.gif)

### 创建requests

Your requests can include multiple details determining the data Postman will send to the API you are working with. At the very least you will need to enter a URL and choose a method, but you can optionally specify a variety of other details

在请求中可以包含诸多的信息，通过Postman向对应的API发送。最简单的操作就是：指定请求方法，输入对应的Restful API。

创建一个request的方法有以下两种： 一种是在前面演示通过添加一个tab ；另一种是 new --> Request --> 配置request名字、描述信息 --> 创建collection、并保存

[请求演示](res/2-request.gif)

### 添加请求参数信息

For example, if you're working with an API for a To Do list application, 
you might use a GET method to retrieve the current list of tasks, 
a POST method to create a new task, and a PUT or PATCH method to edit an existing task.

根据不同的方法，参数的构造形式也是不同的。






