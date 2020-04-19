from flask import Flask, render_template

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
def index(yes = None, no = None ):
        return render_template("index.html", yes= yes1 , no = no1 )

