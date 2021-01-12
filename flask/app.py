from flask import Flask, request, jsonify, Response
import mysql.connector
from mysql.connector import Error

config = {
    'user': 'root',
    'password': 'demo',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'pendect'
}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "<h1 style='text-align: center'>Dev Pendect API</h1>"

@app.route('/stories', methods=['GET'])
def all_stories():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('SELECT id, title, img_url, content FROM stories')
        records = cursor.fetchall()
        results = [{'id': row[0], 'title': row[1], 'img_url': row[2], 'content': row[3]} for row in records]
        res = jsonify(results)
        res.headers['Access-Control-Allow-Origin'] = '*'
        cursor.close()
        connection.close()
        return res

    except mysql.connector.Error as error:
        print("except block")
        return "Query Failed {}".format(error)

@app.route('/story', methods=['GET'])
def story():
    query_params = request.args
    id = query_params['id']

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("""SELECT id, title, img_url, content FROM stories WHERE id = {}""".format(id))
        row = cursor.fetchone()
        result = {'id': row[0], 'title': row[1], 'img_url': row[2], 'content': row[3]}
        res = jsonify(result)
        res.headers['Access-Control-Allow-Origin'] = '*'
        cursor.close()
        connection.close()
        return res

    except mysql.connector.Error as error:
        print("except block")
        return "Query Failed {}".format(error)


if __name__ == '__main__':
	app.run(host='0.0.0.0')



