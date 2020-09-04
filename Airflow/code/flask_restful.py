from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy  import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:iamneo@127.0.0.1:3306/test'   #连接Mysql数据库
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\test.db'    	#windows上的书写格式

db = SQLAlchemy(app)      # 创建SQLAlchemy对象，但其封装的内容比原来的多：如session、model、engine等封装在一个对象中。

class Authors(db.Model):
"""
	定义数据模型类型，对应的于数据库中的表。ORM：关系数据库的表结构映射到对象
"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	specialisation = db.Column(db.String(50))
	
	def create(self):
		db.session.add(self)
		db.session.commit()
		return self
	
	def __init__(self, name, specialisation):
		self.name = name
		self.specialisation = specialisation
		
	def __repr__(self):
		return '<Product %d>' % self.id
	
db.create_all()     	# 创建表，如果存在则忽略，执行以上代码

class AuthorsSchema(ModelSchema):			   #使用marshmallow中的模型说明
	class Meta(ModelSchema.Meta):
		model = Authors
		sqla_session = db.session

	id = fields.Number(dump_only=True)
	name = fields.String(required=True)
	specialisation = fields.String(required=True)
	
@app.route('/authors', methods = ['GET'])
def index():
	get_authors = Authors.query.all()
	author_schema = AuthorsSchema(many=True)    #参数many设置为True是，长返回所有的数据
	authors = author_schema.dump(get_authors)
	return make_response(jsonify({"authors": authors}))
	
@app.route('/authors/<id>', methods = ['GET'])
def get_author_by_id(id):
	get_author = Authors.query.get(id)
	author_schema = AuthorsSchema()
	author = author_schema.dump(get_author)
	return make_response(jsonify({"author": author}))
	
@app.route('/authors/<id>', methods = ['PUT'])
def update_author_by_id(id):
	data = request.get_json()
	get_author = Authors.query.get(id)
	if data.get('specialisation'):
		get_author.specialisation = data['specialisation']
	if data.get('name'):
		get_author.name = data['name']
	db.session.add(get_author)
	db.session.commit()
	author_schema = AuthorsSchema(only=['id', 'name', 'specialisation'])
	author = author_schema.dump(get_author)
	return make_response(jsonify({"author": author}))
	
@app.route('/authors/<id>', methods = ['DELETE'])
def delete_author_by_id(id):
	get_author = Authors.query.get(id)
	db.session.delete(get_author)
	db.session.commit()
	return make_response("",204)

@app.route('/authors', methods = ['POST'])
def create_author():
	data = request.get_json()
	author_schema = AuthorsSchema()
	author = author_schema.load(data)
	result = author_schema.dump(author.create())
	return make_response(jsonify({"author": result}),200)

if __name__ == "__main__":
	app.run(debug=True)
		