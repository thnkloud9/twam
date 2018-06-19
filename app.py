from flask import Flask, render_template, request
import sqlite3
import sys
from time import gmtime, strftime

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/display/')
def display():
   con = sqlite3.connect("twam.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from Display ORDER BY created DESC LIMIT 1")
   
   items = cur.fetchall();
   return render_template('display.html', items=items)


@app.route('/interface/', methods=['POST', 'GET'])
def interface():
   db = sqlite3.connect("twam.db")
   db.row_factory = sqlite3.Row

   if request.method == 'POST':
       whereWordString = ""
       title = ""
       wordString = request.values.get("words")
       words = wordString.split(",")

       # select a new object from the db, insert into display table, and push post to tumblr
       query = "SELECT * FROM Entries WHERE ("
       for word in words:
           title += word + " "
           query += "Noun like '%" + word + "%' OR "

       query += "Noun like '%default%'" 
       query += ") ORDER BY RANDOM() LIMIT 1"
     
       cur = db.cursor()
       cur.execute(query);
       items = cur.fetchall();

       # insert into the display table
       create = 'create table if not exists Display (Id INT, Title TEXT, Description TEXT, Created TEXT)'
       cur.execute(create)

       for item in items:
           insert = 'INSERT INTO Display VALUES ('
           insert += str(item['Id']) + ','
           insert += "'" + str(title).strip() + "',"
           insert += "'" + str(item['Description']) + "',"
           insert += "'" + str(strftime("%s", gmtime())) + "')"

           sys.stderr.write(insert)
           cur.execute(insert)
           db.commit() 

           # TODO: post to tumblr

       return render_template('done.html', items=items, words=words)
  
   cur = db.cursor()
   cur.execute("select distinct Noun from Entries")
   words = cur.fetchall();

   return render_template('interface.html', words=words)


@app.route('/done/')
def done():
   con = sqlite3.connect("twam.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from Display ORDER BY created DESC LIMIT 1")
   
   items = cur.fetchall();
   return render_template('done.html', items=items)
