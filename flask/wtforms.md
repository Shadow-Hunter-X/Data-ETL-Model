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


### Filed-表单字段

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
|wtforms.fields.RadioField|表示\<input type = 'radio'\> HTML表单元素||
|wtforms.fields.SelectField|Select字段保留一个选择属性，它是一个(值、标签)对序列|
|wtforms.fields.SelectMultipleField|与普通的选择字段没有什么不同，只是这个字段可以接受(并验证)多个选择|
|wtforms.fields.SubmitField|表示\<input type = 'submit'\>表单元素|
|wtforms.fields.HiddenField|表示\<input type="hidden"\>|
|wtforms.fields.PasswordField|表示\<input type="password"\>|
|wtforms.fields.TextAreaField|这个字段表示一个HTML文本框。并可用于取多行输入|
|wtforms.fields.Label|\<label\>|

#### Field Enclosures

    Field Enclosures允许您拥有表示字段集合的字段，以便表单可以由可以表示多个可重用组件或更复杂的数据结构，如列表和嵌套对象。
使用 wtforms.fields.FormField ：将一个表单封装为另一个表单中的字段。
~~~python
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = StringField('Number')

class ContactForm(Form):
    first_name = StringField()
    last_name = StringField()
    mobile_phone = FormField(TelephoneForm)         # 使用FormFiled
    office_phone = FormField(TelephoneForm)         # 使用FormFiled

~~~

#### FieldList

    封装同一字段类型的多个实例的有序列表，将数据保持为列表。
wtforms.fields.FieldList

~~~python
class IMForm(Form):
    protocol = SelectField(choices=[('aim', 'AIM'), ('msn', 'MSN')])
    username = StringField()

class ContactForm(Form):
    first_name = StringField()
    last_name = StringField()
    im_accounts = FieldList(FormField(IMForm)
~~~

### Validators--验证器

验证器只接受输入，验证它是否满足某些条件，比如字符串的最大长度然后返回。如果验证失败，则引发ValidationError。
这个系统非常简单和灵活，并允许在字段上连接任意数量的验证器。

* class wtforms.validators.ValidationError(message=”, *args, **kwargs)

    当验证器验证其输入失败时引发

* class wtforms.validators.StopValidation(message=”, *args, **kwargs)

    导致验证链停止

#### 内建验证器

|验证器|说明|
|---------|--------|
|wtforms.validators.DataRequired(message=None)|检查字段的数据是否为"真"，否则停止验证链|
|wtforms.validators.Email(message=None)|验证电子邮件地址| 
|wtforms.validators.EqualTo(fieldname, message=None)|比较两个字段的值|
|wtforms.validators.InputRequired(message=None)|检查数据是否有提供。与DataRequired的不同：|
|wtforms.validators.IPAddress(ipv4=True, ipv6=False, message=None)|检查是否为正确IP地址|
|wtforms.validators.Length(min=-1, max=-1, message=None)|验证字符串的长度|
|wtforms.validators.MacAddress(message=None)|验证Mac地址|
|wtforms.validators.NumberRange(min=None, max=None, message=None)|验证是否在最大和最小值间|
|wtforms.validators.Optional(strip_whitespace=True)|允许空输入并停止验证链继续|
|wtforms.validators.Regexp(regex, flags=0, message=None)|根据用户提供的正则表达式验证字段|
|wtforms.validators.URL(require_tld=True, message=None)|验证URL是否正确|
|wtforms.validators.UUID(message=None)|验证一个UUID|
|wtforms.validators.AnyOf(values, message=None, values_formatter=None)|将输入的数据与有效的输入序列进行比较。|
|wtforms.validators.NoneOf(values, message=None, values_formatter=None)|将输入的数据与无效的输入序列进行比较|

### Widgets

小部件是用于将字段呈现为其可用表示的类，通常是XHTML。当一个字段调用时，默认行为是将呈现委托给它的小部件。提供这种抽象是为了让小部件能够
很容易创建，以定制现有字段的呈现。

注意，所有内置的小部件都会在呈现一个“html -安全”的unicode字符串子类时返回框架(Jinja2、Mako、Genshi)将被识别为不需要自动转义。

#### 内置Widget

* wtforms.widgets.ListWidget(html_tag=’ul’, prefix_label=True)

将字段列表呈现为ul或ol列表。它用于将许多内部字段封装为子字段的字段。小部件将尝试迭代字段
访问子字段并调用它们以呈现它们。如果设置了prefix_label，则子字段的标签将在字段之前打印，否则将在字段之后打印。后者是有用的迭代单选或复选框

* wtforms.widgets.TableWidget(with_table_tag=True)

将字段列表呈现为一组带有th/td对的表行。如果with_table_tag为真，则在行周围放置一个封闭的<table>。
隐藏字段将不会与一行一起显示，相反，该字段将被推入后续的表行确保XHTML的有效性。字段列表末尾的隐藏字段将出现在表外部。

* wtforms.widgets.Input(input_type=None)
  
渲染一个基本的输入字段。这被用作大多数其他输入字段的基础

* wtforms.widgets.TextInput

