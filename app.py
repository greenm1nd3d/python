import markdown
import os
import yaml

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_restful import Resource, Api

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

api = Api(app)
mysql = MySQL(app)

@app.route("/", methods=['GET'])
def index():
	"""Display instructions on how to use the services"""

	f = open('README.md', 'r')
	content = f.read()
	return markdown.markdown(content)


class Order(Resource):
	def get(self):
		"""Retrieve order data by given user first name"""
		arr = []
		user_fname = request.args.get('user_first_name')

		cur = mysql.connection.cursor()
		sql = "SELECT \
				o.order_id, \
				o.order_name, \
				u.user_first_name, \
				u.user_last_name \
			FROM orders o \
			INNER JOIN users u \
				ON o.order_user_id = u.user_id \
			WHERE u.user_first_name = %s"
		result = cur.execute(sql, (user_fname,))

		if result > 0:
			orders = cur.fetchall()
			for order in orders:
				arr.append(
					{'order_id': order[0], 'order_name': order[1], 'user_first_name': order[2], 'user_last_name': order[3]}
				)

		cur.close()

		return jsonify({'orders': arr})

	def post(self):
		"""Create a new order"""
		user_id = request.form.get('user_id')
		order_name = request.form.get('order_name')

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO orders (order_name, order_user_id) VALUES (%s, %s)", (order_name, int(user_id)))
		mysql.connection.commit()
		cur.close()

		return jsonify({'result': 201, 'message': 'Order successfully created'})


class Users(Resource):
	def get(self):
		"""Retrieve list of users"""
		arr = []
		cur = mysql.connection.cursor()
		result = cur.execute("""SELECT user_first_name, user_last_name FROM users""")
		if result > 0:
			users = cur.fetchall()
			for user in users:
				arr.append(
					{'first_name': user[0], 'last_name': user[1]}
				)

		cur.close()

		return jsonify({'users': arr})


class User(Resource):
	def get(user_id):
		"""Retrieve user by given user_id"""
		myusers = [user for user in theusers if user['user_id'] == user_id]
		return jsonify({'user': myusers[0]})

	def post(self):
		"""Create a new user"""
		fname = request.form.get('first_name')
		lname = request.form.get('last_name')

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users (user_first_name, user_last_name) VALUES (%s, %s)", (fname, lname))
		mysql.connection.commit()
		cur.close()

		return jsonify({'result': 201, 'message': 'User successfully created'})


api.add_resource(Order, '/order', '/createorder')
api.add_resource(User, '/createuser')
api.add_resource(Users, '/users')

if __name__ == '__main__':
	app.run(debug=True, port=8888)
