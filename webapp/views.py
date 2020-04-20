from flask import Flask, render_template
from flask import abort, redirect, url_for

app = Flask(__name__)
import sqlite3
 
conn = sqlite3.connect ('inginious.sqlite')
c = conn.cursor ()

#Mettre toutes les commandes des données ici

c.execute ("SELECT * FROM user_tasks WHERE succeeded = 'false' and task = 'palindrome'")
no1 = len(c.fetchall())   #info qui devrait être introduit dans le graphe
c.execute ("SELECT * FROM user_tasks WHERE succeeded = 'true' and task = 'palindrome'")
yes1 = len(c.fetchall())  #info qui devrait être introduit dans le graphe


conn.close()

@app.route('/')
def index():
        return render_template("index.html")

@app.route('/cours1')
def cours1():
        return render_template("cours1.html")

@app.route('/cours2')
def cours2():
        return render_template("cours2.html")

@app.route('/cours3')
def cours3():
        return render_template("cours3.html")



