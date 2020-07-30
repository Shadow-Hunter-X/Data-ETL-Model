---
title : wtforms
---

### Form
    class wtforms.form.Form
Forms provide the highest level API in WTForms. They contain your field definitions, delegate validation, take input,
aggregate errors, and in general function as the glue holding everything together 
表单提供了WTForms中最高级别的API。它们包含你的字段定义，委托验证，接受输入，聚合错误。一般来说，它的作用就像胶水一样把所有的东西粘在一起。

* 相关API

validate()
    Validates the form by calling validate on each field, passing any extra Form.validate_<fieldname> validators to the field validator
    通过在每个字段上调用validate来验证表单，并传递任何额外的表单。验证器到字段验证器

populate_obj()
    Populates the attributes of the passed obj with data from the form’s fields
    使用来自表单字段的数据填充Python对象，此对象用于后续的数据处理或存储。但这是一个破坏性的操作,与字段同名的任何属性都将被覆盖(谨慎使用)。

data属性:
    包含每个字段数据的dict。请注意，它是在每次访问属性时生成的，因此在使用它时应小心重复访问可能会非常昂贵

#### 定义Forms

To define a form, one makes a subclass of Form and defines the fields declaratively as class attributes:
要定义一个表单，需要创建一个表单的子类，并以类属性的形式声明地定义字段:

~~~py
# 典型的定义的方法如下,
class MyForm(Form):
    first_name = StringField(u'First Name', validators=[validators.input_required()])
    last_name = StringField(u'Last Name', validators=[validators.optional()])
~~~

#### 使用Forms

对于From的操作上的概念，是整体。将数据整体的拷贝、传输、提取 。
明确是有两份数据：前端的表单数据 对应 后端Python数据对象；对前端数据的提取操作，并转换为后端的数据对象。


### Filed

class wtforms.fields.Field

字段以声明方式定义为表单上的成员:在表单上定义字段时，构造参数将被保存，直到表单实例化为止。在形式实例化时，使用定义中指定的所有参数创建字段的副本。的每个实例
字段保存自己的字段数据和错误列表

~~~python
class MyForm(Form):
    name = StringField(u'Full Name', [validators.required(), validators.length(max=10)])
    address = TextAreaField(u'Mailing Address', [validators.optional(), validators.length(max=200)])
~~~

标签和验证器可以作为顺序参数传递给构造函数，而其他所有参数都应该是顺序参数作为关键字参数传递。

#### 基本字段

|基本字段|对应的HTML标签|
|-------|--------|
|wtforms.fields.BooleanField|\<input type="checkbox"\>|
|wtforms.fields.DateTimeField|存储日期时间的文本字段,匹配格式的日期时间|
|wtforms.fields.DateField|同上|
|wtforms.fields.DecimalField|显示和强制十进制数据的文本字段|
|wtforms.fields.FileField|文件上传字段|
|wtforms.fields.MultipleFileField|允许选择多个文件的文件字段|
|wtforms.fields.FloatField|一个文本字段，除了所有输入都强制为浮点数。错误的输入会被忽略，不会被接受|
|wtforms.fields.IntegerField|文本字段，除了所有输入都强制为整数。错误的输入会被忽略，不会被接受价值|
|wtforms.fields.RadioField||