from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'SecretKey'
mysql = MySQLConnector(app, 'friends')

@app.route('/')
def index():
	query="SELECT * FROM friends"
	friends=mysql.query_db(query)
	return render_template('index.html',friends=friends)


@app.route('/friends')
def create():
	count=0
	if(request.form[first_name])<1:
		count+=1
		flash("invalid")
	if(request.form[last_name])<1:
		count+=1
		flash("invalid")
	if(request.form[email])<1:
		count+=1
		flash("invalid")
	elif not(EMAIL_REGEX.match(request.form[email])):
		count+=1
		flash("format invalid")
	if count > 0:
		return redirect('/')
	query="INSERT INTO friends (f_name,l_name,email,created_at,updated_at) VALUES (:first_name,last_name,email,NOW(), NOW())"
	data= {
		  'first_name':request.form['first_name'],
		  'last_name':request.form['last_name'],
		  'email':request.form['email'],
		  'created_at':request.form['NOW()']
		  }
	mysql.query_db(query,data)
	return redirect('/')

@app.route('/friends/<friends_id>/edit', methods=['POST'])
def edit(friends_id):
	query="SELECT * FROM friends WHERE id=:id"
	data={'id':friends_id}
	friends=mysql.query_db(query,data)
	return render_template ('edit.html', friends=friends)


@app.route('/friends/<friends_id>', methods=['POST'])
def update(friends_id):
	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id"
	data= {
			'first_name': request.form['first_name'], 
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'id': friends_id
			}
	mysql.query_db(query,data)

@app.route('/friends/<friends_id>/delete', methods=['POST'])
def delete(friends_id):
	query="SELECT * FROM friends WHERE id=:id"
	data={'id':friends_id}
	friends=mysql.query_db(query,data)
	return render_template("delete.html", friends=friends[0]) 



@app.route('/friends/<friends_id>/deleteconfirm', methods=['POST'])
def deleteconfirm(friends_id):	
	# if request.form['delete']=='Yes':
		print "****************", friends_id
		query = "DELETE FROM friends WHERE id = :id"
		data = {'id':friends_id} #change friend_id to int?
		mysql.query_db(query,data)
		return redirect('/')




app.run(debug=True)

