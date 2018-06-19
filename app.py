from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/display/')
def display():
   # TODO: select latest new object from the db display table
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
       # TODO: select a new object from the db, insert into display table, and push post to tumblr
       cur = db.cursor()
       cur.execute("select distinct Noun from Entries")
       words = cur.fetchall();

       return render_template('done.html', object=words)
  
   cur = db.cursor()
   cur.execute("select distinct Noun from Entries")
   words = cur.fetchall();

   return render_template('interface.html', words=words)
