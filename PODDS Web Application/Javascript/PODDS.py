from flask import Flask,render_template,request


#import sqlite3

import flask




app = Flask(__name__)



@app.route('/')
def welcome():
	#flask.url_for('static')
#	return render_template('PODDS_js.html')
	return render_template('VCDM_js.html')
#@app.route('/test')

@app.route('/PODDS')
def PODDS():
	return render_template('PODDS_js.html')
#def test():
#	return "Dave"

