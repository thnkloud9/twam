from flask import Flask, render_template
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/display/')
def display():
    # TODO: select latest new object from the db display table
    return render_template('display.html', name='TODO', desc='ALSO TODO')

@app.route('/interface/', methods=['POST', 'GET'])
def interface():
    #if request.method == 'POST':
    # TODO: select a new object from the db, insert into display table, and push post to tumblr
    return render_template('interface.html', name='TODO')
