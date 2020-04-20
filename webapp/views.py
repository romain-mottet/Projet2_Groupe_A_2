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

    lcourse= []

    #trouve le nombre de réussite globale 
    c.execute ("SELECT * FROM user_tasks WHERE course = '{}' and succeeded = 'true'".format(name))
    r_global = len(c.fetchall())   #info qui devrait être introduit dans le graphe
    lcourse.append (r_global)

    #Trouve le nombre de ratés de cours 
    c.execute ("SELECT * FROM user_tasks WHERE course = '{}' and succeeded = 'false'".format(name))
    f_global = len(c.fetchall())   #info qui devrait être introduit dans le graphe
    lcourse.append (f_global)

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
    lcourse.append (nbr_tried)

    
    #trouve le nombre d'essaye moyen 
    if (lcourse[0]+lcourse[1]) !=0 :
            moyenne_tried = nbr_tried //(lcourse[0]+lcourse[1])
            lcourse.append (moyenne_tried)
    else :
            lcourse.append (None)

    conn.close()
    return lcourse  


@app.route('/')
def index():
        return render_template("index.html")

@app.route('/LSINF1252')
def LSINF1252( infocourse = None ):
        return render_template("LSINF1252.html", infocourse = info_course ('LSINF1252'))

@app.route('/LEPL1402')
def LEPL1402(infocourse = None):
        return render_template("LEPL1402.html", infocourse = info_course ('LEPL1402'))

@app.route('/LSINF1101_PYTHON')
def LSINF1101_PYTHON(infocourse = None):
        return render_template("LSINF1101_PYTHON.html", infocourse = info_course ('LSINF1101_PYTHON'))
