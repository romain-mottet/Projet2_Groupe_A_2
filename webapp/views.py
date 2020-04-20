from flask import Flask, render_template
from flask import abort, redirect, url_for

app = Flask(__name__)
import sqlite3
 
def info_course (name):
    """
    pré: Le nom du cours en générale
    post: return une liste sous la forme [nombre de réussite globale du cours, nombre de fail globale du cours, nombre d'essaye total, nombre d'essaye moyen]
    """
    conn = sqlite3.connect ('inginious.sqlite')
    c = conn.cursor ()

    l= []

    #trouve le nombre de réussite globale 
    c.execute ("SELECT * FROM user_tasks WHERE course = '{}' and succeeded = 'true'".format(name))
    r_global = len(c.fetchall())   #info qui devrait être introduit dans le graphe
    l.append (r_global)

    #Trouve le nombre de ratés de cours 
    c.execute ("SELECT * FROM user_tasks WHERE course = '{}' and succeeded = 'false'".format(name))
    f_global = len(c.fetchall())   #info qui devrait être introduit dans le graphe
    l.append (f_global)

    #Trouve le nombre d'essaye total
    c.execute ("SELECT tried FROM user_tasks WHERE course = '{}'".format(name))
    tried = c.fetchall ()
    nbr_tried = 0
    for e in range (0, len (tried)):
        newstring = ""
        for i in range (0, len (tried [e])):
            if tried [e][i] == "(" or tried [e][i] == ")" or tried [e][i] == ",":
                "nothing"
            else:
                newstring += str (tried [e][i])
        nbr_tried += int (newstring)
    l.append (nbr_tried)

    
    #trouve le nombre d'essaye moyen 
    moyenne_tried = nbr_tried //(l[0]+l[1])
    l.append (moyenne_tried)

    conn.close()
    return l   

@app.route('/')  #page d'acceuil
def index():
        return render_template("index.html")

@app.route('/LSINF1252')  #équivalent du cours 1
def LSINF1252():
        return render_template("LSINF1252.html")

@app.route('/LEPL1402')   #équivalent du cours 2
def LEPL1402():
        return render_template("LEPL1402.html")

@app.route('/LSINF1101_PYTHON')   #équivalent du cours 3
def LSINF1101_PYTHON():
        return render_template("LSINF1101_PYTHON.html")

