from flask import Flask
from flask import json
from flask import request
from random import random
import mysql.connector
import logging

app = Flask(__name__)

@app.route('/status')
def healthcheck():
    mydb = mysql.connector.connect(
      host="mysql",
      user="root",
      password="password",
      database="inventory"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT count(*) FROM users")
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    ## log line
    app.logger.info('Status request successfull')
    return response

@app.route('/metrics')
def metrics():
    mydb = mysql.connector.connect(
      host="mysql",
      user="root",
      password="password",
      database="inventory"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT count(*) FROM users")
    result_users = cursor.fetchall()
    cursor.execute("SELECT count(*) FROM widgets")
    result_widgets = cursor.fetchall()

    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"UserCount":result_users[0][0],"widgets":result_widgets[0][0]}}),
            status=200,
            mimetype='application/json'
    )

    ## log line
    app.logger.info('Metrics request successfull')
    return response

@app.route("/")
def hello():
    ## log line
    app.logger.info('Main request successfull')

    return "Hello World!"
@app.route('/widgets')
def get_widgets() :
  mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="password",
    database="inventory"
  )
  cursor = mydb.cursor()


  cursor.execute("SELECT * FROM widgets")

  row_headers=[x[0] for x in cursor.description] #this will extract row headers

  results = cursor.fetchall()
  json_data=[]
  for result in results:
    json_data.append(dict(zip(row_headers,result)))

  cursor.close()

  return json.dumps(json_data)

@app.route('/users')
def get_users() :
  mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="password",
    database="inventory"
  )
  cursor = mydb.cursor()


  cursor.execute("SELECT * FROM users")

  row_headers=[x[0] for x in cursor.description] #this will extract row headers

  results = cursor.fetchall()
  json_data=[]
  for result in results:
    json_data.append(dict(zip(row_headers,result)))

  cursor.close()

  return json.dumps(json_data)


@app.route('/insert_widget')
def insert_widget():
  mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="password",
    database="inventory"
  )
  cursor = mydb.cursor()
  numrandom = str(random())
  name = 'name-' + numrandom
  description = 'description-' + numrandom
  cursor.execute("INSERT INTO widgets(name, description) VALUES (%s, %s)", (name, description))
  mydb.commit()
  cursor.close()
  return "OK"

@app.route('/insert_user')
def insert_user():
  mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="password",
    database="inventory"
  )
  cursor = mydb.cursor()
  numrandom = str(random())
  name = 'name-' + numrandom
  description = 'description-' + numrandom
  cursor.execute("INSERT INTO users(name, description) VALUES (%s, %s)", (name, description))
  mydb.commit()
  cursor.close()
  return "OK"

@app.route('/initdb')
def db_init():
  mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="password"
  )
  cursor = mydb.cursor()

  cursor.execute("DROP DATABASE IF EXISTS inventory")
  cursor.execute("CREATE DATABASE inventory")
  cursor.close()

  mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="password",
    database="inventory"
  )
  cursor = mydb.cursor()

  cursor.execute("DROP TABLE IF EXISTS widgets")
  cursor.execute("DROP TABLE IF EXISTS users")
  cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
  cursor.execute("CREATE TABLE users (id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, description VARCHAR(255) NOT NULL)")
  cursor.close()

  return 'init database'

if __name__ == "__main__":

    ## stream logs to app.log file
    logging.basicConfig(filename='app.log',level=logging.DEBUG)

    app.run(host='0.0.0.0')