from flask import Flask, render_template , request
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

def info_task (tache):
    """
    pré: Le nom de la tache 
    post: return une liste sous la forme [nom du cours où elle se trouve,nombre de réussite, nombre d'échec , nombre d'essaye total, nombre d'essaye moyen ]
    """
    conn = sqlite3.connect ('inginious.sqlite')
    c = conn.cursor ()

    ltache = []

    #trouve le cours où est la tâche
    c.execute ("SELECT course FROM user_tasks WHERE task = '{}'".format(tache))
    cours = c.fetchone()
    if cours == None :
            return None
    else:
        name = ""
        for i in range (0, len (cours)):
                if cours [i] == "(" or cours [i] == ")" or cours [i] == ",":
                    "nothing"
                else:
                    name += str (cours[i])
        ltache.append (name)
        
        #trouve le nombre de réussite de la tache
        c.execute ("SELECT * FROM user_tasks WHERE task = '{}' and succeeded = 'true'".format(tache))
        r_tache = len (c.fetchall ())
        ltache.append (r_tache)


        #trouve le nombre de réussite de la tache
        c.execute ("SELECT * FROM user_tasks WHERE task = '{}' and succeeded = 'false'".format(tache))
        f_tache = len (c.fetchall ())
        ltache.append (f_tache)


        #trouve le nombre d'essaye de la tâche 
        c.execute ("SELECT tried FROM user_tasks WHERE task = '{}'".format(tache))
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
        ltache.append (nbr_tried)


        #trouve le nombre moyen d'essaye par étudiant 
        if (ltache[1]+ltache[2]) !=0 :
                moyenne_tried = nbr_tried //(ltache[1]+ltache[2])
                ltache.append (moyenne_tried)
        else :
                ltache.append (None)

        conn.close()
        return ltache




@app.route('/')
def index():
        return render_template("index.html")

@app.route('/LSINF1252', methods= ['POST', 'GET'])
def LSINF1252( infocourse = None, name_task = None , infotache = None ):
        if request.method == 'POST':
                nom = request.form.get ("name_tache")
                ltache = info_task (nom)
                if info_task (nom) != None :
                        if ltache [0] == "LSINF1252":
                                return render_template("LSINF1252.html", infocourse = info_course ('LSINF1252'), name_task = nom, infotache = ltache )
                        else:
                                return render_template("LSINF1252.html", infocourse = info_course ('LSINF1252'), name_task = "Cette tâche ne  fait pas partie du cours LSINF1252 " )
                
                else:
                        return render_template("LSINF1252.html", infocourse = info_course ('LSINF1252'), name_task = "Cette têche n'existe pas" )  


        return render_template("LSINF1252.html", infocourse = info_course ('LSINF1252'))




@app.route('/LEPL1402', methods= ['POST', 'GET'])
def LEPL1402( infocourse = None, name_task = None , infotache = None):
        if request.method == 'POST':
                nom = request.form.get ("name_tache")
                ltache = info_task (nom)
                if info_task (nom) != None :
                        if ltache [0] == "LEPL1402":
                                return render_template("LEPL1402.html", infocourse = info_course ('LEPL1402'), name_task = nom , infotache = ltache)
                        else:
                                return render_template("LEPL1402.html", infocourse = info_course ('LEPL1402'), name_task = "Cette tâche ne  fait pas partie du cours LEPL1402 " )
                
                else:
                        return render_template("LEPL1402.html", infocourse = info_course ('LEPL1402'), name_task = "Cette têche n'existe pas" )  


        return render_template("LEPL1402.html", infocourse = info_course ('LEPL1402'))



@app.route('/LSINF1101_PYTHON', methods= ['POST', 'GET'])
def LSINF1101_PYTHON( infocourse = None, name_task = None, infotache = None ):
        if request.method == 'POST':
                nom = request.form.get ("name_tache")
                ltache = info_task (nom)
                if info_task (nom) != None :
                        if ltache [0] == "LSINF1101_PYTHON":
                                return render_template("LSINF1101_PYTHON.html", infocourse = info_course ('LSINF1101_PYTHON'), name_task = nom, infotache = ltache )
                        else:
                                return render_template("LSINF1101_PYTHON.html", infocourse = info_course ('LSINF1101_PYTHON'), name_task = "Cette tâche ne  fait pas partie du cours LSINF1101_PYTHON " )
                
                else:
                        return render_template("LSINF1101_PYTHON.html", infocourse = info_course ('LSINF1101_PYTHON'), name_task = "Cette têche n'existe pas" )  


        return render_template("LSINF1101_PYTHON.html", infocourse = info_course ('LSINF1101_PYTHON'))
