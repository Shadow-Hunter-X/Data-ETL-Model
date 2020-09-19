---
title : 7-Kettle-数据转换
---

前面说明的数据处理，都是查找、过滤、汇总这样不会对数据集的结构发生改变的操作。但这些只是数据的部分，还有诸如行列转换、维度化处理等。
所以将进行对这些操作进行说明。

## 行列的转换

	使用Transform分组下的Row Normaliser和Row Dennormaliser两个实施行列间的转换。

做一个汇总：计算一个产品的max和min值，将这个进行换转为列；然后实施逆运算。

* Input分组 --> Text File Input --> 配置orderdetails.csv文件。

* statics分组 --> group by --> 以OrderId进行分组，计算单价最高和最低的
![]()

* transform分组 --> Row Normaliser   --> 配置将列转为行 （一行变多行）
![]()

* transform分组 --> Row Denormaliser -->  配置将行转为列 （多行变一行）
![]()

## 时间维度 

