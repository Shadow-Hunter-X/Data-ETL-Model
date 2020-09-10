---
title : JWT
---

## JSON Web Token是什么

JSON Web Token (JWT)是一个开放标准(RFC7519)，它定义了一种紧凑的、自包含的方式，用于作为JSON对象在各方之间安全地传输信息。
该信息可以被验证和信任，因为它是数字签名的


## 何时应用JWT

* Authorization (授权) 

这是使用JWT的最常见场景。一旦用户登录，后续每个请求都将包含JWT，允许用户访问该令牌允许的路由、服务和资源。单点登录是现在广泛使用的JWT的一个特性，因为它的开销很小，并且可以轻松地跨域使用。

* Information Exchange (信息交换) 

对于安全的在各方之间传输信息而言，JSON Web Tokens 无疑是一种很好的方式。
因为JWT可以被签名，例如，用公钥/私钥对，你可以确定发送人就是它们所说的那个人。另外，由于签名是使用头和有效负载计算的，还可以验证内容没有被篡改。


## JSON Web Token的结构

JSON Web Token由三部分组成，它们之间用圆点(.)连接。这三部分分别是：Header、Payload、Signature。
因此，一个典型的JWT看起来是这个样子的：xxxxx.yyyyy.zzzzz


## 使用演示，流程样式